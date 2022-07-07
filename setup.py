#!/usr/bin/env python3
# =============================================================================
# @file    setup.py
# @brief   Installation setup file
# @author  Michael Hucka <mhucka@caltech.edu>
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/caltechlibrary/commonpy
#
# Note: the full configuration metadata is maintained in setup.cfg, not here.
# This file exists to hook in setup.cfg and requirements.txt, so that the
# requirements don't have to be repeated and so that "python3 setup.py" works.
# =============================================================================

from os.path import abspath, dirname, exists, join
from setuptools import setup

required = []
requirements_file = join(abspath(dirname(__file__)), 'requirements.txt')
if exists(requirements_file):
    with open(requirements_file, encoding = 'utf-8') as f:
        required = [line for line in filter(str.strip, f.read().splitlines())
                    if not line.startswith('#')]
    if any(item.startswith(('-', '.', '/')) for item in required):
        # The requirements.txt uses pip features. Try to use pip's parser.
        try:
            from pip._internal.req import parse_requirements
            from pip._internal.network.session import PipSession
            parsed = parse_requirements(requirements_file, PipSession())
            required = [item.requirement for item in parsed]
        except ImportError:
            # No pip, or not the expected version. Give up & leave list as is.
            pass

setup(
    setup_requires = ['wheel'],
    install_requires = required,
)
