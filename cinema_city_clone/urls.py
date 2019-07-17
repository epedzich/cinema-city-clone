"""cinema_city_clone URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from rest_framework import authentication, permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from cinemas_repertoire.rest_views import EventsViewset

router = routers.DefaultRouter()
router.register(r'movies', EventsViewset, basename='movies')

schema_view = get_schema_view(
    openapi.Info(
        title="Cinema City Clone API",
        default_version='v1',
        description="API documentation for Cinema City Clone",
    ),
    validators=['flex', 'ssv'],
    public=False,
    permission_classes=(permissions.IsAdminUser,),
    authentication_classes=(authentication.TokenAuthentication,
                            authentication.SessionAuthentication),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cinemas_repertoire.urls', 'repertoire')),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    path('api/', include(router.urls)),
]
