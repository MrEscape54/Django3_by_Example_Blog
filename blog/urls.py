from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    #path("", views.PostListView.as_view(), name="post_list"),
    #path("<int:year>/<str:month>/<int:day>/<slug:post>", views.PostDetailView.as_view(), name="post_detail"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>", views.post_detail, name="post_detail"),
    #path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:pk>/share/', views.SharePostView.as_view(), name='post_share'),
]
