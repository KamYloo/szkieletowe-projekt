"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("cez.urls")),
    path("", include("chat.urls")),
    path("login/", auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path("register/", user_views.register, name="register-users"),
    path('profile/', user_views.profile, name='profile'),
    path('degrees/', user_views.degrees, name='degrees'),
    path('degrees/<int:course_id>/', user_views.degrees_course, name='degrees_course'),
    path('update-profile/', user_views.update_profile, name='update-profile'),
    path("logout/", auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path("admin/", admin.site.urls),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', user_views.activate, name='activate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

