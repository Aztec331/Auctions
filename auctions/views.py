from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# Listing here means a particular item with all its details
from .models import User,Category,Listing,Comment,Bid



def index(request):
    #shows all the objects which are active of Listing
    active_listings= Listing.objects.filter(isActive=True)
    #shows all the categories available
    allCategories= Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":active_listings,
        "categories":allCategories
    })

def display_watchlist(request):
    current_user= request.user
    listings= current_user.listingwatchlist.filter(isActive=True)
    active= Listing.objects.filter(isActive=True)
    context={"listings":listings,"active":active}
    return render(request,"auctions/watchlist.html",context)

def your_winnings(request):
    return

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        # Which means the user exists in the database
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
    

def create_listing(request):
    if request.method=="GET":
        #Category is a model and Category.objects.all means all objects of Category class
        allCategories= Category.objects.all()
        return render(request,"auctions/create_listing.html",{
            "categories":allCategories
        })
    else:
        #Get the data from the form
        title= request.POST["title"]
        description= request.POST["description"]
        category= request.POST["category"]
        bidding_price= request.POST["bidding_price"]
        imageURL = request.POST["imageURL"]
        # Who is the user
        current_user= request.user

        #get category name from the form, store it in categoryName of Category model
        #save this data into into categoryData variable and save this variable as 
        #a new category in a new object of Listing class such that
        # category = categoryData
        category_data = Category.objects.get(categoryName= category)

        #Create a new bid object 
        bid= Bid(bid=float(bidding_price), user= current_user)
        bid.save()

        #Create a new listing object
        new_listing= Listing(
            title= title,
            description=description,
            bidding_price= bid,
            imageURL=imageURL,
            category=category_data,
            owner= current_user
        )
        #insert the object in our database
        new_listing.save()
        #Redirect to the index page
        return HttpResponseRedirect(reverse('index'))

def display_category(request):
    if request.method=="POST":
        allCategories= Category.objects.all()
        category_from_form= request.POST['category']
        category= Category.objects.get(categoryName= category_from_form)
        activeListings= Listing.objects.filter(isActive=True, category= category)
        return render(request,"auctions/index.html",{
            "categories":allCategories,
            "listings":activeListings
        })


def listing(request,id):
    listingData= Listing.objects.get(pk=id)
    is_listing_in_watchlist = request.user in listingData.watchlist.all()
    all_comments= Comment.objects.filter(listing=listingData)
    is_owner= request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html",{
        "listing":listingData,
        "is_listing_in_watchlist": is_listing_in_watchlist,
        "all_comments":all_comments,
        "is_owner": is_owner
    })

def add_watchlist(request,id):
    listingData= Listing.objects.get(pk=id)
    current_user= request.user
    #we can use below watchlist field of Listing model because
    #of the many to many relationship
    listingData.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing",args=(id,)))

def remove_watchlist(request,id):
    listingData= Listing.objects.get(pk=id)
    current_user= request.user
    listingData.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing",args=(id,)))

def add_comment(request,id):
    current_user = request.user
    listingData= Listing.objects.get(pk=id)
    message= request.POST['new_comment']

    newComment= Comment(
        author= current_user,
        listing= listingData,
        comment= message
    )

    newComment.save()
    #always remember we add data to models then use .save() on that variable
    return HttpResponseRedirect(reverse("listing",args=(id,)))


def add_bid(request,id):
    '''you can place new bids using this'''
    new_bid= request.POST["new_bid"]
    listingData= Listing.objects.get(pk=id)
    is_listing_in_watchlist = request.user in listingData.watchlist.all()
    all_comments= Comment.objects.filter(listing=listingData)
    is_owner= request.user.username == listingData.owner.username
    if float(new_bid) > listingData.bidding_price.bid:
        updateBid= Bid(user=request.user, bid= float(new_bid))
        updateBid.save()
        listingData.bidding_price = updateBid
        listingData.save()
        context= {"listing":listingData,"message":"Bid updated successfully !","update":True,
                "is_listing_in_watchlist": is_listing_in_watchlist,
                "all_comments":all_comments,"is_owner": is_owner}
        return render(request,"auctions/listing.html",context)

    else:
        context= {"listing":listingData,"message":"Bid should be higher than current price","update":False,
                "is_listing_in_watchlist": is_listing_in_watchlist,
                "all_comments":all_comments,"is_owner": is_owner}
        return render(request,"auctions/listing.html",context)

def close_bid(request,id):
    '''closing bid function'''
    listingData= Listing.objects.get(pk=id)
    listingData.isActive= False
    listingData.save()
    is_listing_in_watchlist = request.user in listingData.watchlist.all()
    all_comments= Comment.objects.filter(listing=listingData)
    is_owner= request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html",{
        "listing":listingData,
        "is_listing_in_watchlist": is_listing_in_watchlist,
        "all_comments":all_comments,
        "is_owner": is_owner,
        "update": True,
        "message": "Congrats ! your auction is closed."
    })
