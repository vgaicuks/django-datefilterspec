from django.conf import settings


settings.configure(
    DEBUG=True,
    USE_TZ=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'daterange_filter',
    ],
    SITE_ID=1,
)

try:
    import django
    setup = django.setup
except AttributeError:
    pass
else:
    setup()
