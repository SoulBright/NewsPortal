from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.shortcuts import render

from .filters import PostFilter
from .forms import PostForm
from .models import *


def post_filter(request):
    f = PostFilter(request.GET, queryset=Post.objects.all())
    return render(request, 'post_filter.html', {'filter': f})


class NewsList(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    # queryset = Post.objects.order_by('-id')
    ordering = ['-id']
    paginate_by = 5
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Post_all'] = Post.objects.all()
        context['form'] = PostForm()
        return context

    def news(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class NewsDetails(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class CategoriesList(ListView):
    model = Category
    template_name = 'categories_list.html'
    context_object_name = 'categories_list'


class CategoriesDetail(DetailView):
    model = Category
    template_name = 'categories_detail.html'
    context_object_name = 'categories_detail'

    # def get_context_data(self, **kwargs):
    #     pass


class PostCreate(CreateView):
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdate(UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'post_delete.html'
    context_object_name = 'post_delete'
    queryset = Post.objects.all()
    success_url = '/news/'

