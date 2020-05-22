from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse


class User(AbstractUser):
    #Query u.last_name()
    def full_name(self):
        return f'{self.last_name.capitalize()}, {self.first_name.capitalize()}'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='publicado')


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

    # Para crear una URL canónica de un objeto (links de cada post: ver formato de URLs en el path de details)
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
    
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



