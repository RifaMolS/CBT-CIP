"""
URL configuration for connectsphere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from sphere import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/',views.register, name='register'),
    path('login/',views.login,name='login'),
    path('homepage/',views.homepage,name='homepage'),
    path('profile/', views.profile_view, name='profile'),
    path('profile_update/', views.update_profile, name='profile_update'),
    path('messages/', views.message_page, name='messages'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('send_message/', views.send_message, name='send_message'),
    path('fetch_messages/<int:user_id>/', views.fetch_messages, name='fetch_messages'),
    path('forgotpassword/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('update_password/', views.update_password, name='update_password'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

]
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
