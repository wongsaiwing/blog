from django.shortcuts import render
from .models import Post
# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    context = { 'posts': posts }
    return render(request, 'post/list.html', context)

def post_detail(request, id):
    ## id = Primary Key
    post = Post.objects.get(id=id)
    context = {'post':post}
    return render(request, 'post/detail.html', context)