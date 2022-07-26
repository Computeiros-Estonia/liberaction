from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from  liberaction import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('liberaction.core.urls')),
    path('users/', include('liberaction.users.urls')),
    path('basket/', include('liberaction.basket.urls')),
    path('sales/', include('liberaction.sales.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
