Flask-Kadabra
=============

.. image:: https://secure.travis-ci.org/bal2ag/flask-cachual.png?branch=master
    :target: http://travis-ci.org/bal2ag/flask-cachual
    :alt: Build

.. image:: https://readthedocs.org/projects/flask-cachual/badge/?version=latest&style
    :target: http://flask-cachual.readthedocs.org/
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/bal2ag/flask-cachual/badge.svg?branch=master
    :target: https://coveralls.io/github/bal2ag/flask-cachual?branch=master
    :alt: Coverage

Flask-Cachual is a Flask extension for the `Cachual
<https://github.com/bal2ag/cachual>`_ library. It allows you to cache the
return values of functions in your Flask app with a simple decorator::

    from flask_cachual import cached

    @cached(ttl=300) # 5 minutes
    def get_user_email(user_id):
        ...

It's that easy!

For details on how to install and use, see the `documentation
<http://flask-cachual.readthedocs.io/en/latest/>`_.
