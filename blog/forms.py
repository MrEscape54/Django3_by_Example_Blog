from django import forms
from django.core.mail import send_mail
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}))
    to = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje aquí'}), required=False)

    def send_mail(form, post, post_url):
        cd = form.cleaned_data # si la info es válida, se crea un diccionario "form.cleaned_data" con la info limpia
        # Crea el path completo para enviar el link del post
        subject = f"{cd['name']} recommends you read " f"{post.title}"
        message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comment: {cd['comment']}"

        send_mail(subject, message, 'admin@myblog.com', [cd['to']], fail_silently=True)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'post')
        
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}),
            'body': forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje aquí'}),
            'post' : forms.HiddenInput(),
        }