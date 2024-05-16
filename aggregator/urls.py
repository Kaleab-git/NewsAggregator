from django.urls import path
from . import views


urlpatterns = [
    path('search/', views.search),
    path('test/', views.test),
    path('verification/<int:_id>/<str:status>/', views.verify),
    path('subscribe/', views.subscribe),
]
