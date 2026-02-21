from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count, F
from django.utils import timezone
from django.contrib import messages
import json
from datetime import timedelta, date
from .models import Product, Category, Sale, SaleItem


# ─── POS ──────────────────────────────────────────────────────────────────────

@login_required
def pos_view(request):
    return render(request, 'shop/pos.html')


@login_required
def api_products(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    data = []
    for p in products:
        data.append({
            'id': p.id,
            'name': p.name,
            'emoji': p.emoji,
            'category': str(p.category) if p.category else 'Others',
            'price_mmk': float(p.price_mmk),
            'price_thb': float(p.price_thb),
            'stock': p.stock,
            'is_low_stock': p.is_low_stock,
            'is_out_of_stock': p.is_out_of_stock,
        })
    return JsonResponse({'products': data})


@login_required
@csrf_exempt
def api_checkout(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    try:
        data = json.loads(request.body)
        cart = data.get('cart', [])
        currency = data.get('currency', 'MMK')
        payment_method = data.get('payment_method', 'cash')
        discount = int(data.get('discount_mmk', 0))
        cash_received = int(data.get('cash_received_mmk', 0))

        if not cart:
            return JsonResponse({'error': 'Cart is empty'}, status=400)

        subtotal = 0
        sale_items = []

        for item in cart:
            product = get_object_or_404(Product, id=item['id'])
            qty = int(item['qty'])
            if product.stock < qty:
                return JsonResponse({'error': f'{product.name} stock မလုံပါ'}, status=400)
            line_total = int(product.price_mmk) * qty
            subtotal += line_total
            sale_items.append({
                'product': product,
                'qty': qty,
                'price_mmk': int(product.price_mmk),
                'subtotal': line_total,
            })

        total = max(0, subtotal - discount)
        change = max(0, cash_received - total)

        # Create Sale
        sale = Sale.objects.create(
            currency=currency,
            payment_method=payment_method,
            subtotal=subtotal,
            discount=discount,
            total=total,
            cash_received=cash_received,
            change_amount=change,
            cashier=request.user,
        )

        for si in sale_items:
            SaleItem.objects.create(
                sale=sale,
                product=si['product'],
                product_name=si['product'].name,
                product_emoji=si['product'].emoji,
                price_mmk=si['price_mmk'],
                quantity=si['qty'],
                subtotal=si['subtotal'],
            )
            # Reduce stock
            si['product'].stock = F('stock') - si['qty']
            si['product'].save(update_fields=['stock'])

        return JsonResponse({
            'success': True,
            'sale_number': sale.sale_number,
            'total': total,
            'change': change,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ─── DASHBOARD ────────────────────────────────────────────────────────────────

@login_required
def dashboard_view(request):
    low_stock = Product.objects.filter(stock__lte=F('low_stock_threshold'), stock__gt=0, is_active=True)
    out_of_stock = Product.objects.filter(stock=0, is_active=True)
    return render(request, 'shop/dashboard.html', {
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
    })


@login_required
def api_dashboard_stats(request):
    today = timezone.localdate()
    month_start = today.replace(day=1)

    today_sales = Sale.objects.filter(created_at__date=today)
    month_sales = Sale.objects.filter(created_at__date__gte=month_start)

    today_revenue = today_sales.aggregate(t=Sum('total'))['t'] or 0
    month_revenue = month_sales.aggregate(t=Sum('total'))['t'] or 0
    today_count = today_sales.count()
    month_count = month_sales.count()

    total_products = Product.objects.filter(is_active=True).count()
    low_stock_count = Product.objects.filter(stock__lte=F('low_stock_threshold'), stock__gt=0, is_active=True).count()
    out_of_stock_count = Product.objects.filter(stock=0, is_active=True).count()

    return JsonResponse({
        'today_revenue': float(today_revenue),
        'month_revenue': float(month_revenue),
        'today_count': today_count,
        'month_count': month_count,
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
    })


@login_required
def api_sales_chart(request):
    chart_type = request.GET.get('type', 'daily')
    today = timezone.localdate()

    if chart_type == 'daily':
        # Last 30 days
        days = [(today - timedelta(days=i)) for i in range(29, -1, -1)]
        labels = [d.strftime('%d/%m') for d in days]
        values = []
        for d in days:
            rev = Sale.objects.filter(created_at__date=d).aggregate(t=Sum('total'))['t'] or 0
            values.append(float(rev))
    else:
        # Last 12 months
        months = []
        for i in range(11, -1, -1):
            m = (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
            months.append(m)
        labels = [m.strftime('%b %Y') for m in months]
        values = []
        for m in months:
            end = (m.replace(month=m.month % 12 + 1, day=1) if m.month < 12
                   else m.replace(year=m.year + 1, month=1, day=1))
            rev = Sale.objects.filter(created_at__date__gte=m, created_at__date__lt=end).aggregate(t=Sum('total'))['t'] or 0
            values.append(float(rev))

    return JsonResponse({'labels': labels, 'values': values})


# ─── PRODUCTS ─────────────────────────────────────────────────────────────────

@login_required
def product_list_view(request):
    products = Product.objects.filter(is_active=True).select_related('category').order_by('category', 'name')
    categories = Category.objects.all()
    return render(request, 'shop/products.html', {'products': products, 'categories': categories})


@login_required
def product_add_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        try:
            cat_id = request.POST.get('category')
            Product.objects.create(
                name=request.POST['name'],
                emoji=request.POST.get('emoji', '🛍️'),
                category_id=cat_id if cat_id else None,
                price_mmk=request.POST['price_mmk'],
                stock=request.POST.get('stock', 0),
                low_stock_threshold=request.POST.get('low_stock_threshold', 5),
            )
            messages.success(request, '✅ ကုန်ပစ္စည်း ထည့်ပြီးပါပြီ!')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f'❌ Error: {e}')
    return render(request, 'shop/product_form.html', {'categories': categories, 'action': 'Add'})


@login_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        try:
            cat_id = request.POST.get('category')
            product.name = request.POST['name']
            product.emoji = request.POST.get('emoji', '🛍️')
            product.category_id = cat_id if cat_id else None
            product.price_mmk = request.POST['price_mmk']
            product.stock = request.POST.get('stock', 0)
            product.low_stock_threshold = request.POST.get('low_stock_threshold', 5)
            product.save()
            messages.success(request, '✅ ကုန်ပစ္စည်း ပြင်ပြီးပါပြီ!')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f'❌ Error: {e}')
    return render(request, 'shop/product_form.html', {'categories': categories, 'product': product, 'action': 'Edit'})


@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_active = False
        product.save()
        messages.success(request, f'🗑️ {product.name} ဖျက်ပြီးပါပြီ!')
        return redirect('product_list')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})


# ─── SALES HISTORY ────────────────────────────────────────────────────────────

@login_required
def sales_history_view(request):
    sales = Sale.objects.prefetch_related('items').order_by('-created_at')[:100]
    return render(request, 'shop/sales_history.html', {'sales': sales})


@login_required
def sale_detail_view(request, pk):
    sale = get_object_or_404(Sale.objects.prefetch_related('items'), pk=pk)
    return render(request, 'shop/sale_detail.html', {'sale': sale})
