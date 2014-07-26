#! -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='hello_flask',
      version='0.0.1',
      author='Kang Hyojun',
      author_email='hyojun@admire.kr',
      install_requires=[
          'flask==0.10.1', 'flask-script==2.0.5', 'sqlalchemy==0.9.7',
          'pytest==2.6.0'
      ])
