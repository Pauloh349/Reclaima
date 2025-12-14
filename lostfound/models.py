from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# ------------------------
# LostItem model
# ------------------------
class LostItem(models.Model):
    STATUS_CHOICES = [
        ("lost", "Lost"),
        ("claimed", "Claimed"),
    ]

    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    date_lost = models.DateField(null=True, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=100, blank=True)
    reporter_name = models.CharField(max_length=120, blank=True)
    reporter_email = models.EmailField(blank=True)
    reporter_phone = models.CharField(max_length=30, blank=True)
    reward = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="lost")
    image = CloudinaryField('image',  blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    claimed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.location})"

    def get_category_display(self):
        return self.category.name if self.category else "Uncategorized"

# ------------------------
# FoundItem model
# ------------------------
class FoundItem(models.Model):
    STATUS_CHOICES = [
        ("unclaimed", "Unclaimed"),
        ("claimed", "Claimed"),
    ]

    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    date_found = models.DateField(null=True, blank=True)
    finder_name = models.CharField(max_length=120, blank=True)
    finder_email = models.EmailField(blank=True)
    finder_phone = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unclaimed")
    image = CloudinaryField('image',folder='found-items', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    claimed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} (found at {self.location})"

    def get_category_display(self):
        return self.category.name if self.category else "Uncategorized"

# ------------------------
# SuccessStory model
# ------------------------
class SuccessStory(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('keys', 'Keys & Access'),
        ('wallets', 'Wallets & Purses'),
        ('documents', 'Documents'),
        ('jewelry', 'Jewelry & Accessories'),
        ('clothing', 'Clothing'),
        ('bags', 'Bags & Luggage'),
        ('pets', 'Pets'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    author_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    image = CloudinaryField('image', folder='success-stories', blank=True, null=True)
    item_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    allow_featured = models.BooleanField(default=False, verbose_name="Allow to be featured")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Success Stories'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
