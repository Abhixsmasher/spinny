from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import generics, permissions

class Box(models.Model):
    length = models.FloatField()
    breadth = models.FloatField()
    height = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def calculate_area(self):
        return self.length * self.breadth

    def calculate_volume(self):
        return self.length * self.breadth * self.height

class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_staff

class IsBoxCreatorOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user or request.user.is_staff

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

class BoxListAPIView(generics.ListCreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsStaffUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class BoxDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [IsStaffOrReadOnly, IsBoxCreatorOrStaff]
