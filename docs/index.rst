Flask-Cachual
=============

Flask-Cachual is a Flask extension for the `Cachual
<https://github.com/bal2ag/cachual>`_ library. It allows you to cache your
function's return values with a simple decorator::

    from flask_cachual import cached

    @cached(ttl=300) # 5 minutes
    def get_user_email(user_id):
        ...

It's that easy!

.. contents::
    :local:
    :backlinks: none

Installation
============

Install the extension with pip::

    $ pip install flask-cachual

Usage
=====

You can initialize :class:`~flask_cachual.Cachual` directly::

    from flask import Flask
    from flask_cachual import Cachual

    app = Flask()
    Cachual(app)

Or, you can defer initialization if you are utilizing the
`application factory <http://flask.pocoo.org/docs/0.12/patterns/appfactories/>`_
pattern, using the :meth:`~flask_cachual.Cachual.init_app` method::

    from flask import Flask
    from flask_cachual import Cachual

    cachual = Cachual()

    def create_app():
        app = Flask()
        cachual.init_app(app)

That's it! Now, anywhere in your application code, you can use the
:class:`~flask_cachual.cached` decorator on any function whose value you want
to cache. For example::

    @app.route('/<userId>/email')
    def user_email(userId):
        return jsonify({'email': get_user_email(userId)})

    @cached(ttl=300)
    def get_user_email(userId):
        ...

Whenever the decorated method is called, your app will check the configured
cache for the result. If there's a cache hit, it's immediately returned;
otherwise the function will execute as normal, the value will be stored in the
cache with a unique key, and the value will be returned. Make sure you read
Cachual's `documentation <http://cachual.readthedocs.io/en/latest/>`_ carefully
to understand what values can be cached, how it works, and how to deal with
more complex data types.

Speaking of configuration...

.. _configuration:

Configuration
=============

You need to specify two configuration values in your application's config:

================ ==============================================================
``CACHUAL_TYPE`` The type of cache you want to use. Currently only two values
                 are supported: ``redis`` which corresponds to
                 :class:`~cachual.RedisCache` and ``memcached`` which
                 corresponds to :class:`~cachual.MemcachedCache`.
``CACHUAL_ARGS`` Dictionary of arguments to initialize the the Cachual cache
                 with. If ``None``, the cache's defaults will be used.
================ ==============================================================

API Documentation
=================

.. module:: flask_cachual

.. autoclass:: Cachual

    .. automethod:: init_app

.. autofunction:: cached
