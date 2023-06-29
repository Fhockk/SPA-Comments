from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
        'id', 'author', 'home_page', 'content', 'image', 'text_file', 'created_at', 'updated_at', 'parent', 'replies'
        )

    def get_replies(self, obj):
        if obj.replies:
            return CommentSerializer(obj.replies.all(), many=True).data
        return None

    def create(self, validated_data):
        comment = super().create(validated_data)
        comment.clean()
        comment.save()
        return comment
