from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Comment


@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        print(f'{sender.__name__} created with ID: {instance.id}, author ID: {instance.author.id}')


# Сигнал при удалении экземпляра Comment
@receiver(post_delete, sender=Comment)
def comment_deleted(sender, instance, **kwargs):
    print(f'{sender.__name__} deleted with ID: {instance.id} deleted, author ID: {instance.author.id}')
