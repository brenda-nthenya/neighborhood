from . import views
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name= 'index'),
    path('register/', views.register, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('search_business/(\d+)',views.search_results,name='search_results'),
    path('edit_profile/<int:profile_id', views.edit_profile, name='edit_profile'),
    path('new_business/', views.new_business, name='new_business'),
    path('new_post/', views.new_post, name='new_post'),
    path('create_hood/', views.create_hood, name='create_hood'),
    # path('my_hood/', views.my_hood, name='my_hood'),
    path('all_works/', views.all_works, name='all_works'),
    path('all_posts/', views.all_posts, name='all_posts'),
]   


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)