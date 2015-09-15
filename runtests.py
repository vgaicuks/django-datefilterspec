#!/usr/bin/env python

import os
import sys
import pytest


os.environ['test'] = '1'

args = ['-rsxX', '--tb=native', '--cov', 'daterange_filter', '--cov-config', '.coveragerc',
        '--cov-report', 'html', '--cov-report', 'term-missing'] + sys.argv[1:]

sys.exit(pytest.main(args + ['tests/']))
