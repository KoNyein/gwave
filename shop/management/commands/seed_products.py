from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    help = 'Seed sample products'

    def handle(self, *args, **kwargs):
        categories_data = [
            ('🍹 အချိုရည်', '🍹'),
            ('🍪 မုန့်', '🍪'),
            ('🧴 အိမ်သုံး', '🧴'),
            ('🍿 မုန့်ပေါ်', '🍿'),
            ('📝 ရုံးသုံး', '📝'),
        ]
        cats = {}
        for name, emoji in categories_data:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'emoji': emoji})
            cats[name] = cat

        products = [
            ('ရေသန့်', '🍶', '🍹 အချိုရည်', 500, 50),
            ('ကော်ဖီ', '☕', '🍹 အချိုရည်', 1500, 30),
            ('ဆိုဒါ', '🥤', '🍹 အချိုရည်', 800, 24),
            ('လက်ဖက်ရည်', '🍵', '🍹 အချိုရည်', 1000, 20),
            ('မုန့်', '🍞', '🍪 မုန့်', 2000, 15),
            ('ချောကလက်', '🍫', '🍪 မုန့်', 3500, 3),
            ('ဆပ်ပြာ', '🧼', '🧴 အိမ်သုံး', 1500, 40),
            ('ရေချိုး', '🧴', '🧴 အိမ်သုံး', 5000, 18),
            ('အာလူးကြော်', '🥔', '🍿 မုန့်ပေါ်', 2500, 35),
            ('ပြောင်းဖူး', '🍿', '🍿 မုန့်ပေါ်', 2000, 22),
            ('ဘောပင်', '🖊️', '📝 ရုံးသုံး', 500, 100),
            ('မှတ်စုစာ', '📓', '📝 ရုံးသုံး', 2000, 45),
        ]

        count = 0
        for name, emoji, cat_name, price, stock in products:
            _, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'emoji': emoji,
                    'category': cats[cat_name],
                    'price_mmk': price,
                    'stock': stock,
                    'low_stock_threshold': 5,
                }
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ {count} products seeded!'))
