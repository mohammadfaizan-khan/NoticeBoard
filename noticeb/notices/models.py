from django.db import models

# Create your models here.

from django.conf import settings

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_at']  #
        
    def __str__(self):
        return self.title
    
    def can_edit(self, user):
        return user == self.author or user.is_admin()