# vim: expandtab tabstop=4 shiftwidth=4

import pkgutil
import sys

if sys.version_info.major == 3:
    from html import escape
elif sys.version_info.major == 2:
    from cgi import escape
else:
    raise Exception('Invalid version of Python')

def _str_to_bytes(s):
    if sys.version_info.major == 3:
        return bytes(s, encoding='utf8')
    elif sys.version_info.major == 2:
        return s
    else:
        return s

def _in_virtualenv():
    # based on http://stackoverflow.com/questions/1871549/python-determine-if-running-inside-virtualenv
    if hasattr(sys, 'real_prefix'):
        return True
    return False

def _config_contains_target(config_options):
    for config_option in config_options:
        if config_option.startswith('--target=') or config_option.startswith('--target '):
            return True

def _config_contains_user(config_options):
    for config_option in config_options:
        if config_option == '--user':
            return True

def _apply_user(config_options, test_mode=False):
    # tests happen in a virtualenv, so test_mode allows
    # this check to be bypassed so the rest of the
    # function can be tested
    if test_mode is False and _in_virtualenv():
        return []

    if _config_contains_target(config_options):
        return []

    if _config_contains_user(config_options):
        # don't need to specify --user again if it's already in the config
        return []

    return ['--user']

def _bytes_to_str(b):
    if sys.version_info.major == 3:
        return str(b, encoding='utf8')
    elif sys.version_info.major == 2:
        return b
    else:
        return b

def _html_escape(s):
    return escape(s, quote=True)

def _in_ipython():
    try:
        from IPython import get_ipython

        if get_ipython() is not None:
            return True
        else:
            return False

    except ImportError:
        return False

    return False

def _stdlib_packages(version=sys.version_info.major):
    stdlib_list = ''

    if version == 3:
        stdlib_list = pkgutil.get_data(__name__, 'data/libs3.txt')
    elif version == 2:
        stdlib_list = pkgutil.get_data(__name__, 'data/libs2.txt')

    stdlib_list = _bytes_to_str(stdlib_list)
    stdlib_list = [ x.strip() for x in stdlib_list.split('\n') ]
    stdlib_list = [ x for x in stdlib_list if len(x) > 0 ]
    return set(stdlib_list)
