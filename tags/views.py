from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Posts, Images, User, Tags, FollowedTags
from .serializers import UserPostsSerializer, PostSerializer


class AdminPostsManagement(ViewSet):
    """
    This API to create posts
    """
    def create(self, request):
        data = request.data
        # Saving Posts details to Post table
        try:
            post = Posts(
                title=data.get('title'),
                uploader=User.objects.get(id=data.get('uploader')),
                description=data.get('description'),
            )
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'})
        post.save()
        # Saving Images details to Images table from Images list
        Images.objects.bulk_create([
            Images(
                post=post,
                file=image,
            ) for image in request.FILES.getlist('file')
        ])
        # Adding Tags to manytomany relationship table if it's already exists
        # otherwise save the tag to Tags table then add to manytomany relationship table.
        for item in data.getlist('tags'):
            if Tags.objects.filter(title=item).exists():
                tag = Tags.objects.get(title=item)
                post.tagged.add(tag)
            else:
                tag = Tags(title=item)
                tag.save()
                post.tagged.add(tag)
        return Response({
            'status': 'success',
        })


class UserPostManagement(ViewSet):

    def retrieve(self, request, pk):
        """
        This API to get all posts of a user
        :param pk: User ID who logged in
        """
        posts = Posts.objects.all()
        serialized_data = UserPostsSerializer(posts, context={'user_id': pk}, many=True).data
        # sorting serialized data by tag weight
        serialized_data.sort(key=lambda x: x['user_tags_status'], reverse=True)
        return Response({
            'data': serialized_data,
            'status': 'success'
        })

    def partial_update(self, request, pk):
        """
        This API to like or unlike a post
        :param request: Pass True for like and False for unlike
        :param pk: User ID
        """
        post_id = request.GET.get('post_id')
        post = Posts.objects.get(id=post_id)
        if request.data.get('like'):
            post.liked_user.add(pk)
            # If the user already liked the post then unlike it
            post.disliked_user.remove(pk) if post.disliked_user.exists() else None
            # Here we are checking If the user following the post's tag or not and Update to follow every tag's of a post
            if post.tagged.exists():
                for tag in post.tagged.all():
                    user = User.objects.get(id=pk)
                    FollowedTags.objects.update_or_create(
                        user=user,
                        tag=tag,
                        post=post,
                        defaults={'is_followed': True}
                    )
        else:
            # Here we are checking If the user following the post's tag or not and Update to unfollow the tag every tag's of a post
            post.disliked_user.add(pk)
            post.liked_user.remove(pk) if post.liked_user.exists() else None
            if post.tagged.exists():
                for tag in post.tagged.all():
                    user = User.objects.get(id=pk)
                    FollowedTags.objects.update_or_create(
                        user=user,
                        tag=tag,
                        post=post,
                        defaults={'is_followed': False}
                    )

        post.save()
        return Response({
            'data': None,
            'status': 'success'
        })


class PostManagement(ViewSet):

    def retrieve(self, request, pk):
        """
            API to know users who liked the post
            :param pk: Post ID
        """
        posts = Posts.objects.get(id=pk)
        serializer = PostSerializer(posts)
        return Response({
            'data': serializer.data,
            'status': 'success'
        })
