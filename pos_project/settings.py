import os
import pymysql
pymysql.install_as_MySQLdb()
from pathlib import Path

BASE_DIR = Path(**file**).resolve().parent.parent



SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me')
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
‘django.contrib.admin’,
‘django.contrib.auth’,
‘django.contrib.contenttypes’,
‘django.contrib.sessions’,
‘django.contrib.messages’,
‘django.contrib.staticfiles’,
‘rest_framework’,
‘shop’,
]

MIDDLEWARE = [
‘django.middleware.security.SecurityMiddleware’,
‘whitenoise.middleware.WhiteNoiseMiddleware’,
‘django.contrib.sessions.middleware.SessionMiddleware’,
‘django.middleware.common.CommonMiddleware’,
‘django.middleware.csrf.CsrfViewMiddleware’,
‘django.contrib.auth.middleware.AuthenticationMiddleware’,
‘django.contrib.messages.middleware.MessageMiddleware’,
‘django.middleware.clickjacking.XFrameOptionsMiddleware’,
]

ROOT_URLCONF = ‘pos_project.urls’

TEMPLATES = [
{
‘BACKEND’: ‘django.template.backends.django.DjangoTemplates’,
‘DIRS’: [],
‘APP_DIRS’: True,
‘OPTIONS’: {
‘context_processors’: [
‘django.template.context_processors.debug’,
‘django.template.context_processors.request’,
‘django.contrib.auth.context_processors.auth’,
‘django.contrib.messages.context_processors.messages’,
],
},
},
]

WSGI_APPLICATION = ‘pos_project.wsgi.application’

DATABASES = {
‘default’: {
‘ENGINE’: ‘django.db.backends.mysql’,
‘NAME’: os.environ.get(‘MYSQLDATABASE’, ‘railway’),
‘USER’: os.environ.get(‘MYSQLUSER’, ‘root’),
‘PASSWORD’: os.environ.get(‘MYSQLPASSWORD’, ‘’),
‘HOST’: os.environ.get(‘MYSQLHOST’, ‘mysql.railway.internal’),
‘PORT’: os.environ.get(‘MYSQLPORT’, ‘3306’),
‘OPTIONS’: {
‘charset’: ‘utf8mb4’,
},
}
}

USE_I18N = False
USE_TZ = True
TIME_ZONE = ‘Asia/Rangoon’

STATIC_URL = ‘/static/’
STATIC_ROOT = BASE_DIR / ‘staticfiles’
STATICFILES_STORAGE = ‘whitenoise.storage.CompressedManifestStaticFilesStorage’
DEFAULT_AUTO_FIELD = ‘django.db.models.BigAutoField’
LOGIN_URL = ‘/login/’
LOGIN_REDIRECT_URL = ‘/’