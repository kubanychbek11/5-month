from rest_framework import serializers
from .models import Category, Product, Review, Tag
from rest_framework.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):

    # rating = ReviewSerializer(many=True)
    class Meta:
        model = Product
        fields = "id title description price category_name".split()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name products_count products_list'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id stars text product_title'.split()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'title rating'.split()


'''VALIDATE'''

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=100)
class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=100)
    price = serializers.IntegerField()
    description = serializers.CharField(required=False, default='No description')
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField())

    '''EXTRA-TASK'''

    def validate_genres(self, tags):
        filtered_tags = Tag.objects.filter(id__in=tags)  # QuerySet of existed tags
        if len(tags) == filtered_tags.count():  # validating
            return tags

        lst_ = {i['id'] for i in filtered_tags.values_list().values()}  # creating set of existed tags

        raise ValidationError(f'This ids doesnt exist {set(tags).difference(lst_)}')  # collecting errors

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError(f"Error! {category_id} does not exists")
        return category_id

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=4, max_length=100)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Review.objects.get(product_id=product_id)
        except Review.DoesNotExist:
            raise ValidationError('Product not found!')