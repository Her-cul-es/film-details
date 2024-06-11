from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserProfile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Category, Review
from .forms import MovieForm

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                UserProfile.objects.create(user=user)

                messages.success(request, 'You are now registered and can log in')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

def view_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.first_name = request.POST['first_name']
        profile.last_name = request.POST['last_name']
        profile.email = request.POST['email']
        profile.phone_number = request.POST['phone_number']
        profile.image = request.POST['image']
        profile.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('profile')

    return render(request, 'profile.html', {'user_profile': profile})

def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        user_profile.first_name = request.POST.get('first_name', user_profile.first_name)
        user_profile.last_name = request.POST.get('last_name', user_profile.last_name)
        user_profile.email = request.POST.get('email', user_profile.email)
            # Check if an image is uploaded
        if 'image' in request.FILES:
            user_profile.image = request.FILES['image']

        user_profile.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('view_profile')

    return render(request, 'edit_profile.html')
def index(request):
    return render(request, 'index.html')

def home(request):
    movie = Movie.objects.all()
    return render(request, 'home.html', {'movies': movie})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})

# views.py

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            return redirect('movie_detail', movie_id=movie.pk)
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})

@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user == movie.added_by:
        if request.method == 'POST':
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('movie_detail', movie_id=movie.pk)
        else:
            form = MovieForm(instance=movie)
        return render(request, 'edit_movie.html', {'form': form, 'movie': movie})
    else:
        # Handle unauthorized access
        return HttpResponse("You are not authorized to edit this movie.")

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user == movie.added_by:
        movie.delete()
        return redirect('home')
    else:
        # Handle unauthorized access
        return HttpResponse("You are not authorized to delete this movie.")


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = movie.reviews.all()

    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')

        # Validate the form data
        if review_text and rating:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError("Rating should be between 1 and 5")
            except ValueError:
                return render(request, 'movie_detail.html',
                              {'movie': movie, 'reviews': reviews, 'error_message': 'Invalid rating value'})

            # Create and save the review
            review = Review.objects.create(
                movie=movie,
                user=request.user,
                review_text=review_text,
                rating=rating
            )
            return redirect('movie_detail', movie_id=movie.pk)
        else:
            return render(request, 'movie_detail.html',
                          {'movie': movie, 'reviews': reviews, 'error_message': 'Please fill in all fields'})

    return render(request, 'movie_detail.html', {'movie': movie, 'reviews': reviews})


@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    # Check if the user has already submitted a review for this movie
    existing_review = Review.objects.filter(movie=movie, user=request.user).first()

    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')

        # Validate the form data
        if review_text and rating:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError("Rating should be between 1 and 5")
            except ValueError:
                return render(request, 'add_review.html',
                              {'error_message': 'Invalid rating value', 'existing_review': existing_review})

            # Check if an existing review exists for the user and update it
            if existing_review:
                existing_review.review_text = review_text
                existing_review.rating = rating
                existing_review.save()
            else:
                # Create a new review
                review = Review.objects.create(
                    movie=movie,
                    user=request.user,
                    review_text=review_text,
                    rating=rating
                )

            return redirect('movie_detail', movie_id=movie.pk)
        else:
            return render(request, 'add_review.html',
                          {'error_message': 'Please fill in all fields', 'existing_review': existing_review})

    return render(request, 'add_review.html', {'movie': movie, 'existing_review': existing_review})


def category_movies(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    movies = Movie.objects.filter(category=category)
    return render(request, 'category_movies.html', {'category': category, 'movies': movies})

@login_required
def user_movies(request):
    user = request.user
    movies = Movie.objects.filter(added_by=user)
    return render(request, 'user_movies.html', {'movies': movies})

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, added_by=request.user)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Movie deleted successfully!')
        return redirect('user_movies')
    return render(request, 'user_movies.html', {'movie': movie})

def search_movies(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')  # Use get method with a default value
        movies = Movie.objects.filter( Q(title__icontains=searched) | Q(category__name__icontains=searched))
        return render(request, 'search_results.html', {'searched': searched, 'movies': movies})
    else:
        return render(request, 'search_results.html', {})

def custom_logout_view(request):
    logout(request)
    return redirect('index')

