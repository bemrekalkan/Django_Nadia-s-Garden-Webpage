from rest_framework import serializers
from .models import Pizza, Size

class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = '__all__'
        # fields = ["id", "topping1", "last_name", "number"]
        # exclude = ['last_name']

class SizeSerializer(serializers.ModelSerializer):
    # sizes = serializers.StringRelatedField()
    class Meta:
        model = Size
        fields = ["id", "title"]