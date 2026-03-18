from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('crops/', views.crop_list, name='crop_list'),
    path('crops/<int:pk>/', views.crop_detail, name='crop_detail'),
    path('crops/add/', views.crop_create, name='crop_create'),
    path('crops/<int:pk>/update/', views.crop_update, name='crop_update'),
    path('crops/<int:pk>/delete/', views.crop_delete, name='crop_delete'),
    
    path('ask-question/', views.ask_question, name='ask_question'),
    path('community-qa/', views.community_qa, name='community_qa'),
    path('query/<int:pk>/', views.question_detail, name='question_detail'),
    path('query/<int:pk>/answer/', views.answer_question, name='answer_question'),
]
