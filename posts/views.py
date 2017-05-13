from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.base import RedirectView
from .models import Post
from comments.models import Comment
from comments.forms import CommentForm
import json

def index(request, username):
    try:
    	User.objects.get(username=username)
    except:
        # user doesn't exist.
        context = {'username': None}
        return render(request, 'posts/index.html', context)

    user = User.objects.get(username=username)
    context = {'username': user}
    return render(request, 'posts/index.html', context)

def displayPost(request, username, post_number):
    post = Post.objects.get(user=User.objects.get(username=username), id=post_number)
    comments = Comment.objects.filter(post=post)

    # generate or handle comment form.
    if request.method == "POST":
        comment_text = request.POST.get('the_comment')
        comment = Comment(body=comment_text, post=post, user=request.user)
        comment.save()
        user = request.user.username
        num_comments = post.comment_set.count()
        response_data={'comment': str(comment), 'user':user, 'comment_count': num_comments}
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
    	form = CommentForm()

    num_comments = post.comment_set.count()
    context = {
        'post': post,
        'comments':comments,
        'num_comments':num_comments,
        'form': form
    }
    return render(request, 'posts/single_post.html', context)

def archive(request, username=None):
    return render(request, 'posts/archive.html')

class UserRedirectView(RedirectView):
    def get_redirect_url(self, username):
    	return '/%s/posts' % username

def deletePost(request, username, post_number):
    Post.objects.get(user=User.objects.get(username=username), id=post_number).delete()
    return redirect('posts:index', username=username)

