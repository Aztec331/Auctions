from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName

#this model is the custom bid that user will insert
class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null= True,related_name="user_bid")
    
    def __str__(self):
        return f"{self.user} bidded {self.bid}" 

class Listing(models.Model):
    title= models.CharField(max_length=30)
    description= models.CharField(max_length=300)
    #predefined price that we define at the time of listing on create_listing.html page
    bidding_price= models.ForeignKey(Bid, on_delete=models.CASCADE, blank= True, null= True,related_name="bidding_price")
    imageURL= models.CharField(max_length=300)
    isActive= models.BooleanField(default=True)
    owner= models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null= True,related_name="user")
    category= models.ForeignKey(Category, on_delete=models.CASCADE,blank=True, null=True,related_name="category")
    #the below name is being used in display_watchlist function, careful we use model field name as well as model field's related name 
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingwatchlist")

    def __str__(self):
        return self.title

#put simply- konsa author konsi listing pe kya comment kar raha hai
#author>lisitng>comment
#related name should not repeat between models/classes
class Comment(models.Model):
    author= models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null= True,related_name="user_comment")
    listing= models.ForeignKey(Listing, on_delete=models.CASCADE, blank= True, null= True,related_name="listing_comment")
    comment= models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.author} comment on {self.listing} is {self.comment}"
    
