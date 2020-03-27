from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PostForm
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import markdown
# Create your views here.

def post_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    # search using Q :
    if search:
        if order == 'total_views':
            
            post_list = Post.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            post_list = Post.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # clear history
        search = ''
        if order == 'total_views':
            post_list = Post.objects.all().order_by('-total_views')
        else:
            post_list = Post.objects.all()

    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = { 'posts': posts, 'order': order, 'search': search }
    
    return render(request, 'post/list.html', context)

def post_detail(request, id):
    ## id = Primary Key
    post = Post.objects.get(id=id)
    post.total_views += 1
    post.save(update_fields=['total_views'])

    ## translate markdown to html 
    post.body = markdown.markdown(post.body, extentions=[
        # offical Extra Extensions:
        'markdown.extensions.extra', 
        'markdown.extensions.codehilite',
        'markdown.extensions.TOC',
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
@login_required(login_url='/userprofile/login/')
def post_update(request, id):
        # using POST 
        # enter oroginal form by GET 
        # redirect to the modified psot 

    post=Post.objects.get(id=id)
    if request.user != post.author:
        return HttpResponse("You can't edit this post") 

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
