from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import create_cv, share_cv_email,cv_list

urlpatterns = [
    path('', cv_list, name='cv_list'),  # List all CVs
    path('create/', create_cv, name='create_cv'),
    path('share/email/<int:cv_id>/', share_cv_email, name='share_cv_email'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
