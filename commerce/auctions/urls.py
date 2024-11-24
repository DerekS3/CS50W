from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user/<str:listing_owner>", views.user_listings, name="user_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>/", views.category_listings, name="category_listings"),
    path("listing/<int:listing_id>/", views.listing_view, name="listing_view"),
    path("listing/<int:listing_id>/bid/", views.submit_bid, name="submit_bid"),
    path("listing/<int:listing_id>/comment/", views.add_comment, name="add_comment"),
    path("listing/<int:listing_id>/update_watchlist/", views.update_watchlist, name="update_watchlist"),
    path("listing/<int:listing_id>/end_listing/", views.end_listing, name="end_listing"),
]
