from django.db import models
from users.models import User

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        users = ", ".join([user.username for user in self.participants.all()])
        return f"Conversation between {users}"
    
    def get_other_user(self, current_user):
        return self.participants.exclude(pk=current_user.pk).first()
    
    def last_message(self):
        return self.messages.order_by('-created_at').first()
    
    class Meta:
        ordering = ['-updated_at']

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"
    
    class Meta:
        ordering = ['created_at']
