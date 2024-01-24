from django.urls import path
from . import views


urlpatterns = [
    path('search/', views.search),
    path('all/', views.get_latest),
    path('test/', views.test),
    path('verification/<int:_id>/<str:status>/', views.verify),
    path('subscribe/', views.subscribe),
    path('new/', views.new)
]
