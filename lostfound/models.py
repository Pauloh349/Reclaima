from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
import os
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


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
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='items/thumbs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    claimed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.location})"
    
    def get_category_display(self):
        """Get category name for display"""
        if self.category:
            return self.category.name
        return "Uncategorized"


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
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='items/thumbs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    claimed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} (found at {self.location})"
    
    def get_category_display(self):
        """Get category name for display"""
        if self.category:
            return self.category.name
        return "Uncategorized"


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
    image = models.ImageField(upload_to='success_stories/', blank=True, null=True)
    item_url = models.URLField(blank=True, null=True)  # Link to the original item
    image_url = models.URLField(blank=True, null=True)  # Alternative image URL
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
        """Get the display name for the category"""
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)


def make_thumbnail(image_field, size=(300, 300)):
    try:
        img = Image.open(image_field)
        img = img.convert('RGB')
    except Exception:
        return None
    
    # Pillow 10+ removed ANTIALIAS constant; use Resampling.LANCZOS when available
    try:
        resample = Image.Resampling.LANCZOS
    except Exception:
        # fallback for older Pillow versions
        resample = getattr(Image, 'LANCZOS', getattr(Image, 'ANTIALIAS', 1))

    img.thumbnail(size, resample)
    thumb_io = BytesIO()
    img.save(thumb_io, format='JPEG', quality=85)
    return ContentFile(thumb_io.getvalue())


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=LostItem)
def create_lostitem_thumbnail(sender, instance, created, **kwargs):
    if instance.image and (not instance.thumbnail):
        thumb_content = make_thumbnail(instance.image, size=(400, 300))
        if thumb_content:
            base, ext = os.path.splitext(os.path.basename(instance.image.name))
            thumb_name = f"{base}_thumb.jpg"
            instance.thumbnail.save(thumb_name, thumb_content, save=False)
            instance.save()
    
    # Update claimed_at timestamp when status changes to claimed
    if instance.status == 'claimed' and not instance.claimed_at:
        instance.claimed_at = timezone.now()
        instance.save(update_fields=['claimed_at'])


@receiver(post_save, sender=FoundItem)
def create_founditem_thumbnail(sender, instance, created, **kwargs):
    if instance.image and (not instance.thumbnail):
        thumb_content = make_thumbnail(instance.image, size=(400, 300))
        if thumb_content:
            base, ext = os.path.splitext(os.path.basename(instance.image.name))
            thumb_name = f"{base}_thumb.jpg"
            instance.thumbnail.save(thumb_name, thumb_content, save=False)
            instance.save()
    
    # Update claimed_at timestamp when status changes to claimed
    if instance.status == 'claimed' and not instance.claimed_at:
        instance.claimed_at = timezone.now()
        instance.save(update_fields=['claimed_at'])


@receiver(post_save, sender=SuccessStory)
def create_successstory_thumbnail(sender, instance, created, **kwargs):
    """Create thumbnail for success story images"""
    if instance.image and (not instance.image_url):
        thumb_content = make_thumbnail(instance.image, size=(400, 300))
        if thumb_content:
            base, ext = os.path.splitext(os.path.basename(instance.image.name))
            thumb_name = f"{base}_thumb.jpg"
            # You might want to save thumbnail in a different way
            # For now, we'll just ensure the main image is properly processed
            pass