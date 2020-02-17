# Copyright (c) 2020 Shawn Chen.
# Monkey patch for the flask_appbuilder
"""
Make the standard library cooperative.

"""
from __future__ import absolute_import
from __future__ import print_function
import sys
import fab_admin
import logging

log = logging.getLogger(__name__)


class MonkeyPatchWarning(RuntimeWarning):
    """
    The type of warnings we issue.

    .. versionadded:: 1.3a2
    """

# maps module name -> {attribute name: original item}
# e.g. "time" -> {"sleep": built-in function sleep}
saved = {}


def is_module_patched(mod_name):
    """
    Check if a module has been replaced with a cooperative version.

    :param str mod_name: The name of the standard library module,
        e.g., ``'socket'``.

    """
    return mod_name in saved


def is_object_patched(mod_name, item_name):
    """
    Check if an object in a module has been replaced with a
    cooperative version.

    :param str mod_name: The name of the standard library module,
        e.g., ``'socket'``.
    :param str item_name: The name of the attribute in the module,
        e.g., ``'create_connection'``.

    """
    return is_module_patched(mod_name) and item_name in saved[mod_name]


def _get_original(name, items):
    d = saved.get(name, {})
    values = []
    module = None
    for item in items:
        if item in d:
            values.append(d[item])
        else:
            if module is None:
                module = __import__(name)
            values.append(getattr(module, item))
    return values


def get_original(mod_name, item_name):
    """
    Retrieve the original object from a module.

    If the object has not been patched, then that object will still be
    retrieved.

    :param str mod_name: The name of the standard library module,
        e.g., ``'socket'``.
    :param item_name: A string or sequence of strings naming the
        attribute(s) on the module ``mod_name`` to return.

    :return: The original value if a string was given for
             ``item_name`` or a sequence of original values if a
             sequence was passed.
    """
    if isinstance(item_name, str):
        return _get_original(mod_name, [item_name])[0]
    return _get_original(mod_name, item_name)


_NONE = object()


def patch_item(module, attr, newitem):
    olditem = getattr(module, attr, _NONE)
    if olditem is not _NONE:
        saved.setdefault(module.__name__, {}).setdefault(attr, olditem)
    setattr(module, attr, newitem)


def remove_item(module, attr):
    olditem = getattr(module, attr, _NONE)
    if olditem is _NONE:
        return
    saved.setdefault(module.__name__, {}).setdefault(attr, olditem)
    delattr(module, attr)


def _patch_module(target_module, source_module, items=None,
                 _notify_did_subscribers=True):
    """

    """
    for attr in items:
        patch_item(target_module, attr, getattr(source_module, attr))

    return True

def patch_module(name, items=None, path=None, _notify_did_subscribers=True):
    """dynamic import module from file"""
    import os
    import importlib
    target_module = importlib.import_module(name)
    base_patch_dir = fab_admin.__path__[0]
    spec = importlib.util.spec_from_file_location(name, os.path.join(base_patch_dir, 'fab_manager_overwrite',
                                                                     path))
    source_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source_module)
    _patch_module(target_module, source_module, items=items,
                 _notify_did_subscribers=_notify_did_subscribers)

    return source_module, target_module


def _queue_warning(message, _warnings):
    # Queues a warning to show after the monkey-patching process is all done.
    # Done this way to avoid extra imports during the process itself, just
    # in case. If we're calling a function one-off (unusual) go ahead and do it
    if _warnings is None:
        _process_warnings([message])
    else:
        _warnings.append(message)


def _process_warnings(_warnings):
    import warnings
    for warning in _warnings:
        warnings.warn(warning, MonkeyPatchWarning, stacklevel=3)


def _check_repatching(**module_settings):
    _warnings = []
    key = '_fab_admin_saved_patch_all'
    if saved.get(key, module_settings) != module_settings:
        _queue_warning("Patching more than once will result in the union of all True"
                       " parameters being patched",
                       _warnings)

    first_time = key not in saved
    saved[key] = module_settings
    return _warnings, first_time, module_settings


def patch_all(is_fab_model=True, is_fab_baseviews=True, is_flask_redis_sentinel=True,
              is_fab_secu_decorators=True, is_flask_rq2_app=True, is_flask_rq2_cli=True,
              is_rq_cli=True, is_rq_helper=True, is_rq_schedule_dashboard_web=True):
    """
        patch flask_appbuilder
    """

    # Check to see if they're changing the patched list
    _warnings, first_time, modules_to_patch = _check_repatching(**locals())
    if not _warnings and not first_time:
        # Nothing to do, identical args to what we just
        # did
        return
    # order is important
    if is_fab_model:
        patch_module('flask_appbuilder', ['Model', 'Base'], 'flask_appbuilder/models/sqla/__init__.py')

    if is_fab_baseviews:
        patch_module('flask_appbuilder', ['BaseView'], 'flask_appbuilder/baseviews.py')
        patch_module('flask_appbuilder.baseviews', ['BaseView'], 'flask_appbuilder/baseviews.py')

    if is_flask_redis_sentinel:
        patch_module('flask_redis_sentinel', ['SentinelExtension', 'RedisSentinel'], 'flask_redis_sentinel.py')

    if is_fab_secu_decorators:
        # decorate has_access_api to support identify 403 401 type
        patch_module('flask_appbuilder.security.decorators', ['has_access_api'],
                     'flask_appbuilder/security/decorators.py')

    if is_flask_rq2_app:
        # patch flask_rq2 pass client by init method
        patch_module('flask_rq2', ['RQ'], 'flask_rq2/app.py')
        patch_module('flask_rq2.app', ['RQ'], 'flask_rq2/app.py')

    if is_flask_rq2_cli:
        """patch flask_rq2_cli module to add worker before run action"""
        patch_module('flask_rq2.cli', ['reset_db_connections', 'worker'], 'flask_rq2/cli.py')

    if is_rq_cli:
        """patch rq_cli to add extra click option to pass client into rq"""
        patch_module('rq.cli.cli', ['shared_options'], 'rq/cli/cli.py')

    if is_rq_helper:
        patch_module('rq.cli.helpers', ['CliConfig'], 'rq/cli/helpers.py')

    if is_rq_schedule_dashboard_web:
        patch_module('rq_scheduler_dashboard.web', ['setup_rq_connection'], 'rq_scheduler_dashboard/web.py')
