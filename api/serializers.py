from rest_framework import serializers
from category.models import Category
from product.models import Product
from image.models import Image
from django.conf import settings
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = '__all__'
    def get_image_url(self, obj):
        if settings.DEBUG:  # debug enabled for dev and stage
            return '%s%s%s' % (settings.API_DOMAIN, settings.MEDIA_URL, obj.image.url)
        return obj.img.url
# class ProductSerializer(serializers.ModelSerializer):
#     images = ImageSerializer(many=True, read_only=True)  # Nested serializer for images

#     class Meta:
#         model = Product
#         fields = (['id','images'])



class ProductSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()

    def get_thumbnail_url(self, obj):
        return obj.get_thumbnail_url()
    image = ImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True)
    
    class Meta:
        model = Product
        fields = [ "id","image","uploaded_images","thumbnail_url",'category']
    
    
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            newproduct_image = Image.objects.create(product=product, image=image)
        return product        
