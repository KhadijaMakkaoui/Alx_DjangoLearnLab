from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(actor, verb, target):
    target_content_type = ContentType.objects.get_for_model(target.__class__)
    Notification.objects.create(
        actor=actor,
        verb=verb,
        target_object_id=target.id,
        target_content_type=target_content_type,
        recipient=target.author  # Assuming the target has an author field
    )
