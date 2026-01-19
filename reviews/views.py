from django.shortcuts import redirect #Aka
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Avg, Q
from .models import Item
from .forms import ReviewForm

class ItemListView(ListView):
    model = Item
    template_name = 'reviews/item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        query = self.request.GET.get('q')
        genre = self.request.GET.get('genre')
        queryset = Item.objects.annotate(avg_rating=Avg('reviews__rating'))
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        if genre:
            queryset = queryset.filter(description__icontains=genre)
        return queryset.order_by('-avg_rating')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

class ItemDetailView(DetailView):
    model = Item
    template_name = 'reviews/item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin:login')
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = self.object
            review.user = request.user
            review.save()
            return redirect('item_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

class AdvancedSearchView(TemplateView):
    template_name = 'reviews/advanced_search.html'
