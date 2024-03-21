from django.db.models.signals import pre_delete
from django.dispatch import receiver

from server.models import Category


@receiver(pre_delete, sender=Category)
def delete_category_icon_file(sender, **kwargs):
    """
    When a category gets deleted we aso delete the icon that was stored in
    the media root.
    """
    if kwargs["instance"].icon:
        kwargs["instance"].icon.delete(save=False)
