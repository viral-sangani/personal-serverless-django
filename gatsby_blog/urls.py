from django.urls import path
from gatsby_blog.views import setLike, getLike, newSubscriber

urlpatterns = [
    path('set/', setLike.as_view(), name="setLikes"),
    path('get/', getLike.as_view(), name="getLikes"),
    path('subscribe/', newSubscriber.as_view(), name="newSubscriber")
]
