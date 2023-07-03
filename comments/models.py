import os
import uuid

from django.db import models

from users.models import User


def generate_unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('images/', filename)


class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='comments')
    home_page = models.URLField(
        blank=True, null=True, verbose_name='Home page'
    )
    content = models.TextField(
        blank=False, null=False, verbose_name='Comment body'
    )
    image = models.ImageField(upload_to=generate_unique_filename, blank=True, null=True)
    text_file = models.FileField(upload_to=generate_unique_filename, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='replies')
