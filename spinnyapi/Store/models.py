from django.db import models
from django.contrib.auth.models import User

class Box(models.Model):
    length = models.FloatField()
    breadth = models.FloatField()
    height = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


    def calculate_area(self):
        return 2*(self.length * self.breadth + self.length*self.height + self.height*self.breadth)


    def calculate_volume(self):
        return self.length * self.breadth * self.height
