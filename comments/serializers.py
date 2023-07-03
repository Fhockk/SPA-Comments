from PIL import Image
from io import BytesIO
from rest_framework import serializers
from django.core.files.base import ContentFile
from django.template.defaultfilters import filesizeformat

from comments.models import Comment

ALLOWED_IMAGE_FORMATS = ['JPEG', 'GIF', 'PNG']


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
        'id', 'author', 'home_page', 'content', 'image', 'text_file', 'created_at', 'updated_at', 'parent', 'replies'
        )

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all().order_by('-created_at'), many=True).data
        return None

        # img[0] - width, img[1] - height
    def validate_image(self, image):
        if image:
            try:
                with Image.open(image) as img:
                    img.verify()
            except Exception:
                raise serializers.ValidationError("Invalid image file")

            img = Image.open(image)

            if img.format.upper() not in ALLOWED_IMAGE_FORMATS:
                raise serializers.ValidationError(f'Unsupported image format. Use one of {ALLOWED_IMAGE_FORMATS}')

            if img.size[0] > 320 or img.size[1] > 240:
                ratio = min(320 / img.size[0], 240 / img.size[1])
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                new_img = img.resize(new_size, Image.ANTIALIAS)
                new_img_io = BytesIO()
                new_img.save(new_img_io, format=img.format)
                image.file = ContentFile(new_img_io.getvalue(), name=image.name)
        return image

    def validate_text_file(self, file):
        if file:
            if file.size > 100 * 1024:
                raise serializers.ValidationError('Size of the text file should not exceed 100 kB. ' +
                                                  f'Your file size is {filesizeformat(file.size)}.')
            if not file.name.endswith('.txt'):
                raise serializers.ValidationError('Invalid file format. Only .txt format is accepted.')
        return file

    def create(self, validated_data):
        if 'text_file' in validated_data:
            validated_data['text_file'] = self.validate_text_file(validated_data['text_file'])
        comment = super().create(validated_data)
        return comment

    def update(self, instance, validated_data):
        if 'image' in validated_data:
            instance.image = self.validate_image(validated_data['image'])
        if 'text_file' in validated_data:
            instance.text_file = self.validate_text_file(validated_data['text_file'])
        return super().update(instance, validated_data)
