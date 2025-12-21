from django.urls import path
from . import views
urlpatterns = [
    #authenticaion
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    #CRUD
    path('upload_photo/',views.upload_photo,name = 'upload_photo'),
    path('list_photos/',views.list_photos,name = 'list_photos'),
    path('view_photo/<int:photo_id>/',views.view_photo,name = 'view_photo'),
    path('public_photo/<int:photo_id>/',views.public_photo,name = 'public_photo'),
    path('all_public_photos/',views.all_public_photos, name = 'all_public_photos'),
    path('delete_photo/<int:photo_id>/',views.delete_photo,name='delete_photo'),
]
