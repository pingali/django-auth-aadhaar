#!/usr/bin/env python 

# Uncomment these for testing
import os, sys 
here = lambda path: os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
sys.path.insert(0,here('../../pyAadhaarAuth'))
sys.path.insert(0,here('../examples'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'authextend.settings'


from django.db import models
from django.contrib.auth import backends
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from config import Config
from datetime import datetime 
import logging 
import traceback 
import gc 

from AadhaarAuth.request import AuthRequest
from AadhaarAuth.data import AuthData
from AadhaarAuth.command import AuthConfig 

log = logging.getLogger("AadhaarBackend") 

class AadhaarBackend(backends.ModelBackend):

    def authenticate(self, **credentials):
        print "AadhaarBackend.authenticate()" 
        print "Credentials = ", credentials 
        aadhaar_id = credentials['aadhaar_id']
        try:
            aadhaar_user = AadhaarBackendHelper(self, aadhaar_id=aadhaar_id)
            user = None 
            try: 
                print "Type of aadhaar_user = ", type(aadhaar_user)
                user = aadhaar_user.authenticate(credentials)
            except: 
                print "Caught exception" 
                traceback.print_exc() 
                pass 
            print "Authenticated with aadhaar" 
            return user
        except:
            print "Authentication failed" 
            traceback.print_exc() 
            return None
        

    def get_user(self, user_id):
        print "AadhaarBackend.get_user() user_id = ",user_id
        user = None
        try:
            user = self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            pass
        print "AadhaarBackend.get_user() returning user = ",user
        return user 

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = User
            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model')
        return self._user_class


class AadhaarBackendHelper(object): 
    
    _user = None 

    def __init__(self, backend, aadhaar_id, user=None):
        print "AadhaarBackendHelper.init()"
        self._aadhaar_id = aadhaar_id 
    
        if user is not None: 
            self._set_authenticated_user(user) 

    def _set_authenticated_user(self, user): 
        print "AadhaarBackendHelper.set_authenticated_user()"
        profile = user.get_profile() 
        if attr == None: 
            print "Setting attr on ", user 
            setattr(profile, 'aadhaar_id', self._aadhaar_id)         
            profile.save() 
        else:
            print "Found attr ", getattr(profile, 'aadhaar_id'), \
                "for user ", user
        self._user = user 

    def authenticate_with_aadhaar(self, cfg, credentials): 
        """
        Eventually support all possible combinations and levels 
        of authentication 
        """
        log.debug("authenticate_with_aadhaar: credentials = %s " % credentials) 
        if cfg == None: 
            raise Exception("Aadhaar configuration unspecified or invalid") 
        log.debug("authenticate_with_aadhaar: cfg = %s " % cfg)

        auth_type = credentials['aadhaar_auth_type']
        if auth_type != "Pi": 
            raise Exception("Aadhaar auth type %s not supported" % auth_type)
        
        try: 
            aadhaar_id = credentials['aadhaar_id']
            name = credentials['aadhaar_name']
        except: 
            raise Exception("Name of the individual not specified")
        
        cfg.request.uid = aadhaar_id 
        cfg.request.demographics = ["Pi"]
        cfg.request.biometrics = []
        cfg.request['Pi'] = {
            'ms': "E",
            'name': name,
            }

        log.debug("authenticate_with_aadhaar: request  %s " % cfg.request)

        # => Generate the request XML and send it over the 
        # server 

        data = AuthData(cfg=cfg) 
        data.generate_client_xml() 
        exported_data = data.export_request_data() 
        req = AuthRequest(cfg)
        req.import_request_data(exported_data)
        req.execute()
            
        return req.is_successful()
            
    def authenticate(self, credentials):         
        print "AadhaarBackendHelper.authenticate()", credentials 
        
        # Check if the user exists in the database 
        user = None 
        try: 
            user = User.objects.get(username=self._aadhaar_id)
        except: 
            pass 
        
        authenticated = False 
        try: 
            cfg = aadhaar_settings.get_cfg() 
            authenticated = self.authenticate_with_aadhaar(cfg, credentials) 
        except: 
            print "Authentication unsuccessful" 
            if user != None: 
                print "Returning without creating user" 
                # Dont create user 
                return None 

        if (user == None): 
            try: 
                if authenticated:
                    # Create the user 
                    user = User(username=self._aadhaar_id) 
                    user.set_unusable_password()
                    user.save() # This will create the profile object 
                    
                    # Update the profile 
                    profile = user.get_profile() 
                    profile.aadhaar_id = self._aadhaar_id 
                    profile.last_successful_authentication = datetime.now()
                    profile.num_successful_authentications += 1 
                    profile.save() 
                    
                    print "Created user ", user, " with profile ", profile 
                else: 
                    print "Returning without creating user" 
                    return None
            except: 
                traceback.print_exc() 
                print "Exception in AadhaarBackendHelper.authenticate()" 
                pass 
        else: 
            # user exists in the db. Authentication may have succeeded or 
            # failed. 
            print "User exists" 
            try: 
                profile = user.get_profile() 
            except: 
                # doesnt exist for some reason. Why? 
                print "Creating profile. Check why this has come here" 
                profile = AadhaarUserProfile.objects.create(user=user) 

            print "Profile before updating = ", profile.__dict__
            # Update the stats 
            if authenticated: 
                profile.last_successful_authentication = datetime.now()
                profile.num_successful_authentications += 1 
            else: 
                profile.last_unsuccessful_authentication = datetime.now()
                profile.num_unsuccessful_authentications += 1 
            profile.save() 
            print "Profile before updating = ", profile.__dict__

        # The user may exist but the authentication may have
        # failed. So we keep track of it 
        self._user = user 
        if authenticated: 
            return user 
        else: 
            return None 
    
#    def _get_or_create_user(self): 
#        print "AadhaarBackendHelper.get_or_create_user()" 
#        try: 
#            (self._user, created) = User.objects.get_or_create(username=self._aadhaar_id)
#            if created: 
#                self._user.set_unusable_password()
#                self._user.save() # This will create the profile object 
#            self._set_authenticated_user(self._user) 
#            
#        except: 
#            traceback.print_exc() 
#            pass 





class AadhaarSettings(object):
    """
    This is a simple class to take the place of the global settings object. A
    instance will contain all of our settings as attributes, with default val
    if they are not specified by the configuration.
    """
    defaults = {
        'AADHAAR_CONFIG_FILE': None,
    }

    def __init__(self):
        """
        Loads our settings from django.conf.settings, applying defaults for a
        that are omitted.
        """
        from django.conf import settings

        for name, default in self.defaults.iteritems():
            value = getattr(settings, name, default)
            setattr(self, name, value)
        
        cfg_file = getattr(self, 'AADHAAR_CONFIG_FILE') 
        if cfg_file == None or not (os.path.isfile(cfg_file)): 
            raise Exception("Please define AADHAAR_CONFIG_FILE") 
        
        c = AuthConfig(cfg=cfg_file)
        self.cfg = c.update_config()
        
    def get_cfg(self): 
        return self.cfg 

    def is_valid(self): 
        # Validate the configuration file to make sure 
        # the components are 
        return True 

# Our global settings object
aadhaar_settings = AadhaarSettings()
if not aadhaar_settings.is_valid(): 
    raise Exception("Configuration file is invalid") 



if __name__ == "__main__": 
    

    logging.basicConfig() 
    logging.getLogger().setLevel(logging.WARN) 
    
    sample_data = {'aadhaar_id': '999999990019', 
                   'aadhaar_name': 'Shivshankar Choudhury',
                   'aadhaar_auth_type': 'Pi'}
    cfg = aadhaar_settings.get_cfg() 
    helper = AadhaarBackendHelper(None, None, None)
    helper.authenticate_with_aadhaar(cfg, sample_data)
    
