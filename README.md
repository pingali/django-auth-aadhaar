Django Aadhaar-based User Authentication Module 
===============================================

The aim is to provide a standard way to add Aadhaar authentication to
all django applications. 

Status
------
Crude integration is now in place. We can start with a Aadhaar-specific
login page, authenicate the user and complete the login process 

Usage
-----

Please add the following to the settings: 

       AUTH_USER_PROFILE='django_aadhaar_auth.AadhaarUserProfile'
       AUTHENTICATION_BACKENDS=('django_aadhaar_auth.backend.AadhaarBackend')
       AADHAAR_CONFIG_FILE='...fixtures/auth.cfg' 

Please provide the full path for configuration file. Once the
configuration is in place, then run the application. The examples
directory has a sample application. 

       $ cd examples/authextend 
       $ python manage.py syncdb 
       $ python manage.py runserver 

Now visit http://localhost:8000/login Fillin the details and press
'Authenticate'. 

Caveat 
------

It is work in progress. Still exploring better ways to implementing
this. For now we use aadhaar number as the username, and
AadhaarUserProfile to store extra information. In the backend we
ignore the username.

1. Only does authentication. Cannot change password or any other
attributes.

2. Creates a local user when the authentication happens. Cant avoid
it, it seems. I looked at RemoteUserBackend as well. 

3. Does not fully address the security issues 

Thanks
------

This is based on the django-ldap-auth implementation. 