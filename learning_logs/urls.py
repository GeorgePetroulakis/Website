from django.urls import path, include

from . import views 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


app_name = 'learning_logs'
urlpatterns = [
    # Home page
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # Page that shows all topics
    path('topics/', views.topics, name='topics'),
    # Page that shows a single topic and its entries
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    #Page for editing an entry.
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('profile_search/', views.profile_search, name='profile_search'), 
    path('select_topic_to_remove/', views.select_topic_to_remove, name='select_topic_to_remove'),
    path('remove_topic/<int:topic_id>/', views.remove_topic, name='remove_topic'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('edit_profile/<int:user_id>/', views.edit_user_profile, name='edit_user_profile'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
