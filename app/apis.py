from django.http import JsonResponse

from .models import Post

from .models import Post, Like

from .models import Post, Comment

from .models import User, Follow

from .models import User, Post


def post_list_api(request):
    posts = Post.objects.all()
    data = []
    for post in posts:
        data.append({
            'id': post.id,
            'content': post.content,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'author': post.author.username,
            'likes': post.likes
        })
    return JsonResponse({'posts': data})


def post_detail_api(request, pk):
    post = Post.objects.get(pk=pk)
    data = {
        'id': post.id,
        'content': post.content,
        'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'author': post.author.username,
        'likes': post.likes
    }
    return JsonResponse({'post': data})


def post_create_api(request):
    if request.method == 'POST':
        data = request.POST.dict()
        post = Post.objects.create(**data)
        return JsonResponse({'post': {
            'id': post.id,
            'content': post.content,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'author': post.author.username,
            'likes': post.likes
        }})
    return JsonResponse({'error': 'Invalid request method'})


def post_edit_api(request, pk):
    if request.method == 'PUT':
        data = request.PUT.dict()
        post = Post.objects.get(pk=pk)
        post.content = data['content']
        post.save()
        return JsonResponse({'post': {
            'id': post.id,
            'content': post.content,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'author': post.author.username,
            'likes': post.likes
        }})
    return JsonResponse({'error': 'Invalid request method'})


def post_delete_api(request, pk):
    if request.method == 'DELETE':
        post = Post.objects.get(pk=pk)
        post.delete()
        return JsonResponse({'success': 'Post deleted successfully'})
    return JsonResponse({'error': 'Invalid request method'})


def like_api(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            post.likes += 1
            post.save()
            return JsonResponse({'success': 'Post liked successfully'})
        else:
            like.delete()
            post.likes -= 1
            post.save()
            return JsonResponse({'success': 'Post unliked successfully'})
    return JsonResponse({'error': 'Invalid request method'})


def comment_api(request, pk):
    if request.method == 'POST':
        data = request.POST.dict()
        post = Post.objects.get(pk=pk)
        comment = Comment.objects.create(user=request.user, post=post, content=data['content'])
        return JsonResponse({'comment': {
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': comment.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'author': comment.user.username
        }})
    return JsonResponse({'error': 'Invalid request method'})


def follow_api(request, pk):
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        Follow.objects.get_or_create(follower=request.user, followed=user)
        return JsonResponse({'success': 'User followed successfully'})
    return JsonResponse({'error': 'Invalid request method'})


def unfollow_api(request, pk):
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        Follow.objects.filter(follower=request.user, followed=user).delete()
        return JsonResponse({'success': 'User unfollowed successfully'})
    return JsonResponse({'error': 'Invalid request method'})


def profile_api(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user)
    data = {
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        },
        'posts': [{
            'id': post.id,
            'content': post.content,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'author': post.author.username,
            'likes': post.likes
        } for post in posts]
    }
    return JsonResponse(data)