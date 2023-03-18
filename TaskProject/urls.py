from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('session-auth/', include('rest_framework.urls')),
    path('api/v1/', include('Test.urls')),
    path('token-auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
]
