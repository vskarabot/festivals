from django.urls import path, include
from api import views

urlpatterns = [
    path('countries/', views.countries),
    path('festivals/', views.FestivalList.as_view()),
    path('festivals/<int:pk>', views.FestivalDetail.as_view()),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>', views.PostDetail.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
] 
