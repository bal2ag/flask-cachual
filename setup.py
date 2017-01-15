"""
Flask-Cachual
-------------

Flask extension for the Cachual library. See https://github.com/bal2ag/cachual
"""
import ast, re

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('flask_cachual.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='Flask-Cachual',
    version=version,
    url='https://github.com/bal2ag/flask-cachual',
    #license='BSD',
    author='Alex Landau',
    author_email='balexlandau@gmail.com',
    description='Flask extension for the Cachual library',
    long_description=__doc__,
    py_modules=['flask_cachual'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Cachual>=0.2.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
