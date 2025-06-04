from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .models import Photo, Tag, Comment
from .models import Profile, Photo
from .forms import PhotoForm, CommentForm, RegisterForm
from .forms import ProfileUpdateForm
from .forms import CommentForm 


def home(request):
    tag_filter = request.GET.get('tag')
    photos = Photo.objects.all().order_by('-created_at')
    all_tags = Tag.objects.all()  # Get all tags for the filter dropdown
    
    if tag_filter:
        photos = photos.filter(tags__name=tag_filter)
    
    return render(request, 'photo_gallery/home.html', {
        'photos': photos,
        'all_tags': all_tags
    })

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    comments = photo.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.user = request.user
            comment.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = CommentForm()
    
    return render(request, 'photo_gallery/photo_detail.html', {
        'photo': photo,
        'comments': comments,
        'comment_form': form  # Changed from 'form' to 'comment_form'
    })

@login_required
def profile(request, username):
    # Get the user whose profile we're viewing
    profile_user = get_object_or_404(User, username=username)
    
    # Get or create profile (just in case)
    profile, created = Profile.objects.get_or_create(user=profile_user)
    
    # Handle form submission for profile owner
    if request.method == 'POST':
        if request.user == profile_user:  # Only owner can edit
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if p_form.is_valid():
                p_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('profile', username=username)
        else:
            messages.error(request, "You can't edit someone else's profile")
            return redirect('profile', username=username)
    else:
        # Only show form to profile owner
        p_form = ProfileUpdateForm(instance=profile) if request.user == profile_user else None
    
    # Get user's photos for display
    user_photos = Photo.objects.filter(user=profile_user).order_by('-created_at')[:6]
    
    context = {
        'profile_user': profile_user,
        'p_form': p_form,
        'user_photos': user_photos,
    }
    return render(request, 'photo_gallery/profile.html', context)
@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    return redirect('photo_detail', pk=photo.pk)

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            form.save_m2m()  # Save many-to-many data
            messages.success(request, 'Your photo has been uploaded!')
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm()
    return render(request, 'photo_gallery/upload_photo.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'photo_gallery/register.html', {'form': form})
def home(request):
    tag_filter = request.GET.get('tag')
    if tag_filter:
        photos = Photo.objects.filter(tags__name=tag_filter).order_by('-created_at')
    else:
        photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'photo_gallery/home.html', {'photos': photos})