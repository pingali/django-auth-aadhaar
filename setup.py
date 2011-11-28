#!/usr/bin/env python

from distutils.core import setup

classifiers = [    
    'Development Status :: 2 - Pre-Alpha',    
    'Intended Audience :: Developers',    
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',    
    'Programming Language :: Python',    
    'Topic :: System :: Systems Administration :: Authentication/Directory']


setup(name='django_auth_aadhaar',
      version='0.1.0',
      description='Aadhaar auth module for django',
      author='Venkata Pingali',
      author_email='pingali@gmail.com',
      url='http://www.github.com/pingali/django-auth-aadhaar',
      packages=['django_auth_aadhaar'],
      license='LICENSE.txt',
      long_description=open('README.md').read(),
      classifiers=classifiers, 
     )

