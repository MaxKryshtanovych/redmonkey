from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
                  path('/' + settings.TOKEN, views.getMessage, name='gm'),
                  path('/', views.webhook, name='wh'),
                  path('', views.index, name='index'),
                  path('client/', views.client_list, name='client_list'),
                  path('client/<int:pk>/', views.client_detail, name='client_detail'),
                  path('client/create/', views.client_create, name='client_create'),
                  path('client/<int:pk>/edit/', views.client_edit, name='client_edit'),
                  path('employer/', views.employer_list, name='employer_list'),
                  path('employer/<int:pk>/', views.employer_detail, name='employer_detail'),
                  path('employer/create/', views.employer_create, name='employer_create'),
                  path('employer/<int:pk>/edit/', views.employer_edit, name='employer_edit'),
                  path('check/create/', views.check_create, name='check_create'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
