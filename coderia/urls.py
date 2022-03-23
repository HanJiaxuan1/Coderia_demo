from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('community.urls')),
    path('note', include('note.urls')),
    path('admin/', admin.site.urls),
    path('search/', include('haystack.urls')),
]
