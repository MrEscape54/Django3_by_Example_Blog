from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Post, User

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = "blog/list.html"


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='publicado', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'post/detail.html', {'post': post})


