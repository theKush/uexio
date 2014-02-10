from django.db import models
from django.contrib.auth.models import User

# COMMENT DATE: 3-3-14
# The model gives instruction to the database on how it should be stored
# The way the models work are as follows: the 'ForeignKey' designator in the first model attribute
# establishes the relationship, 'ForeignKey' represents a many-to-one relationship, so
# the Product model has a many to one relationship with the User model, which makes it possible
# to reference the user and create joins, bindings, etc. If you need a many-to-many relationship,
# you simply designate it with a ManyToManyField (as I did in the category model), so below categories
# have many products, and vice versa
class Product(models.Model):
	user = models.ForeignKey(User, null=True, blank=True)
	title = models.CharField(max_length=180)
	description = models.CharField(max_length=500)
	price = models.DecimalField(max_digits=20, decimal_places=2)
	sale_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
	slug = models.SlugField()
	order = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return str(self.title)

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

class Category(models.Model):
	products = models.ManyToManyField(Product)
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

