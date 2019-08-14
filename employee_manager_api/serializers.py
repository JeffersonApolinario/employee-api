from rest_framework import serializers
from .models import Employee, Department


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'name', 'created_at']


class EmployeeSerializer(serializers.ModelSerializer):

    department = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'created_at', 'department']
        read_only_fields = ('created_at', 'id')

