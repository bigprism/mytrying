from django.shortcuts import render

from .models import Post

from django.shortcuts import render, redirect

from .forms import PostCreateForm

from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostEditForm

from django.shortcuts import redirect, get_object_or_404

from .models import Post, Like

from .models import Post, Comment

from .forms import CommentForm

from .models import User, Follow

from django.shortcuts import render, get_object_or_404

from .models import User, Post


def home_view(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'home.html', context)


def post_detail_view(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post
    }
    return render(request, 'post_detail.html', context)


def post_create_view(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostCreateForm()
    context = {
        'form': form
    }
    return render(request, 'post_create.html', context)


def post_edit_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostEditForm(instance=post)
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'post_edit.html', context)


def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('home')


def like_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if created:
        post.likes += 1
        post.save()
    else:
        like.delete()
        post.likes -= 1
        post.save()
    return redirect('home')


def comment_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'comment.html', context)


def follow_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    Follow.objects.get_or_create(follower=request.user, followed=user)
    return redirect('home')


def unfollow_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    Follow.objects.filter(follower=request.user, followed=user).delete()
    return redirect('home')


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    context = {
        'user': user,
        'posts': posts
    }
    return render(request, 'profile.html', context)