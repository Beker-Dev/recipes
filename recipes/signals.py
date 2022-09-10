from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Recipe
import os


def delete_cover(recipe):
    try:
        os.remove(recipe.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(instance, *args, **kwargs):
    delete_cover(instance)


@receiver(pre_save, sender=Recipe)
def recipe_cover_update(instance, *args, **kwargs):
    try:
        old_instance = Recipe.objects.get(pk=instance.pk)
    except Recipe.DoesNotExist:
        return
    else:
        is_new_cover = old_instance.cover != instance.cover

        if is_new_cover:
            delete_cover(old_instance)
