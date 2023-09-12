
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
  
    path("admin/", admin.site.urls),
    path('auth/v1/',include('authapp.urls')),
    path("social/v1/",include('social.urls'))

]
