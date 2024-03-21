from django.db.models.signals import pre_delete
from django.dispatch import receiver

from server.models import Channel


@receiver(pre_delete, sender=Channel)
def delete_channel_icon_banner_file(sender, **kwargs):
    """
    When a channel gets deleted we aso delete the icon and the banner
    that was stored in the media root.
    """
    if kwargs["instance"].icon:
        kwargs["instance"].icon.delete(save=False)
    if kwargs["instance"].banner:
        kwargs["instance"].banner.delete(save=False)
