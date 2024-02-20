# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Album, Artist, Favorite
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Initialize Spotify client credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="fe983663e33741f980cc9e2878f6a07e", client_secret="515bfdc02524444081d05d27a84db1ef"))

def custom_404_view(request, exception):
    return render(request, 'app/error.html', status=404)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')  # Added return statement
        else:
            messages.error(request, "Account not created. Please contact support or try again later.")
            return redirect('signup')  
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

@login_required
def logout_views(request):
    return render(request,'app/logout.html')
def login_views(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('search')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  
    return render(request, 'app/login.html')


@login_required
def search(request):
    query = request.GET.get('q', '')
    query_type = request.GET.get('type', '')  
    print(request.user)
    user_favorites = Favorite.objects.filter(user=request.user) 
    print(user_favorites)
    albums_favorites=[]
    artists_favorites=[]

    for i in user_favorites:
        if i.album:
            
            albums_favorites.append(i.album)
        if i.artist:
            artists_favorites.append(i.artist)

    context = {'user': request.user, 'user_favorites': user_favorites,'artists_favorites':artists_favorites,'albums_favorites':albums_favorites}  # Pass user_favorites to context
  
    if query:
       
        if query_type == 'album':
            album_results = sp.search(q=query, type='album')
          
            context['albums'] = album_results['albums']['items']
        elif query_type == 'artist':
            artist_results = sp.search(q=query, type='artist')
            context['artists'] = artist_results['artists']['items']

        context['query'] = query
      
    return render(request, 'app/search.html', context)

@login_required
def mark_favorite(request):
    if request.method == 'POST':
        item_type = request.POST.get('type')
        item_id = request.POST.get('id')
        item_name = request.POST.get('name')
        user = request.user

  
        if item_type == 'album':
            album, created = Album.objects.get_or_create(user=user,spotify_id=item_id, name=item_name)
            print(album,created)
            if created:
                Favorite.objects.create(user=user, album=album)
        elif item_type == 'artist':
            artist, created = Artist.objects.get_or_create(user=user,spotify_id=item_id, name=item_name)
            if created:
                Favorite.objects.create(user=user, artist=artist)

    return redirect('search')
