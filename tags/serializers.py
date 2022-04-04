from rest_framework import serializers
from .models import Images, User, FollowedTags


class ImagesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    file = serializers.ImageField()


class UserPostsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    file = serializers.SerializerMethodField()
    uploader = serializers.IntegerField(source='uploader.id')
    created_at = serializers.DateTimeField(format='%d-%m-%Y %I:%M %p')
    updated_at = serializers.DateTimeField(format='%d-%m-%Y %I:%M %p')
    tags_count = serializers.SerializerMethodField(read_only=True)
    liked_count = serializers.SerializerMethodField(read_only=True)
    disliked_count = serializers.SerializerMethodField(read_only=True)
    liked = serializers.SerializerMethodField(read_only=True)
    unliked = serializers.SerializerMethodField(read_only=True)
    user_tags_status = serializers.SerializerMethodField(read_only=True)

    def get_file(self, obj):
        # to get all images that uploaded in a post
        images = Images.objects.filter(post=obj.id)
        return ImagesSerializer(images, many=True).data

    def get_tags_count(self, obj):
        # to get count of tags in a post
        return obj.tagged.count()

    def get_liked_count(self, obj):
        # to get post's liked count
        return obj.liked_user.count()

    def get_disliked_count(self, obj):
        # to get post's disliked count
        return obj.disliked_user.count()

    def get_liked(self, obj):
        # return True or False whether user liked the post or not
        return obj.liked_user.filter(id=self.context['user_id']).exists()

    def get_unliked(self, obj):
        # return True or False whether user liked the post or not
        return obj.disliked_user.filter(id=self.context['user_id']).exists()

    def get_user_tags_status(self, obj):
        # getting followed tags count of a user
        tags = obj.tagged.all()
        count = 0
        for item in tags:
            if FollowedTags.objects.filter(user=self.context['user_id'], tag=item.id, post=obj.id, is_followed=True).exists():
                count += FollowedTags.objects.filter(user=self.context['user_id'], tag=item.id, post=obj.id, is_followed=True).count()
            else:
                count -= FollowedTags.objects.filter(user=self.context['user_id'], tag=item.id, post=obj.id, is_followed=False).count()
        return count


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    liked_user = serializers.ListSerializer(child=serializers.CharField(source='liked_user.username'))
