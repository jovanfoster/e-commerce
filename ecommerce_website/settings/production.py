from ._base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '_vxyqzwz21nfu&x8@l%)7oeri=cvqwm4rgd*^zx4l@urr8*q)g'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '_vxyqzwz21nfu&x8@l%)7oeri=cvqwm4rgd*^zx4l@urr8*q)g')


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = ['lit-peak-45044.herokuapp.com']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
) 

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE =  True
SESSION_COOKIE_SECURE = True 

# S3 storage settings
# required to get connection to S3 bucket

AWS_STORAGE_BUCKET_NAME = 'ecommerce-website-jpegs'
AWS_S3_REGION_NAME = 'us-east-2'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

STRIPE_PUBLISHABLE_KEY = 'pk_live_51Hy2IAFRAIcOcOMoorOJH65biLVLoyJZheLNVDrEN2dAHZHlvuajPpzLqjAuNvsFx6fq4vVbCVd0jV9ztyD1BHn100sWxj80wN'
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')