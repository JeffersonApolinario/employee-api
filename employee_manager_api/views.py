from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer


def department_exists_by_id(id):
    try:
        department = Department.objects.get(id=id)
        return department
    except Department.DoesNotExist:
        return None

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def department_list_or_create(request):
    if request.method == 'GET':
        departments = Department.objects.all()
        paginator = LimitOffsetPagination()
        result = paginator.paginate_queryset(departments, request)
        serializer = DepartmentSerializer(result, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def employee_list_or_create(request):
    
    if request.method == 'GET':
        employees = Employee.objects.all()
        paginator = LimitOffsetPagination()
        result = paginator.paginate_queryset(employees, request)
        serializer = EmployeeSerializer(result, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            department = department_exists_by_id(request.data['department'])

            if (department == None):
                return Response({'errorMessage': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer.save(department=department)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def employee_findone_or_update_or_delete(request, id):
    try:
        employee = Employee.objects.get(id=id)
    except Employee.DoesNotExist:
        return Response({'errorMessage': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            department = department_exists_by_id(request.data['department'])

            if (department == None):
                return Response({'errorMessage': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer.save(department=department)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)