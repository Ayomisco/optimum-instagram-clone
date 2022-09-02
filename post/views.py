from multiprocessing import context
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from post.models import *
from auth_system.models import Profile

from django.contrib.auth.decorators import login_required

# forms
from post.forms import *

# Create your views here.

@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)

    # Calling all follower by groups
    group_ids = []

    # adding a;; the post to the group id
    for post in posts:
        group_ids.append(post.post_id)
    # Filtering post by id
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    template = loader.get_template('index.html')

    context = {
        'post_items': post_items,

    }

    # return HttpRequest(template.render(context, request))
    return HttpResponse(template.render(context, request))


@login_required
def PostDetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # profile = Profile.objects.get(user=request.user)
    favourited = False

    # favourite color confitions 
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

        if profile.favourites.filter(id=post_id).exists():
            favourited = True

    template = loader.get_template('post_detail.html')
    context = {
        'post': post,
        'favourited': favourited
    }
    return HttpResponse(template.render(context, request))



@login_required
def NewPost(request):
    user = request.user.id
    tags_objs = []

    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tags_input = form.cleaned_data.get('tags')
            
            # spliting tags by comma
            tag_lists = list(tags_input.split(','))

            # 
            for tag in tag_lists:
                # This get tag title and if it doesn't exit it create 1
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)

            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)

            p.tags.set(tags_objs)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()

    context = {
        'form': form,
        }

    return render(request, 'new_post.html', context)



# Tags View
@login_required
def Tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    # MERGING POSTS WITH TAG WITH TAG NAME
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    context = {
        'tag': tag,
        'posts': posts
    }

    template = loader.get_template('tag.html')

    return HttpResponse(template.render(context, request))


    # Likes View
@login_required
def IndexLike(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes

    liked = Likes.objects.filter(user=user, post=post)

    if not liked:
        like = Likes.objects.create(user=user, post=post)
        
        current_likes = current_likes + 1
    else:
        # Unliking
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()

    return HttpResponseRedirect(reverse('index'))


@login_required
def PostDetailLike(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes

    liked = Likes.objects.filter(user=user, post=post)

    if not liked:
        like = Likes.objects.create(user=user, post=post)
        
        current_likes = current_likes + 1
    else:
        # Unliking
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()

    return HttpResponseRedirect(reverse('postdetail', args=[post_id]))



# Favourites post
@login_required
def Favourites(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourites.filter(id=post_id).exists():
        profile.favourites.remove(post)
    else:
        profile.favourites.add(post)

    return HttpResponseRedirect(reverse('postdetail', args=[post_id]))
