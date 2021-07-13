from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Message(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.message,
            "receiver": [user.message for user in self.receiver.all()],
            "message": self.message,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "is_read": self.is_read,
        }
