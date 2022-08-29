"""referal_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import login_view, main_view, signup_view, logout_view, activate, rating_view
from profiles.views import my_recommendations_view 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name="main-view"),
    path('signup/', signup_view, name="signup-view"),
    path('rating/', rating_view, name="rating-view"),
    path('profiles/', my_recommendations_view, name="my-recs-view"),
    path('login/', login_view, name="login-view"),
    path('logout/,', logout_view, name="logout-view"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        activate, name='activate'),    
]
