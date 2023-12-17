from rest_framework import generics, permissions
from .models import Box
from .serializers import BoxSerializer
from .permissions import IsBoxCreatorOrStaff, IsStaffOrReadOnly
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from django.db import transaction
from django.db.models import Sum,F,Count
from django.http import Http404

def check_average_area():
    total_area = Box.objects.aggregate(total_area=Sum(2*((F('length') * F('breadth')) + (F('height')*F('breadth'))+(F('length')*F('height')))))['total_area']
    total_boxes = Box.objects.count()
    A1 = 100  
    average_area = total_area / total_boxes if total_boxes > 0 else 0
    if average_area > A1:
        raise Exception("Average area condition not met")
    return

def check_average_volume(user):
    total_volume = Box.objects.filter(created_by=user).aggregate(total_volume=Sum(F('length') * F('breadth') * F('height')))['total_volume']
    total_user_boxes = Box.objects.filter(created_by=user).count()
    V1 = 1000  
    if total_user_boxes > 0 and total_volume / total_user_boxes > V1:
        raise Exception("Average volume condition not met")
    return

def check_total_boxes_added():
    one_week_ago = timezone.now() - timedelta(days=7)
    total_boxes_in_week = Box.objects.filter(creation_date__gte=one_week_ago).count()
    L1 = 100 
    if total_boxes_in_week > L1:
        raise Exception("Total boxes added condition not met")
    return

def check_total_boxes_added_by_user(user):
    one_week_ago = timezone.now() - timedelta(days=7)
    total_boxes_added_by_user = Box.objects.filter(created_by=user, creation_date__gte=one_week_ago).count()
    L2 = 50 
    if total_boxes_added_by_user > L2:
        raise Exception("Total boxes added by user condition not met")
    return

def checks(user):
    check_average_area()
    check_average_volume(user)
    check_total_boxes_added()
    check_total_boxes_added_by_user(user)
    return

class BoxListAPIView(generics.ListCreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser,IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser or self.request.user.is_active:
            return BoxSerializer
        else:
            class NonStaffBoxSerializer(BoxSerializer):
                class Meta(BoxSerializer.Meta):
                    exclude = ['created_by', 'last_updated']
            return NonStaffBoxSerializer

    def get_queryset(self):
        queryset = Box.objects.all()
        length_more_than = self.request.query_params.get('length_more_than')
        if length_more_than:
            queryset = queryset.filter(length__gt=length_more_than)

        length_less_than = self.request.query_params.get('length_less_than')
        if length_less_than:
            queryset = queryset.filter(length__lt=length_less_than)
        
        breadth_less_than = self.request.query_params.get('breadth_less_than')
        if breadth_less_than:
            queryset = queryset.filter(breadth__lt=breadth_less_than)

        breadth_more_than = self.request.query_params.get('breadth_more_than')
        if breadth_more_than:
            queryset = queryset.filter(breadth__lt=breadth_more_than)
        
        height_less_than = self.request.query_params.get('height_less_than')
        if height_less_than:
            queryset = queryset.filter(height__lt=height_less_than)

        height_more_than = self.request.query_params.get('height_more_than')
        if height_more_than:
            queryset = queryset.filter(height__lt=height_more_than)

        area_less_than = self.request.query_params.get('area_less_than')
        if area_less_than:
            queryset = queryset.filter(area__lt=area_less_than)

        area_more_than = self.request.query_params.get('area_more_than')
        if breadth_more_than:
            queryset = queryset.filter(area__lt=area_more_than)

        volume_less_than = self.request.query_params.get('volume_less_than')
        if volume_less_than:
            queryset = queryset.filter(volume__lt=volume_less_than)

        volume_more_than = self.request.query_params.get('volume_more_than')
        if volume_more_than:
            queryset = queryset.filter(volume__lt=volume_more_than)

        created_by_username = self.request.query_params.get('created_by_username')
        if created_by_username:
            queryset = queryset.filter(created_by__username=created_by_username)

        created_before = self.request.query_params.get('created_before')
        if created_before:
            created_before_date = datetime.strptime(created_before, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            queryset = queryset.filter(creation_date__lt=created_before_date)

        created_after = self.request.query_params.get('created_after')
        if created_after:
            created_after_date = datetime.strptime(created_after, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            queryset = queryset.filter(creation_date__gt=created_after_date)

        return queryset

class UserBoxesAPIView(generics.ListAPIView):
    serializer_class = BoxSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, IsStaffOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Box.objects.filter(created_by=user)

        length_more_than = self.request.query_params.get('length_more_than')
        if length_more_than:
            queryset = queryset.filter(length__gt=length_more_than)

        length_less_than = self.request.query_params.get('length_less_than')
        if length_less_than:
            queryset = queryset.filter(length__lt=length_less_than)
        
        breadth_less_than = self.request.query_params.get('breadth_less_than')
        if breadth_less_than:
            queryset = queryset.filter(breadth__lt=breadth_less_than)

        breadth_more_than = self.request.query_params.get('breadth_more_than')
        if breadth_more_than:
            queryset = queryset.filter(breadth__lt=breadth_more_than)
        
        height_less_than = self.request.query_params.get('height_less_than')
        if height_less_than:
            queryset = queryset.filter(height__lt=height_less_than)

        height_more_than = self.request.query_params.get('height_more_than')
        if height_more_than:
            queryset = queryset.filter(height__lt=height_more_than)

        area_less_than = self.request.query_params.get('area_less_than')
        if area_less_than:
            queryset = queryset.filter(area__lt=area_less_than)

        area_more_than = self.request.query_params.get('area_more_than')
        if breadth_more_than:
            queryset = queryset.filter(area__lt=area_more_than)

        volume_less_than = self.request.query_params.get('volume_less_than')
        if volume_less_than:
            queryset = queryset.filter(volume__lt=volume_less_than)

        volume_more_than = self.request.query_params.get('volume_more_than')
        if volume_more_than:
            queryset = queryset.filter(volume__lt=volume_more_than)
        
        return queryset

class BoxAddAPIView(generics.CreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser,IsStaffOrReadOnly]

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(created_by=self.request.user)
            self.check_conditions_after_create()
    
    def check_conditions_after_create(self):
        user=self.request.user
        checks(user)

class BoxDeleteAPIView(generics.DestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser,IsStaffOrReadOnly]

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.delete()
            self.check_conditions_after_delete()

    def check_conditions_after_delete(self):
        user=self.request.user
        checks(user)


class BoxUpdateAPIView(generics.UpdateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [IsStaffOrReadOnly, IsBoxCreatorOrStaff, IsStaffOrReadOnly]
    def perform_update(self, serializer):
        with transaction.atomic():
            serializer.save(created_by=self.get_object().created_by, creation_date=self.get_object().creation_date)
            self.check_conditions_after_update()

    def check_conditions_after_update(self):
        user=self.request.user
        checks(user)
    


