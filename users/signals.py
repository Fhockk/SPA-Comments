from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict

from .models import User


# Сигнал при создании экземпляра User
@receiver(post_save, sender=User)
def comment_created(sender, instance, created, **kwargs):
    if created:
        print(f'{sender.__name__} {instance.username} created with ID: {instance.id}')


# Сигнал при обновлении экземпляра User
@receiver(pre_save, sender=User)
def user_updated(sender, instance, **kwargs):
    try:
        orig = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Если объекта не существует, значит, он только что создан.
        return
    else:
        orig_dict = model_to_dict(orig)
        instance_dict = model_to_dict(instance)
        changes = {f: (orig_dict.get(f), instance_dict.get(f)) for f in orig_dict.keys() if
                   orig_dict.get(f) != instance_dict.get(f)}
        if changes:
            print(f'{sender.__name__} {instance.username} with ID: {instance.id} has these changes {changes}')


# Сигнал при удалении экземпляра User
@receiver(post_delete, sender=User)
def user_deleted(sender, instance, **kwargs):
    print(f'{sender.__name__} {instance.username} with ID: {instance.id} deleted')
