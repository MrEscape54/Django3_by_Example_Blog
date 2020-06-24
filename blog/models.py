from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import localtime
from django.urls import reverse

class User(AbstractUser):
    #Query u.last_name()
    def full_name(self):
        return f'{self.last_name.capitalize()}, {self.first_name.capitalize()}'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='publicado')


class PostTag(models.Model):
    name = models.CharField('nombre', max_length=40)
    slug = models.SlugField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Etiqueta'


class Post(models.Model):
    POST_STATUS = (('borrador', 'Borrador'), ('publicado', 'Publicado'))

    title = models.CharField('titulo', max_length=100)
    body = models.TextField('cuerpo')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='autor')
    # auto_now_add es para que se agregue el campo solo cuando se crea el objeto
    created = models.DateTimeField('creado', auto_now_add=True)
    # auto_now actualiza el campo cada vez que se hace un save() del objeto
    publish = models.DateTimeField('publicado', auto_now=True)
    updated = models.DateTimeField('actualizado', auto_now=True)
    # unique_for_date es para prevenir que no se creen slugs iguales el mismo día
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    status = models.CharField(max_length=10, choices=POST_STATUS, default='borrador')
    tags = models.ManyToManyField(PostTag, blank=True)

    # Para crear una URL canónica de un objeto (links de cada post: ver formato de URLs en el path de details)
    def get_absolute_url(self):
        #es importante definir local_time para evitar que la URL no se base en UTC y no haya relación entre la fecha en la base y en la URL
        local_time = localtime(self.publish)
        return reverse("blog:post_date_detail", args=[local_time.year, local_time.month, local_time.day, self.slug])
    
    # Este método sirve para poder usarlo en el list_display del admin (sino aparece el atributo username en la columna author)
    def full_name(self):
        return f'{self.author.last_name.capitalize()}, {self.author.first_name.capitalize()}'
    full_name.short_description = 'Autor'

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField('nombre', max_length=80)
    email = models.EmailField()
    body = models.TextField('comentario')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField('activo', default=True)

    def get_absolute_url(self):
        #es importante definir local_time para evitar que la URL no se base en UTC y no haya relación entre la fecha en la base y en la URL
        local_time = localtime(self.post.publish)
        return reverse("blog:post_date_detail", args=[local_time.year, local_time.month, local_time.day, self.post.slug])

    class Meta:
        ordering = ('created',)
        
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

