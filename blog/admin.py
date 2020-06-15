from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment, PostTag


admin.site.register(User, UserAdmin)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Son las columnas que se muestran en la grilla
    list_display = ('title', 'slug', 'full_name', 'status', 'created', 'publish') # full_name está definido en el modelo Post
    # Los filtros que se muesran al costado
    list_filter = ( 'status', 'publish', 'tags')
    # Campos de búsqueda en la barra de búsqueda
    search_fields = ['title', 'author__first_name', 'author__last_name']
    #Campos que se generan de forma automática
    prepopulated_fields = {'slug': ('title',)}
    # Reemplaza el drop-down para que parezca una lupa (para FKs)
    raw_id_fields = ('author',)
    # Orden de aparición de las filas de la grilla
    date_hierarchy = 'publish'
    # Opciones de ordenamiento
    ordering = ('status', 'publish')
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')       
        
@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}
