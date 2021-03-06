"""stitchit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from stitchitapi.models import *
from stitchitapi.views import Fabrics, Sizes, Designs, Follows, Stitchers, Users
from stitchitapi.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'fabrics', Fabrics, 'fabric')
router.register(r'sizes', Sizes, 'size')
router.register(r'designs', Designs, 'design')
router.register(r'follows', Follows, 'follow')
router.register(r'stitchers', Stitchers, 'stitcher')
router.register(r'users', Users, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user),
    path('login/', login_user),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)