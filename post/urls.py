from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('post-list/', views.post_list, name="post_list"),
]
