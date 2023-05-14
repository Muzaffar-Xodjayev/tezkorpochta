from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static
from cargo import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("cargo.urls"))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.error_404