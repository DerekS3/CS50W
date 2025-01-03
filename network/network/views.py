from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Like, Follower


def index(request):
    return render(request, "network/index.html")


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

def posts_view(request):
    return render(request, "network/posts.html")

def user_profile(request):
    return render(request, "network/user.html")

def following_view(request):
    return render(request, "network/following.html")


@csrf_exempt
def posts(request):
    # Handle POST request to create a new post
    if request.method == 'POST':
        data = json.loads(request.body)  # Get the post data from request
        content = data.get('content', '')

        # Validate content
        if content == '':
            return JsonResponse({"error": "Content cannot be empty."}, status=400)

        # Create a new post
        post = Post(author=request.user, content=content)
        post.save()

        return JsonResponse({"message": "Post created successfully."}, status=201)

    # Handle GET request to retrieve posts
    elif request.method == 'GET':
        posts = Post.objects.all().order_by('-created_at')
        posts_data = [post.serialize() for post in posts]
        return JsonResponse(posts_data, safe=False)

    # Handle unsupported methods
    return JsonResponse({"error": "GET or POST method required."}, status=405)