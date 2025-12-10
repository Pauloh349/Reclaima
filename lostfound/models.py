from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
import os


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

	def __str__(self):
		return f"{self.title} ({self.location})"


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

	def __str__(self):
		return f"{self.title} (found at {self.location})"


class SuccessStory(models.Model):
	title = models.CharField(max_length=200)
	author_name = models.CharField(max_length=120, blank=True)
	content = models.TextField()
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
	# store a simple link back to the related item and an image url for small thumbnails
	item_url = models.CharField(max_length=500, blank=True)
	image_url = models.CharField(max_length=500, blank=True)
	created_at = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.title


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


@receiver(post_save, sender=FoundItem)
def create_founditem_thumbnail(sender, instance, created, **kwargs):
	if instance.image and (not instance.thumbnail):
		thumb_content = make_thumbnail(instance.image, size=(400, 300))
		if thumb_content:
			base, ext = os.path.splitext(os.path.basename(instance.image.name))
			thumb_name = f"{base}_thumb.jpg"
			instance.thumbnail.save(thumb_name, thumb_content, save=False)
			instance.save()

