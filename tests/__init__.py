from unittest import TestCase
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


class BaseTest(TestCase):
    if not hasattr(TestCase, 'assertItemsEqual'):
        def assertItemsEqual(self, expected_seq, actual_seq, msg=None):
            self.assertEqual(sorted(expected_seq), sorted(actual_seq), msg=msg)

    if not hasattr(TestCase, 'assertIsInstance'):
        def assertIsInstance(self, instance, klass, msg=None):
            self.assertTrue(isinstance(instance, klass), msg=msg)

    if not hasattr(TestCase, 'assertDictContainsSubset'):
        def assertDictContainsSubset(self, needle, haystack, msg=None):
            self.assertTrue(set(needle.items()).issubset(set(haystack.items())), msg=msg)