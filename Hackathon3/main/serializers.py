from rest_framework import serializers
from .models import *

# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Like
#         fields = ("user",)


class CommentSerializer(serializers.ModelSerializer):
    # comment_like = LikeSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    # recomments = RecommentSerializer(many=True, read_only=True)
    # reply = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "content",
            "created_at",
            "likes",
            "likes_count",
            # "recomments",
            # "relply"
        ]
        read_only_fields = ["author"]  # client가 수정하면 안되는 것들 read_only로 보호!!

    def get_likes_count(self, obj):
        return obj.likes.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if self.context["request"].resolver_match.urlname == "comment-list":
            data.pop("reply")
        return data

    """ def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data """


class RecommentSerializer(serializers.ModelSerializer):
    # recomment_like = LikeSerializer(many=True, read_only=True)
    relikes_count = serializers.SerializerMethodField()
    comment = CommentSerializer(many=True, read_only=True)
    reply = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "content",
            "created_at",
            "likes",
            "likes_count",
            # "recomments",
            "relply",
        )

    def get_likes_count(self, obj):
        return obj.likes.count()

    """ def get_relikes_count(self, obj):
        return obj.relikes.count() """

    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind("", self)
        return serializer.data


class CommentDetailSerializer(serializers.ModelSerializer):
    recomments = RecommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "content",
            "created_at",
            "likes",
            "likes_count",
            "recomments",
        )


class PostSerializer(serializers.ModelSerializer):
    # comment = CommentSerializer(many=True, read_only=True)
    scraps_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "image",
            "title",
            "painter",
            # "drawing_technique",
            # "work_year",
            # "content",
            # "type_choices",
            # "type",
            # "scraps",
            "scraps_count",
            # "created_at",
            # "comment",
            "comment_count",
        ]

    def get_scraps_count(self, obj):
        return obj.scraps.count()

    def get_comment_count(self, obj):
        return obj.comment.count()


class PosDetailSerializer(serializers.ModelSerializer):
    # comment = CommentSerializer(many=True, read_only=True)
    scraps_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            # "id",
            "image",
            "title",
            "painter",
            "drawing_technique",
            "work_year",
            "content",
            # "type_choices",
            "type",
            "scraps",
            "scraps_count",
            "created_at",
            # "comment",
            "comment_count",
        ]

    def get_scraps_count(self, obj):
        return obj.scraps.count()

    def get_comment_count(self, obj):
        return obj.comment.count()


class PostCommentSerializer(
    serializers.ModelSerializer
):  # Post 모델 인스턴스와 관련된 댓글 중 부모댓글 즉 comment만 가져와서 직렬화
    parent_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "parent_comments")

    def get_parent_comments(self, obj):
        parent_comments = obj.comments.filter(parent=None)
        serializer = CommentSerializer(parent_comments, many=True)
        return serializer.data
