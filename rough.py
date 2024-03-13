from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

# Creating some example data
category = Category.objects.create(name='Electronics')
product1 = Product.objects.create(name='Laptop', category=category)
product2 = Product.objects.create(name='Smartphone', category=category)

# Accessing products related to a category using the related_name 'products'
products_in_category = category.products.all()

# Displaying the products
for product in products_in_category:
    print(product.name)
