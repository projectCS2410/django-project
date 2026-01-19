from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .forms import FilmCommentForm
from .models import FilmComment


def _films_data():
    films = [
        {
            'title': 'Interstellar',
            'year': 2014,
            'genre': 'Sci‑Fi',
            'rating': '8.7',
            'image': 'films/interstellar.jpg',
            'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
            'trailer': 'https://www.youtube.com/embed/2LqzF5WauAw',
        },
        {
            'title': 'The Dark Knight',
            'year': 2008,
            'genre': 'Action',
            'rating': '9.0',
            'image': 'films/dark-knight.jpg',
            'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
            'trailer': 'https://www.youtube.com/embed/LDG9bisJEaI',
        },
        {
            'title': 'Inception',
            'year': 2010,
            'genre': 'Thriller',
            'rating': '8.8',
            'image': 'films/inception.jpg',
            'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
            'trailer': 'https://www.youtube.com/embed/8hP9D6kZseM',
        },
        {
            'title': 'Spirited Away',
            'year': 2001,
            'genre': 'Animation',
            'rating': '8.6',
            'image': 'films/spirited-away.jpg',
            'description': 'During her family\'s move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.',
            'trailer': 'https://www.youtube.com/embed/fDdjfF1Fy7A',
        },
        {
            'title': 'The Matrix',
            'year': 1999,
            'genre': 'Sci‑Fi',
            'rating': '8.7',
            'image': 'films/matrix.jpg',
            'description': 'When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.',
            'trailer': 'https://www.youtube.com/embed/m8e-FF8MsqU',
        },
        {
            'title': 'Parasite',
            'year': 2019,
            'genre': 'Drama',
            'rating': '8.5',
            'image': 'films/parasite.jpg',
            'description': 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
            'trailer': 'https://www.youtube.com/embed/SEUXfv87Wpk',
        },
    ]

    for film in films:
        film['slug'] = slugify(film['title'])

    return films


def _get_film_by_slug(slug: str):
    for film in _films_data():
        if film['slug'] == slug:
            return film
    raise Http404('Film not found')


def home(request):
    films = _films_data()
    allowed_titles = {film['title'] for film in films}

    q = (request.GET.get('q') or '').strip()
    if q:
        q_lower = q.lower()
        films = [
            film
            for film in films
            if q_lower in film['title'].lower()
            or q_lower in film['genre'].lower()
            or q_lower in str(film['year'])
        ]

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = FilmCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if comment.film_title not in allowed_titles:
                messages.error(request, 'Unknown film.')
                return redirect('home')
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added.')
            return redirect('home')
    else:
        form = FilmCommentForm()

    for film in films:
        film['comments'] = list(
            FilmComment.objects.filter(film_title=film['title']).select_related('user')[:10]
        )

    return render(
        request,
        'home.html',
        {
            'films': films,
            'comment_form': form,
            'q': q,
        },
    )


def film_detail(request, slug: str):
    film = _get_film_by_slug(slug)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = FilmCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if comment.film_title != film['title']:
                messages.error(request, 'Invalid film.')
                return redirect('film_detail', slug=slug)
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added.')
            return redirect('film_detail', slug=slug)
    else:
        form = FilmCommentForm(initial={'film_title': film['title']})

    comments = list(
        FilmComment.objects.filter(film_title=film['title']).select_related('user')[:25]
    )

    return render(
        request,
        'film_detail.html',
        {
            'film': film,
            'comments': comments,
            'comment_form': form,
        },
    )


@require_POST
def delete_comment(request, pk: int):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        comment = FilmComment.objects.select_related('user').get(pk=pk)
    except FilmComment.DoesNotExist:
        raise Http404('Comment not found')

    if comment.user_id != request.user.id:
        raise Http404('Not found')

    comment.delete()
    messages.success(request, 'Comment deleted.')
    return redirect(request.POST.get('next') or 'home')


class ForcedHomeLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
