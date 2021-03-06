from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView, SingleObjectMixin, CreateView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DateDetailView
from django.core.mail import send_mail
from django.db.models import Count

from .models import Post, User, Comment, PostTag
from .forms import EmailPostForm, CommentForm


""" def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(PostTag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = {'page_number': page_number, 'page_obj': page_obj, 'posts': posts,'tag': tag}
    return render(request, 'blog/post_list.html', context) """

class PostListView(ListView):
    # Si ponemos "model = Post" el queryset por default es Post.objects.all()
    queryset = Post.published.all()
    # eL nombre por default es object_list
    context_object_name = 'posts'
    paginate_by = 4
    #template_name is not necessary if template name is post_list and it is at templates/blog

    #actualizamos el context para incluir el tag (ver template para ver porque)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # si hay kwargs se actualiza el context
        if self.kwargs:
            context["tag"] = self.kwargs['tag_slug']
        return context

    #filtramos los post en caso de que haya filtro por tag (se usa el mismo template con diferentes URLs, ver urls.py)
    def get_queryset(self):
        tag = None
        #si hay kwargs se aplica el filtro
        if self.kwargs:
            tag_slug = self.kwargs['tag_slug']
            tag = get_object_or_404(PostTag, slug=tag_slug)
            posts = self.queryset.filter(tags__in=[tag])
            return posts
        return self.queryset

class PostYearArchiveView(YearArchiveView):
    queryset = Post.published.all()
    template_name = 'blog/post_list.html'
    date_field = "publish"
    context_object_name = 'posts'
    make_object_list = True
    paginate_by = 4

class PostMonthArchiveView(MonthArchiveView):
    queryset = Post.published.all()
    template_name = 'blog/post_list.html'
    date_field = "publish"
    context_object_name = 'posts'
    month_format='%m'
    paginate_by = 4

class PostDateDetailView(DateDetailView):
    queryset = Post.published.all()
    date_field = "publish"
    month_format='%m'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        post_tags_pks = obj.tags.all().values_list('pk', flat=True)
        related_posts = self.queryset.filter(tags__in=post_tags_pks).exclude(pk=obj.pk)
        related_posts = related_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:3]
        context["related_posts"] = related_posts
        comments = obj.comments.filter(active=True)
        context["comments"] = comments
        context['post_id'] =  obj.pk

        # Agregamos el form de comentarios al context (solo para GET)
        context['form'] = CommentForm()
        return context

class NewComment(CreateView):
    queryset = Comment.actives.all()
    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context["form"].instance.post
        context['post'] = post
        post_tags_pks = post.tags.all().values_list('pk', flat=True)
        related_posts = Post.published.filter(tags__in=post_tags_pks).exclude(pk=post.pk)
        related_posts = related_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:3]
        context["related_posts"] = related_posts
        comments = post.comments.filter(active=True)
        context["comments"] = comments
        return context

class PostDetail(View):

    def get(self, request, *args, **kwargs):
        view = PostDateDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = NewComment.as_view()
        return view(request, *args, **kwargs)

"""def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status='publicado', publish__year=year, publish__month=month, publish__day=day, slug=post)

    #Trae los ids de los tags que tiene el post
    post_tags_ids = post.tags.values_list('id', flat=True)
    # Trae los post que tienen estos tags y excluye al que se está viendo
    related_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    related_posts = related_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:3]

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
    
    context = {'post': post, 'comments': comments,'new_comment': new_comment,'comment_form': comment_form, 'related_posts': related_posts}
    return render(request, 'blog/post_detail.html', context) """

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