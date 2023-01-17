from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http.response import HttpResponse #  импортируем респонс для проверки текста

from django.utils import timezone
import pytz

from .filters import PostFilter
from .forms import PostForm, UserForm
from .models import *


def post_filter(request):
    f = PostFilter(request.GET, queryset=Post.objects.all())
    return render(request, 'post_filter.html', {'filter': f})


# Главная страница, список статей
class NewsList(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    ordering = ['-id']
    paginate_by = 8
    form_class = PostForm

    def get_context_data(self, **kwargs):
        current_time = timezone.localtime(timezone.now())
        context = super().get_context_data(**kwargs)
        context['Post_all'] = Post.objects.all()
        context['form'] = PostForm()
        context['current_time'] = current_time
        context['timezones'] = pytz.common_timezones
        context['authors'] = Author.objects.all()
        context['categories'] = PostCategory.objects.all()
        return context

    def news(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/news/')


# Контент статьи
class NewsDetails(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


# Список категорий
class CategoriesList(ListView):
    model = Category
    template_name = 'categories_list.html'
    context_object_name = 'categories_list'


# Список статей в категории
class PostListByCategories(ListView):
    model = Post
    template_name = 'categories_detail.html'
    context_object_name = 'categories_detail'

    def add_subscribe(request):
        user = request.user
        id = request.META.get('HTTP_REFERER')[-2]
        category = Category.objects.get(id=id)
        category.subscribers.add(user)
        return redirect(request.META.get('HTTP_REFERER'))

    def dell_subscribe(request):
        user = request.user
        id = request.META.get('HTTP_REFERER')[-2]
        category = Category.objects.get(id=id)
        category.subscribers.remove(user)
        return redirect(request.META.get('HTTP_REFERER'))

    def get_queryset(self):
        cat = self.request.resolver_match.kwargs['pk']
        return PostCategory.objects.filter(categoryThrough=cat)

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        cat = self.request.resolver_match.kwargs['pk']
        que = PostCategory.objects.filter(categoryThrough=cat)
        context['category_self'] = que[0].categoryThrough
        context['is_subscribers'] = UserCategory.objects.filter(subCategory=id, subUser=self.request.user).exists()
        return context


# Создание статьи
class PostCreate(PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)


    def form_valid(self, form):
        obj = form.save(commit=False)
        authors = Author.objects.all()
        for i in authors:
            if i.authorUser == self.request.user:
                obj.author = i
        return super().form_valid(form)


# Редактирование статьи
class PostUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# удаление статьи
class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    context_object_name = 'post_delete'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post',)


# Информация о профиле пользователя
class UserDetails(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_detail'


# Редактирование профиля пользователя
class UserUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'user_update.html'
    context_object_name = 'user_update'
    form_class = UserForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return User.objects.get(pk=id)

