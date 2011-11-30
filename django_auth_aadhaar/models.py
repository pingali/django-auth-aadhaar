from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save

class AadhaarUserProfile(models.Model): 
    user = models.OneToOneField(User) 

    # Aadhaar number..
    aadhaar_id = models.CharField(max_length=12, default="0") 

    #Time stamps 
    first_authentication = models.DateTimeField(auto_now_add=True) 
    last_unsuccessful_authentication = models.DateTimeField(null=True) 
    last_successful_authentication = models.DateTimeField(auto_now=True) 

    # Stats 
    num_successful_authentications = models.IntegerField(default=0)
    num_unsuccessful_authentications = models.IntegerField(default=0)
    
    def is_valid_aadhaar(self): 
        if (self.aadhaar_id == "0"):
            return False 
        else:
            return True

class AadhaarAuthResults(models.Model): 
    profile = models.ForeignKey(AadhaarUserProfile) 
    
    # response XML 
    # Ret 
    # Error code  
    # info 

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        AadhaarUserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)



