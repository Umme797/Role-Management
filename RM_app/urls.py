from django.urls import path
from RM_app import views
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('department_dashboard/', views.department_dashboard, name='department_dashboard'),

    path('create_role/', views.create_role, name='create_role'),
    path('update_role/<rid>/', views.update_role, name='update_role'),
    path('delete_role/<rid>/', views.delete_role, name='delete_role'),

    path('create_department/', views.create_department, name='create_department'),
    path('update_department/<did>/', views.update_department, name='update_department'),
    path('delete_department/<did>/', views.delete_department, name='delete_department'),

    path('register', views.register, name='register'),
    path('login', views.ulogin, name='ulogin'),
    path('ulogout', views.ulogout, name='ulogout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

