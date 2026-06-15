from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),

    # Старый адрес оставляем рабочим, чтобы не сломать существующие ссылки.
    path('catalog/', include('catalog.urls')),

    # Новый основной адрес ZPT Market.
    path('market/', include('catalog.urls')),

    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {
            'document_root': settings.MEDIA_ROOT,
        }
    ),
]