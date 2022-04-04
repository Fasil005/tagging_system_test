from django.urls import path
from .views import AdminPostsManagement, UserPostManagement, PostManagement

urlpatterns = [
    path('', AdminPostsManagement.as_view({
        'post': 'create'
    }), name='admin_posts_management'),

    path('<pk>', UserPostManagement.as_view({
        'get': 'retrieve',
        'post': 'partial_update'
    }), name='user_post_management'),

    path('liked/users/<pk>', PostManagement.as_view({
        'get': 'retrieve',
    }), name='post_management'),
]
