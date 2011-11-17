from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.models import User

def login_user(request):
    state = "Please log in below..."
    
    # Whats in DB? 
    users = User.objects.all() 
    print "All users = ", users 

    username = password = ''
    if request.POST:
        print request.POST 
        

        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print type(request.POST) 

        #user = authenticate(username=username, password=password)
        user = authenticate(username=username, password=password,
                            aadhaar_id=request.POST.get('aadhaar_id'))
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('auth.html',
                              {'state':state, 'username': username},
                              context_instance=RequestContext(request))
