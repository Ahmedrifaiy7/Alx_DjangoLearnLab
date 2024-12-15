from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # This is a ManyToMany relationship with itself to represent followers and following
    following = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='followers', 
        through='UserFollow', 
        blank=True
    )

class UserFollow(models.Model):
    # This model stores the relationship between the follower and the followed user
    follower = models.ForeignKey(CustomUser, related_name='following_set', on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser, related_name='followers_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure that a user can only follow another user once
        unique_together = ('follower', 'followed')
