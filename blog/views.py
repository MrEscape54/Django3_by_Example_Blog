from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.core.mail import send_mail

from .models import Post, User, Comment
from .forms import EmailPostForm, CommentForm



class PostListView(ListView):
    # Si ponemos "model = Post" el queryset por default es Post.objects.all()
    queryset = Post.published.all()
    # eL nombre por default es object_list
    context_object_name = 'posts'
    paginate_by = 4
    #template_name is not necessary if template name is post_list and it is at templates/blog


""" class PostDetailView(DateDetailView):
    model = Post
    context_object_name = 'post'
    date_field = 'publish'
    month_format = '%n' 
    #template_name = "blog/post_detail.html"

     def get_object(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        post = self.kwargs.get('slug')
        return get_object_or_404(Post, status='publicado', publish__year=year, publish__month=month, publish__day=day, slug=post)
 """

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

def post_share(request, post_id):
    #retrieve the post by ID and make sure that the retrieved post has a published status
    post = get_object_or_404(Post, id=post_id, status='publicado')
    # Variable creada para utilizar en el template a través de un success message
    sent = False
    if request.method == 'POST':
        # Si el método es POST hay que procesar la información
        form = EmailPostForm(request.POST) # se crea una instancia de ContactForm con los datos provistos por el dict request.PSOT
        
        #Método que valida la información del request.POST
        if form.is_valid():
            cd = form.cleaned_data # si la info es válida, se crea un diccionario "form.cleaned_data" con la info limpia

            # Crea el path completo para enviar el link del post
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comment: {cd['comment']}"

            send_mail(subject, message, 'admin@myblog.com', [cd['to']], fail_silently=True)
            sent = True

            # fail_silently=False to raise an exception if the email couldn't be sent correctly. 
            # If the output you see is 1, then your email was successfully sent.
            # Si la información es válida, redirigimos a index.html
            #return HttpResponseRedirect('/') # podemos enviar un context al index si lo deseamos
    else:
        #Si el método no es POST, entonces creamos una instancia del formulario vacio
        form = EmailPostForm()
    # Si llegamos a esta línea es porque es un GET o el form tiene errores
    #Si es GET se carga el formulario vacio, si tuvo errores se carga con la info previamente ingresada
    return render(request, 'blog/post_share.html', {'post': post, 'form': form, 'sent': sent})

