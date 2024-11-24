from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .forms import ListingForm, BidForm, CommentForm
from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.filter(is_active=True).order_by('-created_at') 
    return render(request, "auctions/index.html", {
        "title": "Active Listings",
        "listings": listings,
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.set_current_bid()
            listing.set_default_image()
            listing.set_default_category()
            listing.save()
            return HttpResponseRedirect(reverse("listing_view", args=[listing.id]))
    else:
        form = ListingForm()
        return render(request, "auctions/create.html", {
            'form': form
        })


def listing_view(request, listing_id):
    # Ensure user is navigating to a valid listing
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/error.html", {
            "error": "Listing not found"
            })
    
    bid_form = BidForm()
    bid_count = Bid.objects.filter(listing=listing).count()
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=listing).all()
    comment_count = Comment.objects.filter(listing=listing).count()
    is_active = listing.is_active

    # Check if current user is owner, highest bidder or watching
    is_highest_bidder = False
    is_watching = False
    is_owner = False
    if request.user.is_authenticated:
        highest_bidder = listing.get_highest_bidder()
        is_highest_bidder = (request.user == highest_bidder)
        is_watching = listing in request.user.watchlist.all()
        is_owner = (request.user == listing.owner)

    return render(request, "auctions/listing.html", {
        'listing': listing,
        'bid_form': bid_form,
        'bid_count': bid_count,
        'comment_form': comment_form,
        'comments': comments,
        'comment_count': comment_count,
        'is_active': is_active,
        'is_highest_bidder': is_highest_bidder,
        'is_watching': is_watching,
        'is_owner': is_owner,
        })


@login_required    
def submit_bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        bid_form = BidForm(request.POST)

        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.listing = listing
            bid.bidder = request.user

            if bid.is_valid_bid():
                listing.update_current_bid(bid.bid_amount)
                bid.save()
                messages.success(request, 'Your bid was successfully placed!')
            else:
                messages.error(request, 'Bid too low. Please increase your bid.')
    else:
        messages.error(request, 'Bid failed. Please try again.')
    return HttpResponseRedirect(reverse("listing_view", args=[listing.id]))


@login_required
def add_comment(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.listing = listing
            new_comment.commenter = request.user
            new_comment.save()
    return HttpResponseRedirect(reverse("listing_view", args=[listing.id]))


def categories(request):
    categories = Listing.objects.values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_listings(request, category):
    listings = Listing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/index.html", {
        "title": category,
        "listings": listings,
    })


def user_listings(request, listing_owner):
    try:
        owner = User.objects.get(username=listing_owner)
        listings = Listing.objects.filter(owner=owner)
        return render(request, "auctions/index.html", {
            "title": listing_owner,
            "listings": listings,
        })
    except User.DoesNotExist:
        return render(request, "auctions/error.html", {
            "error": "User not found"
        })


@login_required
def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/index.html", {
        "title": "Watchlist",
        "listings": listings,
    })


@login_required
def update_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        is_watching = request.user.watchlist.filter(id=listing_id).exists()
        if is_watching:
            request.user.watchlist.remove(listing)
        else:
            request.user.watchlist.add(listing)
    return HttpResponseRedirect(reverse("listing_view", args=[listing.id]))


@login_required
def end_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        listing.is_active = False
        listing.save()
    return HttpResponseRedirect(reverse("listing_view", args=[listing.id]))