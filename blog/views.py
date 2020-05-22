from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import Post, User

class IndexView(TemplateView):
    template_name = "blog/index.html"

def post_list(request):
    posts = Post.published.all()
    return render(request, 'post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='publicado', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'post/detail.html', {'post': post})


