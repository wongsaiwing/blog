from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # comment
    path('post-comment/<int:post_id>/', views.post_comment, name='post_comment'),
]