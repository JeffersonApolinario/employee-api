from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, related_name='department', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
