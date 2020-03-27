from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PostForm
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import markdown
# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    context = { 'posts': posts }
    return render(request, 'post/list.html', context)

def post_detail(request, id):
    ## id = Primary Key
    post = Post.objects.get(id=id)

    ## translate markdown to html 
    post.body = markdown.markdown(post.body, extentions=[
        # offical Extra Extensions:
        'markdown.extensions.extra', 
    ])

    context = {'post':post}
    return render(request, 'post/detail.html', context)

@login_required(login_url='/userprofile/login/')
def post_create(request):
    # determine whether the user want to publish a post
    if request.method == "POST":
        post_form = PostForm(data=request.POST)

        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = User.objects.get(id=request.user.id)
            new_post.save()
            return redirect("post:post_list")
        else:
            return HttpResponse("Invalid content, please edit again")

    # if the user not going to publish a post
    else:
        post_form=PostForm()
        context = {'post_post': post_form}

        return render(request, 'post/create.html', context)

def post_delete(request, id):
    # delete post by its id
    # then back to the post list
    post = Post.objects.get(id=id)
    post.delete()
    return redirect("post:post_list")

    # update a post
def post_update(request, id):
        # using POST 
        # enter oroginal form by GET 
        # redirect to the modified psot 

    post=Post.objects.get(id=id)

    if request.method == "POST":
        post_form = PostForm(data=request.POST)

        if post_form.is_valid():
            # overwrite the original context
            post.title = request.POST['title']
            post.body = request.POST['body']
            post.save()
            return redirect("post:post_detail", id=id)
        else:
            return HttpResponse("Invalid content, please edit again")
    else:
        post_form = PostForm()
        context = {'post': post, 'post_form': post_form}
        return render(request, 'post/update.html', context)
