from django.urls import path
from blog import views

from blog.models import Post

app_name = 'blog'

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='post_list_by_tag'),
    path('<int:year>/', views.PostYearArchiveView.as_view(), name="post_year_archive"),
    path('<int:year>/<int:month>/', views.PostMonthArchiveView.as_view(month_format='%m'), name="post_month_numeric"),

    path("<int:year>/<int:month>/<int:day>/<slug:post>", views.post_detail, name="post_detail"),
    path('<int:pk>/share/', views.SharePostView.as_view(), name='post_share'),
]
