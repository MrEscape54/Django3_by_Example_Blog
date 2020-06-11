from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView, SingleObjectMixin
from django.core.mail import send_mail
from taggit.models import Tag

from .models import Post, User, Comment
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    # Si ponemos "model = Post" el queryset por default es Post.objects.all()
    queryset = Post.published.all()
    # eL nombre por default es object_list
    context_object_name = 'posts'
    paginate_by = 4
    #template_name is not necessary if template name is post_list and it is at templates/blog

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status='publicado', publish__year=year, publish__month=month, publish__day=day, slug=post)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
    # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else: 
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments,'new_comment': new_comment,'comment_form': comment_form})


""" def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='publicado')
    post_url = request.build_absolute_uri(post.get_absolute_url())

    if request.method == 'POST':
        form = EmailPostForm(request.POST)  
        if form.is_valid():
            form.send_mail(post, post_url)
            return HttpResponseRedirect('/blog')
    else:
        form = EmailPostForm()
    return render(request, 'blog/post_share.html', {'post': post, 'form': form}) """


class SharePostView(SingleObjectMixin, FormView): 
    form_class = EmailPostForm
    template_name = 'blog/post_share.html'
    success_url = '/blog'
    context_object_name = 'posts'
    queryset = Post.published.all()

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        context = {'post': post, 'form': self.form_class}
        return render(request, self.template_name, context)   

    def form_valid(self, form):    
        post = self.get_object()
        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        form.send_mail(post, post_url)
        return super(SharePostView, self).form_valid(form)