from django.db import models
from utils.models import TimeStampModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(TimeStampModel):
    content = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} post{self.id}"

    class Meta:
        verbose_name_plural = "Posts"
        verbose_name = "Post"




class PostImage(TimeStampModel):
    image = models.ImageField(upload_to="post/%Y/%m/%d")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="images")

    def __str__(self):
        return  f"{self.post} image"

    class Meta:
        verbose_name_plural = "image"
        verbose_name = "images"


