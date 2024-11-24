from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watched_by")


class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(verbose_name='Image URL', blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, null=True)
    current_bid = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.owner}"
    
    def set_current_bid(self):
        self.current_bid = self.starting_bid

    def set_default_image(self):
        if not self.image_url:
            self.image_url = "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg"

    def set_default_category(self):
        if not self.category:
            self.category = "Uncategorised"
    
    def update_current_bid(self, bid_amount):
        self.current_bid = bid_amount
        self.save()

    def get_highest_bidder(self):
        highest_bid = self.bids.order_by('-bid_amount', '-bid_time').first()
        return highest_bid.bidder if highest_bid else None


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} bid {self.bid_amount} on {self.listing}"
    
    def is_valid_bid(self):
        if self.listing.bids.count() == 0:
            return self.bid_amount >= self.listing.current_bid    
        else: 
            return self.bid_amount > self.listing.current_bid


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenter} commented on {self.listing}"