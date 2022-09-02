from multiprocessing import context
# import profile
from django.shortcuts import redirect, render, get_object_or_404
# Authentication module
from auth_system.forms import ChangePasswordForm, CustomUserLoginForm, SignupForm, EditProfileForm
from django.contrib.auth.models import User
# template loader
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
# importing decorator for login require
from django.contrib.auth.decorators import login_required
# clearing session and updating with a new one when password is reset
from django.contrib.auth import update_session_auth_hash
# Changing profile
from auth_system.models import *
from django.contrib.auth import login as auth_login
from post.models import *
# Paginator Importation
from django.core.paginator import Paginator
# Resolve 
from django.urls import resolve #This will help in identifying the url name. This I use for the tabs  in user profile
# Atomic Transaction
from django.db import transaction

# PROFILE VIEWS
def UserProfile(request, username):
    # user = User.objects.get(username=username)
    user = get_object_or_404(User, username=username)
    # profile = get_object_or_404(Profile, user=user)

    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourites.all()

    # Profile Info Start Here
    # Counting Post and followers
    post_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    follower_count = Follow.objects.filter(following=user).count()

    # Check status
    follow_status = Follow.objects.filter(following=user, follower=request.user)

 # Paginator Starts here
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    post_paginator = paginator.get_page(page_number)


    template = loader.get_template('profile.html')
    
    context = {
        'posts': post_paginator,
        'profile': profile,
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'follow_status': follow_status,

    }

    return HttpResponse(template.render(context, request))



# # def Profile(request):
#     return render(request, 'user-profile.html')



def Signup(request):
    # tags = Tag.objects.all()
    # categories = Category.objects.all()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # first_name = form.cleaned_data.get('first_name')
            # last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            User.objects.create_user(username=username, email=email, password=password)
            return redirect('index')

    

    else:
        form = SignupForm()


    template = loader.get_template('signup.html')

    context = {
        'form': form,
        # 'categories': categories,
        # 'tags': tags,
    }

    # return render(request, 'signup.html', context)
    return HttpResponse(template.render(context, request))


# def LoginView(request):
#     if request.method == 'POST':
#         form = CustomUserLoginForm(request.POST)
#         if form.is_valid():
#             # user = form.get_user()
#             # login(request, user)

#             user = form.user
#             auth_login(request, user)
#             return redirect('index')
#     else:
#         form = CustomUserLoginForm()
#     return render(request, 'login.html', {'form': form})

# @login_required
# CHange Password View
def ChangePassword(request):
    # tags = Tag.objects.all()
    # categories = Category.objects.all()
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('passwordresetsuccess')

    else:
        form = ChangePasswordForm(instance=user)
    
    context = {
        'form': form,
        # 'categories': categories,
        # 'tags': tags,
    }

    return render(request, 'change-password.html', context)

# Password reset success
def PasswordResetSuccess(request):
    return render(request, 'password_change_success.html')


@login_required
# Updating Profile View
def EditProfile(request):
    # tags = Tag.objects.all()
    # categories = Category.objects.all()
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.profile_pic = form.cleaned_data.get('profile_pic')
            profile.profile_banner = form.cleaned_data.get('profile_banner')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.profile_info = form.cleaned_data.get('profile_info')

            profile.save()
            # update_session_auth_hash(request, user)
            return redirect('index')

    else:
        form = EditProfileForm()

    context = {
        'form': form,
        # 'categories': categories,
        # 'tags': tags,
    }

    return render(request, 'edit_profile.html', context)

# Password reset success


# def PasswordResetSuccess(request):
#     return render(request, 'password_change_success.html')


# Follow View
@login_required
def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try: 
        f, created = Follow.objects.get_or_create(follower=user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=user).all().delete
        else:
            posts = Post.objects.all().filter(user=following)[1:0]

            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))

