from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db import models
from django.http import Http404, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .forms import FilmCommentForm
from .models import FilmComment
from reviews.models import Item


def _get_film_by_slug(slug: str):
    return get_object_or_404(Item, slug=slug)


def home(request):
    films_qs = Item.objects.all()
    
    q = (request.GET.get('q') or '').strip()
    if q:
        q_lower = q.lower()
        films_qs = films_qs.filter(
            models.Q(title__icontains=q) |
            models.Q(genre__icontains=q) |
            models.Q(year__icontains=q)
        )
    
    films = list(films_qs)
    allowed_titles = {film.title for film in films}

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

    films_with_comments = []
    for film in films:
        film.comments = list(
            FilmComment.objects.filter(film_title=film.title).select_related('user')[:10]
        )
        films_with_comments.append(film)

    return render(
        request,
        'home.html',
        {
            'films': films_with_comments,
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
            if comment.film_title != film.title:
                messages.error(request, 'Invalid film.')
                return redirect('film_detail', slug=slug)
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added.')
            return redirect('film_detail', slug=slug)
    else:
        form = FilmCommentForm(initial={'film_title': film.title})

    comments = list(
        FilmComment.objects.filter(film_title=film.title).select_related('user')[:25]
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


def comment_api(request, pk: int):
   
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'authentication required'}, status=401)

    try:
        comment = FilmComment.objects.get(pk=pk)
    except FilmComment.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)

    if comment.user_id != request.user.id:
        return JsonResponse({'error': 'forbidden'}, status=403)

    if request.method == 'DELETE':
        comment.delete()
        return JsonResponse({'status': 'deleted'})

    if request.method == 'PUT':
        import json

        try:
            data = json.loads(request.body.decode() or '{}')
        except Exception:
            return JsonResponse({'error': 'invalid json'}, status=400)

        text = (data.get('text') or '').strip()
        if not text:
            return JsonResponse({'error': 'text required'}, status=400)
        if len(text) > 1000:
            return JsonResponse({'error': 'text too long'}, status=400)

        comment.text = text
        comment.save()
        return JsonResponse({'status': 'updated', 'text': comment.text})

    return HttpResponseNotAllowed(['PUT', 'DELETE'])


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
