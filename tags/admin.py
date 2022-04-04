from django.contrib import admin
from .models import Tags, Posts, User, Images

admin.site.register(User)
admin.site.register(Tags)
admin.site.register(Posts)
admin.site.register(Images)

