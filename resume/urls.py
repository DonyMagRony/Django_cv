from django.conf import settings 

from django.conf.urls.static import static 

from django.urls import path 

from .views import share_cv_email 

 

urlpatterns = [ 

    path('share/email/<int:cv_id>/', share_cv_email, name='share_cv_email'), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 