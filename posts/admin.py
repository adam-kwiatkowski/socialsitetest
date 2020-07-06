from django.contrib import admin
from .models import Post, Image, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.


class UserProfileInLine(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInLine,)

# class UserProfileAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         obj.user = request.user
#         super().save_model(request, obj, form, change)


class ImageAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
    list_display = ('image', 'post', 'author')


class ImageInLine(admin.StackedInline):
    model = Image
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'likes', 'pub_date', 'author')
    inlines = [ImageInLine]


admin.site.register(Image, ImageAdmin)
admin.site.register(Post, PostAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
