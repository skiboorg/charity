from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static


admin.site.site_header = "CharityStore"
admin.site.site_title =  "CharityStore администрирование"
admin.site.index_title = "CharityStore администрирование"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('item/', include('item.urls')),
    path('chat/', include('chat.urls')),
    path('user/', include('customuser.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('pages.urls')),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
