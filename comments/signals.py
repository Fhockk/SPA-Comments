from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.forms.models import model_to_dict

from .models import Comment


@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        print(f'{sender.__name__} created with ID: {instance.id}, author ID: {instance.author.id}')


# Сигнал при обновлении экземпляра Comment
@receiver(pre_save, sender=Comment)
def comment_updated(sender, instance, **kwargs):
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
            print(f'{sender.__name__} updated with ID: {instance.id}, author ID: {instance.author.id},' +
                  f' has these changes {changes}')


# Сигнал при удалении экземпляра Comment
@receiver(post_delete, sender=Comment)
def comment_deleted(sender, instance, **kwargs):
    print(f'{sender.__name__} deleted with ID: {instance.id} deleted, author ID: {instance.author.id}')
