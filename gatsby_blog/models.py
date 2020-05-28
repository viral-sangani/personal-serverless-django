from django.db import models
from django.contrib.postgres.fields import JSONField


def default():
    return ([])


class BlogLike(models.Model):
    slug = models.CharField(max_length=500)
    totalLikes = models.IntegerField(default=0)
    individualLikes = JSONField(default=default)
    time = models.DateTimeField(auto_now_add=True)
    ipList = JSONField(default=default)

    def __str__(self):
        return self.slug + " ==> " + str(self.totalLikes)


class BlogSubscriber(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=254)
    time = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=500)

    def __str__(self):
        return self.name
