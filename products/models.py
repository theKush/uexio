from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

def download_loc(instance, filename):
    if instance.user.username:
        return "%s/download/%s" %(instance.user.username, filename)
    else:
        return "%s/download/%s" %("default", filename)

class Category(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.title)

    class Meta:
        # A human-readable name for the object
        verbose_name = "Category"
        # A human-readable name for the object in plural form, if we didn't
        # provide it, Django would automatically just add an 's', which doesn't
        # work well in most cases, so it's best to designate it to ensure it
        # matches in all cases
        verbose_name_plural = "Categories"

class UserPurchase(models.Model):
    user = models.ForeignKey(User)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return unicode(self.id)

# COMMENT DATE: 3-3-14
# The model gives instruction to the database on how it should be stored
# The way the models work are as follows: the 'ForeignKey' designator in the first model attribute
# establishes the relationship, 'ForeignKey' represents a many-to-one relationship, so
# the Product model has a many to one relationship with the User model, which makes it possible
# to reference the user and create joins, bindings, etc. If you need a many-to-many relationship,
# you simply designate it with a ManyToManyField (as I did in the category model), so below categories
# have many products, and vice versa
class Product(models.Model):
    CONDITION_CHOICES = ((1, 'New'), (2, 'Mint'), (3, 'Good'), (4, 'Fair'))
    user = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=180)
    headline = models.CharField(max_length=300, null=True)
    description = models.TextField()
    download = models.FileField(upload_to=download_loc, blank=True, null=True) # this is for testing the order authentication process
    condition = models.IntegerField(choices=CONDITION_CHOICES, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    slug = models.SlugField()
    order = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    isbn_number = models.CharField(max_length=20, null=True, blank=True)
    author = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(Category)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    purchase = models.ForeignKey(UserPurchase, null=True, blank=True)
    sold_for = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __unicode__(self):
        return str(self.title)

    def can_activate(self):
        return self.productimage_set.count() > 0

    @classmethod
    def listing(cls):
        return cls.objects.filter(active=True)

    # COMMENT DATE: 3-3-14
    # This sets up the
    class Meta:
        # The default ordering for the object, for use when obtaining lists of objects:
        # the '-' will return the items in reverse order
        ordering = ['-order']

class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to="products/image/")
    title = models.CharField(max_length=120, null=True, blank=True)
    featured_image = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.title)

class Tag(models.Model):
    product = models.ForeignKey(Product)
    tag = models.CharField(max_length=20)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.tag)

class CategoryImage(models.Model):
    category = models.ForeignKey(Category)
    image = models.ImageField(upload_to="products/image/")
    title = models.CharField(max_length=120, null=True, blank=True)
    featured_image = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.title)

    class Meta:
        # A human-readable name for the object
        verbose_name = "Category Image"
        # A human-readable name for the object in plural form, if we didn't
        # provide it, Django would automatically just add an 's', which doesn't
        # work well in most cases, so it's best to designate it to ensure it
        # matches in all cases
        verbose_name_plural = "Category Images"

class Comment(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User, null=False, blank=False)
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return str(self.content)

class Coupon(models.Model):
    product = models.ForeignKey(Product)
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return str(self.code)
