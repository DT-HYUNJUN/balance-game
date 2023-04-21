from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-pk')
    page = request.GET.get('page', '1')
    per_page = 6
    paginator = Paginator(posts, per_page)
    last_page = paginator.num_pages
    page_obj = paginator.get_page(page)
    context = {
        'last_page': last_page,
        'posts': page_obj,
    }
    return render(request, 'posts/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            form.save()
            return redirect('posts:index')
            
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/create.html', context)


def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comments = post.comment_set.all()
    User = get_user_model()
    people = User.objects.all()
    comment_form = CommentForm()
    context = {
        'people': people,
        'res1': post.select1_count(),
        'res2': post.select2_count(),
        'comments': comments,
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'posts/detail.html', context)


@login_required
def answer(request, post_pk, answer):
    post = Post.objects.get(pk=post_pk)

    if answer == post.select1_content:
        post.select1_users.add(request.user)
    elif answer == post.select2_content:
        post.select2_users.add(request.user)

    return redirect('posts:detail', post.pk)


def likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:detail', post.pk)


@login_required
def comment_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        form.save()
        return redirect('posts:detail', post_pk)
    detail(request, post_pk)
    

@login_required
def comment_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
    return redirect('posts:detail', post_pk)


@login_required
def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts:detail', post.pk)
        else:
            form = PostForm(instance=post)
    else:
        return redirect('posts:detail', post.pk)
    context = {
        'post' : post,
        'form' : form,
    }
    return render(request, 'posts/update.html', context)


@login_required
def delete(request,post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        post.delete()
    return redirect('posts:index')