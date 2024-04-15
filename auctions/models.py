from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName
    
class Listing(models.Model):
    title= models.CharField(max_length=30)
    description= models.CharField(max_length=300)
    bidding_price= models.FloatField(null=True)
    imageURL= models.CharField(max_length=300)
    isActive= models.BooleanField(default=True)
    owner= models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null= True,related_name="owner")
    category= models.ForeignKey(Category, on_delete=models.CASCADE,blank=True, null=True,related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingwatchlist")
    winner =  models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null= True,related_name="winner")

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    offered_price= models.FloatField(null=True)
    listing_id=models.ForeignKey(Listing,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null= True,related_name="user_bid")
    
    def __str__(self):
        return f"{self.user} bidded {self.bid}" 



#put simply- konsa author konsi listing pe kya comment kar raha hai
#author>lisitng>comment
#related name should not repeat between models/classes
class Comment(models.Model):
    author= models.ForeignKey(User, on_delete=models.CASCADE, blank= True, null= True,related_name="user_comment")
    listing= models.ForeignKey(Listing, on_delete=models.CASCADE, blank= True, null= True,related_name="listing_comment")
    comment= models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.author} comment on {self.listing} is {self.comment}"


    