from django.shortcuts import render, redirect
from profiles.models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import RegisterUserForm, LoginUserForm
from django.core.mail import send_mail
from .token import account_activation_token    
from django.template.loader import render_to_string  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
import operator


def signup_view(request):
    profile_id = request.session.get('ref_profile')
    print('profile_id', profile_id)
    form = RegisterUserForm(request.POST or None)
    if form.is_valid():
        ref_code = form.cleaned_data["referal_code"]
        if profile_id is not None or ref_code != '':
            if profile_id is not None:
                recommended_by_profile = Profile.objects.get(id=profile_id)
            else:
                recommended_by_profile = Profile.objects.get(ref_code=ref_code)

            try:
                instance = form.save(commit=False)
                instance.is_active = False  
                instance.save()
            except:
                latest_obj = User.objects.latest('id')
                latest_obj.delete()
                email = form.cleaned_data['email']
                return render(request, 'exception.html', {'email':email})

            registered_user = User.objects.get(id=instance.id)
            registere_profile = Profile.objects.get(user=registered_user)
            registere_profile.recomended_by = recommended_by_profile.user
            registere_profile.save()
        else:
            objects = Profile.objects.all()
            if len(objects) <= 5:
                try:
                    instance = form.save(commit=False)
                    instance.is_active = False  
                    instance.save()  
                except:
                    latest_obj = User.objects.latest('id')
                    latest_obj.delete()
                    email = form.cleaned_data['email']
                    return render(request, 'exception.html', {'email':email})
            else:
                return HttpResponse('Only first 5 users can register withou referal code.\n Please enter referal code!')  

        current_site = get_current_site(request)  
        mail_subject = 'Activation link has been sent to your email id'  
        message = render_to_string('acc_active_email.html', {  
            'user': instance,  
            'domain': current_site.domain,  
            'uid':urlsafe_base64_encode(force_bytes(instance.pk)),  
            'token':account_activation_token.make_token(instance),  
        })  
        to_email = form.cleaned_data.get('email')  
        mail = send_mail(mail_subject, message, 'redka.maksym@lll.kpi.ua', [to_email], fail_silently=False)
        if mail:  
            return HttpResponse('Please confirm your email address to complete the registration')  
        else:
            return HttpResponse('Oops something goes wrong!')  
        #login(request, instance)

    context = {'form':form}
    return render(request, 'signup.html', context)

def activate(request, uidb64, token):  
    User = Profile  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')  
        return redirect('login.html')
    else:
        messages.success(request, 'Activation link is invalid!.')  
        return redirect('login.html')  

def login_view(request):
    print(request)
    form = LoginUserForm(request.POST or None)
    if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
                if user.is_active:
                    login(request, user)
        
                    return redirect('my-recs-view')
                else:
                    return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')

    context = {'form':form}
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('main-view')

def main_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    
    if request.user.is_authenticated is False:
        
        try:
            profile = Profile.objects.get(ref_code=code)
            request.session['ref_profile'] = profile.id
            
            print('id', profile.id)
        except:
            print("exception")

        print(request.session.get_expiry_date())
        return render(request, 'main.html', {})
    
    else: 
        return redirect('my-recs-view')

def rating_view(request):
    auths = Profile.objects.order_by('-points')[:10]
    return render(request, 'rating.html', {"ordered":auths})
