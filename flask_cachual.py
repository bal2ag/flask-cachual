from flask import current_app

from functools import wraps

import cachual

__version__ = '0.2.0'

class Cachual(object):
    """This object ties the Flask application object to the Cachual library by
    setting the ``cachual_cache`` attribute of the application instance to the
    Cachual cache as specified by the application's configuration.

    :param app: The Flask application object to initialize.
    :type app: ~flask.Flask
    """
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Configure the application to use Cachual. Based on the application's
        configuration, this will instantiate the cache and give the application
        object access to it via the ``cachual_cache`` attribute. See
        :ref:`configuration`.
 
        :param app: The Flask application object to initialize.
        :type app: ~flask.Flask
        """
        cache_type = app.config.get('CACHUAL_TYPE')
        if not cache_type:
            raise Exception("CACHUAL_TYPE must be specified")
        cache_type = cache_type.lower()
        cache_args = app.config.get('CACHUAL_ARGS', {})

        if cache_type == 'redis':
            app.cachual_cache = cachual.RedisCache(**cache_args)
        elif cache_type == 'memcached':
            app.cachual_cache = cachual.MemcachedCache(**cache_args)
        else:
            raise Exception("Unrecognized cache type: %s" % cache_type)
        self.app = app

def cached(ttl=None, pack=None, unpack=None, use_class_for_self=False):
    """Functions decorated with this will have their value cached via the
    Cachual library. This is basically just a proxy to Cachual's
    :meth:`~cachual.CachualCache.cached` decorator. It ensures that the correct
    cache is used based on the :data:`~flask.current_app` context."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            cache = current_app.cachual_cache
            cache_decorator = cache.cached(ttl, pack, unpack,
                    use_class_for_self)
            return cache_decorator(f)(*args, **kwargs)
        decorated.__wrapped__ = f # For unit testing
        return decorated
    return decorator
