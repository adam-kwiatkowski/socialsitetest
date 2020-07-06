from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.html import format_html
from io import BytesIO
from PIL import Image as PILImage
from PIL import ExifTags
from django.core.files import File
# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    try:
        return 'user_{0}/{1}'.format(instance.user.id, filename)
    except AttributeError:
        return 'user_{0}/{1}'.format(instance.author.id, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path)

class Post(models.Model):
    text = models.TextField('text content')
    likes = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')


class Image(models.Model):
    image = models.ImageField(upload_to=user_directory_path)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_images')

    # def save(self, *args, **kwargs):
    #     im = PILImage.open(self.image)
    #     im_io = BytesIO()

    #     try:
    #         for orientation in ExifTags.TAGS.keys() : 
    #             if ExifTags.TAGS[orientation]=='Orientation' : break 
    #         exif=dict(im._getexif().items())

    #         if exif[orientation] == 3 : 
    #             im=im.rotate(180, expand=True)
    #         elif exif[orientation] == 6 : 
    #             im=im.rotate(270, expand=True)
    #         elif exif[orientation] == 8 : 
    #             im=im.rotate(90, expand=True)

    #         im.save(im_io, 'JPEG', quality=10)
    #         self.image = File(im_io, name=self.image.name)
    #         super().save(*args, **kwargs)

    #     except:
    #         traceback.print_exc()

        

# class Post(models.Model):
#     text_content = models.CharField(max_length=500)
#     image_content = models.ImageField(upload_to=user_directory_path, blank=True)
#     pub_date = models.DateTimeField('date published')
#     likes = models.IntegerField(default=0)
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')

#     def image_path(self):
#         if self.image_content:
#             return format_html("<a href='{url}'>{url}</a>", url=self.image_content.url)

#     image_path.empty_value_display = 'No images'
