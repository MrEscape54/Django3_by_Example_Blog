from django.urls import path
from blog import views


from blog.models import Post

app_name = 'blog'

urlpatterns = [
    # URL for listing posts w/o filters
    path("", views.PostListView.as_view(), name="post_list"),
    #URL for listing post if tag is selected
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='post_list_by_tag'),

    #URLs for detailed posts
    path('<int:year>/', views.PostYearArchiveView.as_view(), name="post_year_archive"),
    path('<int:year>/<int:month>/', views.PostMonthArchiveView.as_view(), name="post_month_numeric"),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetail.as_view(), name="post_date_detail"),

    # Form to share a post by email
    path('<int:pk>/share/', views.SharePostView.as_view(), name='post_share'),
]
