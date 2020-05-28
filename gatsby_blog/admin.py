from django.contrib import admin
from gatsby_blog.models import BlogLike, BlogSubscriber


# Register your models here.
admin.site.register(BlogLike)
admin.site.register(BlogSubscriber)
