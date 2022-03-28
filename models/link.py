from .base_model import BaseModel
import peewee as pw
from config.settings import db
from .user import User
import datetime

class Link(BaseModel):
    """This class defines the link table."""

    # Describe the status of the link
    # 'active' means the link is in queue and will be started
    # 'inactive' means the link is not in queue and will not be started
    # 'paused' means the link is paused by user
    # 'resumed' means the link is resumed and is downloading
    # 'canceled' means the link is canceled by user
    # 'completed' means the link is completed
    # 'failed' means the link failed to download
    # 'deleted' means the link is deleted by user
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('paused', 'paused'),
        ('resumed', 'resumed'),
        ('canceled', 'canceled'),
        ('completed', 'completed'),
        ('failed', 'failed'),
        ('deleted', 'deleted'),
    )

    user = pw.ForeignKeyField(User, backref='links')
    url = pw.CharField(max_length=255, unique=True)
    # name = pw.CharField(max_length=255)
    # description = pw.TextField()
    # tags = pw.CharField(max_length=255)
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    status = pw.CharField(max_length=255, choices=STATUS_CHOICES, default='active')
    error = pw.TextField(null=True)
    