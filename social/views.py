from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import SignUpForm, PostForm, CommentForm, ProfileForm
from .models import Post, Like, Follow

def feed(request):
    posts = Post.objects.select_related("author", "author__profile").prefetch_related("likes", "comments__user").all()
    form = PostForm()
    comment_form = CommentForm()
    liked_ids = set()
    following_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(Like.objects.filter(user=request.user).values_list("post_id", flat=True))
        following_ids = set(Follow.objects.filter(follower=request.user).values_list("following_id", flat=True))
    return render(request, "social/feed.html", {
        "posts": posts, "form": form, "comment_form": comment_form,
        "liked_ids": liked_ids, "following_ids": following_ids,
    })

def signup(request):
    if request.user.is_authenticated:
        return redirect("feed")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to Pixlo! Your account is ready.")
            return redirect("feed")
    else:
        form = SignUpForm()
    return render(request, "social/signup.html", {"form": form})

@login_required
def create_post(request):
    if request.method != "POST":
        return redirect("feed")
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Your post is live.")
    else:
        messages.error(request, "Please check your post details and try again.")
    return redirect("feed")

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect(request.POST.get("next") or "feed")

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
    return redirect(request.POST.get("next") or "feed")

def profile(request, username):
    profile_user = get_object_or_404(User.objects.select_related("profile"), username=username)
    posts = profile_user.posts.select_related("author", "author__profile").prefetch_related("likes", "comments__user")
    is_following = request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=profile_user).exists()
    return render(request, "social/profile.html", {
        "profile_user": profile_user, "posts": posts, "is_following": is_following,
        "follower_count": profile_user.follower_links.count(),
        "following_count": profile_user.following_links.count(),
        "post_count": posts.count(),
    })

@login_required
def edit_profile(request):
    profile_obj = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile_obj)
    return render(request, "social/edit_profile.html", {"form": form})

@login_required
@require_POST
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        messages.error(request, "You can't follow yourself.")
        return redirect("profile", username=username)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
    return redirect("profile", username=username)

def search_users(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.filter(username__icontains=query).select_related("profile")[:30] if query else User.objects.none()
    return render(request, "social/search.html", {"query": query, "users": users})
