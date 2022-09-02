from django.urls import path
from post.views import *

urlpatterns = [
    path('', index, name='index'),
    path('newpost', NewPost, name='newpost'),
    path('<uuid:post_id>', PostDetails, name='postdetail'),
    path('tag/<slug:tag_slug>', Tags, name='tags'),
    path('<uuid:post_id>/likes', IndexLike, name='postindexlike'),
    path('<uuid:post_id>/like', PostDetailLike, name='postlike'),

    path('<uuid:post_id>/favourites', Favourites, name='postfavourite'),


    


]