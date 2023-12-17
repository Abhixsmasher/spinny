from rest_framework import serializers
from .models import Box

class BoxSerializer(serializers.ModelSerializer):
    area = serializers.SerializerMethodField()
    volume = serializers.SerializerMethodField()

    class Meta:
        model = Box
        fields = ['id', 'length', 'breadth', 'height', 'area', 'volume', 'created_by', 'creation_date', 'last_updated']
        read_only_fields = ['created_by', 'creation_date', 'last_updated']

    def get_area(self, obj):
        return obj.calculate_area()

    def get_volume(self, obj):
        return obj.calculate_volume()
