#!/usr/bin/env python

import os
import sys
import pytest
from django.conf import settings


settings.configure(USE_TZ=True)

try:
    import django
    setup = django.setup
except AttributeError:
    pass
else:
    setup()

args = ['-rsxX', '--tb=native', '--cov', 'daterange_filter', '--cov-config', '.coveragerc',
        '--cov-report', 'html', '--cov-report', 'term-missing'] + sys.argv[1:]

sys.exit(pytest.main(args + ['tests/']))
