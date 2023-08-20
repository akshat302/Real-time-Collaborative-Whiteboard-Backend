import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class WhiteBoard(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=64, blank=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserBoardInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    board = models.ForeignKey(WhiteBoard, on_delete=models.CASCADE, to_field='uuid')
    action = models.CharField(max_length=32, blank=False)
    undo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
