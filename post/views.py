from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PostForm
from .models import Post
from .models import PostColumn
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment
import markdown
# Create your views here.

def post_list(request):

    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    post_list = Post.objects.all()

    if search:
        post_list = post_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    if tag and tag != 'None':
        post_list = post_list.filter(tags__name__in=[tag])

    if order == 'total_views':
        post_list = post_list.order_by('-total_views')

    if column is not None and column.isdigit():
        post_list = post_list.filter(column=column)

    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)


    context = {
        'posts': posts,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }
    
    return render(request, 'post/list.html', context)
def post_detail(request, id):
    ## id = Primary Key
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=id)
    post.total_views += 1
    post.save(update_fields=['total_views'])

    ## translate markdown to html 
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.toc',
        'markdown.extensions.codehilite',
    ])
    post.body = md.convert(post.body)
    context = { 'post': post, 'toc': md.toc, 'comments': comments }
    return render(request, 'post/detail.html', context)

@login_required(login_url='/userprofile/login/')
def post_create(request):
    # determine whether the user want to publish a post
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = User.objects.get(id=request.user.id)
            new_post.save()
            # many to many relationship
            post_form.save_m2m()
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

            if request.POST['column'] != 'none':
                post.column = PostColumn.objects.get(id=request.POST['column'])
            else:
                post.column = None

            post.save()
            return redirect("post:post_detail", id=id)
        else:
            columns = PostColumn.objects.all()
            context = { 
            'post': post, 
            'post_form': post_form,
            'columns': columns,
        }
            return HttpResponse("Invalid content, please edit again")
    else:
        post_form = PostForm()
        context = {'post': post, 'post_form': post_form}
        return render(request, 'post/update.html', context)
