from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.models import User
from django_auth_aadhaar.forms import AadhaarAuthForm 

def login_user(request):

    state = "Please log in below..."
    
    # Whats in DB? 
    users = User.objects.all() 
    print "All users = ", users 

    # Clean data from 
    if request.POST:
        form = AadhaarAuthForm(request.POST) 
        credentials = form.cleaned_data 
        # cleanup and extract the aadhaar 
        auth_params = {} 
        for k,v in credentials.iteritems():
            if k.startswith('aadhaar'):
                auth_params[k] = v
        print auth_params 
        user = auth.authenticate(**auth_params) 
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    
    f = AadhaarAuthForm() 
    return render_to_response('auth.html',
                              {'state':state, 'form': f},
                              context_instance=RequestContext(request))
