from django.contrib import admin
from django.urls import path, include
from . import views
from uploadingg.views import myprojects
# from uploadingg.views import removeitem
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('', views.home, name="home"),
    path('',views.loginPage, name="login"),
    path('home', views.home, name="home"),
    path('index', views.index, name="index"),

    # path('login', views.login, name="login"),
    path('postlogin', views.postlogin, name="postlogin"),
    path('logout', views.logoutUser, name="logout"),

    path('camera', views.camera, name="camera"),
    path('upload', views.upload, name="upload"),

    path('card_question', views.card_question, name="card_question"),
    

    path('card/',views.card_list, name="card_list"),
    path('card/upload/', views.upload_card, name="upload_card"), 
    path('card/<int:pk>/', views.delete_card, name='delete_card'),
    # path('project/<int:pk>/', views.delete_project, name='delete_project'),

    path('classcard/',views.CardListView.as_view(), name="class_card_list"),

    path('base', views.base, name="base"),
    path('myprojects',views.myprojects, name="myprojects"),
    path('delete_myprojects/<int:pk>/', views.delete_project, name='delete_project'),
    path('myprojects/<int:id>',views.myprojects_details, name="myproject_details"),
    path('myprojects/<int:id>/add',views.addtheproject, name="addtheproject"),
    path('myprojects/<int:id>/quest',views.questtheproject, name="questtheproject"),

    # C:\Users\leon\Desktop\Project\Upload\templates\uploadd\upload.html
    
    # path('mylist/<int:id>', removeitem),
# alt trial
    path('trial',views.trial, name="trial"),
    path('hower',views.hower, name="hower"),
    path('modalpopup',views.modalpopup, name="modalpopup"),
    path('modalpopup2',views.modalpopup2, name="modalpopup2"),
    path('glowunder',views.glowunder, name="glowunder"),
    path('altupload', views.altupload, name="altupload"),
    path('modal', views.modal, name="modal"),
    path('multiple', views.mutliple, name="multiple"),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)