from django.db import models

class User(models.Model):
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=45)

    def __str__(self):
        return self.username

class Category(models.Model):
    category_name = models.CharField(max_length=45)

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    brand_name = models.CharField(max_length=45)

    def __str__(self):
        return self.brand_name

class Color(models.Model):
    color_name = models.CharField(max_length=45)

    def __str__(self):
        return self.color_name

class Product(models.Model):
    image = models.ImageField(upload_to='product/')
    product_name = models.CharField(max_length=45)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    session_key = models.CharField(max_length=40, default='default_session_key') 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.product_name} x {self.quantity}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=45)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Item {self.product.product_name} in order {self.order.id}'

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.CharField(max_length=255)
    review_date = models.DateTimeField()

    def __str__(self):
        return f'Review {self.id} for {self.product.product_name} by {self.user.username}'

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5')
