from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.db.models import Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from tag.models import Tag
import os
from django.conf import settings
from PIL import Image


class RecipeManager(models.Manager):
    def get_all_published_and_author_full_name(self):
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '), F('author__last_name')
            )
        ).order_by('-id').select_related('category', 'author').prefetch_related('tags')


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65, unique=True)
    description = models.CharField(max_length=165,)
    slug = models.SlugField(unique=True)
    preparation_time_unit = models.CharField(max_length=65)
    preparation_time = models.IntegerField()
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:detail', args=(self.id,))

    @staticmethod
    def resize_image(image, new_width=840):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return
        else:
            new_height = int(new_width * original_height / original_width)
            new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
            new_image.save(
                image_full_path,
                optimize=True,
                quality=50,
            )
            new_image.close()
            image.close()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        if self.cover:
            self.resize_image(self.cover)

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
