from flask import (Flask, g, Response, current_app)
from flask_cachual import Cachual, cached
from mock import mock, MagicMock

import cachual, pytest


def get_app():
    return Flask(__name__)

@mock.patch('flask_cachual.Cachual.init_app')
def test_ctor_no_app(mock_init_app):
    cachual = Cachual()

    cachual.init_app.assert_has_calls([])
    assert cachual.app == None

@mock.patch('flask_cachual.Cachual.init_app')
def test_ctor_app(mock_init_app):
    app = MagicMock()
    cachual = Cachual(app)

    cachual.init_app.assert_called_with(app)
    assert cachual.app == app

def test_init_no_type():
    app = get_app()

    cachual = Cachual()
    with pytest.raises(Exception):
        cachual.init_app(app)

def test_init_no_args():
    app = get_app()
    app.config["CACHUAL_TYPE"] = 'redis'

    cachual = Cachual()
    with pytest.raises(Exception):
        cachual.init_app(app)

@mock.patch('cachual.RedisCache')
def test_init_redis(mock_redis_cache):
    cache = mock_redis_cache.return_value
    cache_args = {'host': 'test', 'port': 1, 'db': 1}

    app = get_app()
    app.config["CACHUAL_TYPE"] = 'redis'
    app.config["CACHUAL_ARGS"] = cache_args

    cachual = Cachual(app)
    assert app.cachual_cache == cache

@mock.patch('cachual.MemcachedCache')
def test_init_memcached(mock_memcached_cache):
    cache = mock_memcached_cache.return_value
    cache_args = {'server': ('test', 1)}

    app = get_app()
    app.config["CACHUAL_TYPE"] = 'memcached'
    app.config["CACHUAL_ARGS"] = cache_args

    cachual = Cachual(app)
    assert app.cachual_cache == cache

def test_init_invalid_type():
    app = get_app()
    app.config["CACHUAL_TYPE"] = 'R4n3ign4wuih4'
    app.config["CACHUAL_ARGS"] = {}

    cachual = Cachual()
    with pytest.raises(Exception):
        cachual.init_app(app)

@mock.patch('cachual.RedisCache')
def test_cached(mock_redis_cache):
    cache = mock_redis_cache.return_value
    cache.cached = MagicMock()
    cache_decorator = cache.cached.return_value
    cache_decorated = cache_decorator.return_value

    cache_args = {'host': 'test', 'port': 1, 'db': 1}
    test_args = ['arg1', 'arg2']
    test_kwargs = {"kwarg1": "val1", "kwarg2": "val2"}

    app = get_app()
    app.config["CACHUAL_TYPE"] = 'redis'
    app.config["CACHUAL_ARGS"] = cache_args
    cachual = Cachual(app)

    ttl = MagicMock()
    pack = MagicMock()
    unpack = MagicMock()

    @cached(ttl=ttl, pack=pack, unpack=unpack)
    def test_cache_func(*args, **kwargs):
        pass

    @app.route('/')
    def test_route():
        test_cache_func(*test_args, **test_kwargs)
        return 'ok'

    with app.test_client() as c:
        c.get('/')
        cache.cached.assert_called_with(ttl, pack, unpack)
        cache_decorator.assert_called_with(test_cache_func.__wrapped__)
        cache_decorated.assert_called_with(*test_args, **test_kwargs)
