from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from post.models import Post
from .forms import CommentForm

# comment
@login_required(login_url='/userprofile/login/')
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # POST only
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect(post)
        else:
            return HttpResponse("Invalid form, please retry")

    else:
        return HttpResponse("POST only")
