import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import *
from .models import *


def index(request):

    all_posts = Post.objects.all().order_by('-timestamp')

    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html",{
        'new_post': PostForm(),
        'page_obj': page_obj
    })
@csrf_exempt
@login_required
def follow(request, target_id):

    user=request.user
    # Query for requested post
    try:
        target = User.objects.get(pk=target_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

        # Return post contents
    if request.method == "GET":
        return JsonResponse({
            "following_count": target.following.count(),
            "followers_count": target.followers.count()
            })

    # Edit the post text
    if request.method == "PUT" and  not user == target:
        data = json.loads(request.body)

        if data.get("follow") is True and not user in target.followers.all():
            target.followers.add(user)

        if data.get("follow") is False and user in target.followers.all():
            target.followers.remove(user)

        target.save()

        return HttpResponse(status=204)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def edit_post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    

    # Edit the post text
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("text") is not None and request.user==post.poster:
            post.text = (data["text"])

        if data.get("like") is True and not request.user in post.likers.all():
            post.likes +=1
            post.likers.add(request.user)

        if data.get("unlike") is True and request.user in post.likers.all():
            post.likes -=1
            post.likers.remove(request.user)

        post.save()

        return HttpResponse(status=204)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@login_required
def following(request):

    following = request.user.following.all()
    all_posts = Post.objects.filter(poster__in=following).order_by('-timestamp')

    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html",{
        'new_post': PostForm(),
        #'all_posts':all_posts
        'page_obj': page_obj
    })

@login_required
def new_post(request):

    new_post = request.POST["new_post_text"]

    if new_post != '':
        n = Post(
            text=new_post, 
            poster=request.user
        )
        n.save()

    return HttpResponseRedirect(reverse("index"))

@login_required
def profile(request, target):

    profile = User.objects.filter(username=target).first()
    profile_posts = Post.objects.filter(poster=profile).order_by('-timestamp')
    following_count = profile.following.count()
    followers_count = profile.followers.count()
    following = profile in request.user.following.all()

    paginator = Paginator(profile_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html",{
        'profile': profile,
        #'profile_posts': profile_posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'following': following,
        'page_obj': page_obj
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

