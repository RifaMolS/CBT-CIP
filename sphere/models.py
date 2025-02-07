from django.db import models

# Create your models here.
class registration(models.Model):
    username = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    confirmpassword = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=15, null=True, blank=True) 
    address = models.TextField(null=True, blank=True) 
    bio = models.TextField(null=True, blank=True) 
    profilepic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    class Meta:
        db_table = 'sphere_registration'  

    def _str_(self):
        return self.username
class Post(models.Model):
    user = models.ForeignKey(registration, on_delete=models.CASCADE)  # Link post to the user who created it
    content = models.TextField()  # Post content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the post is created

    class Meta:
        db_table = 'posts'  # Create a table named 'posts'

    def _str_(self):
        return f"Post by {self.user.username} at {self.created_at}"


class Like(models.Model):
    user = models.ForeignKey(registration, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'
        unique_together = ('user', 'post')  # Ensure each user can only like a post once

    def _str_(self):
        return f"{self.user.username} liked {self.post}"


class Comment(models.Model):
    user = models.ForeignKey(registration, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'

    def _str_(self):
        return f"Comment by {self.user.username} on {self.post}"
class Message(models.Model):
    sender = models.ForeignKey(registration, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(registration, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sphere_message'

    def _str_(self):
        return f"{self.sender.name} -> {self.receiver.name}: {self.content[:30]}"