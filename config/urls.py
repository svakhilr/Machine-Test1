"""
URL configuration for config project.

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
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from users.views import UserProfileViewset
from django.conf.urls.static import static
from django.conf import settings
from useradmin.views import admin_login,users_list

router = DefaultRouter()

router.register("users",UserProfileViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/',include(router.urls)),
    path('custom/admin',admin_login,name='admin-login'),
    path('custom/admin/user/list',users_list,name='users-list')

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
