from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # наше приложение core
    path('', include('core.urls')),

    # каталог
    path('catalog/', include('catalog.urls')),
]