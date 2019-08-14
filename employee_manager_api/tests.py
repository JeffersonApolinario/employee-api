from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee, Department
import json

class EmployeeTests(APITestCase):


    def setUp(self):
        url_department_create_or_list = reverse('department_list_or_create')
        url_create_or_list = reverse('employee_list_or_create')
        url_findone_or_update_or_delete = reverse('employee_findone_or_update_or_delete', args=[1])

        department = Department(name='IT')
        department.save()

        employee = Employee(name='jeff', email='apolinario.kl@gmail.com', department=department)
        employee.save()

        user = User.objects.create_superuser('admin', 'admin@contact.com', 'asdfgh')
        user.save()

        self.url_department_create_or_list = url_department_create_or_list
        self.url_create_or_list = url_create_or_list
        self.url_findone_or_update_or_delete = url_findone_or_update_or_delete
        self.department = department
        self.employee = employee
        self.user = user

        self.client.force_authenticate(user=user)

    def test_post_department_success(self):
       
        data = {'name': 'Financial' }
        response = self.client.post(self.url_department_create_or_list, data, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['name'], 'Financial')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_post_department_with_email_exists(self):
        
        data = {'name': 'IT' }
        response = self.client.post(self.url_department_create_or_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"name":["department with this name already exists."]}')
    
    def test_list_departments_success(self):

        response = self.client.get(self.url_department_create_or_list)
        content = json.loads(response.content)[0]
        self.assertEqual(content['id'], self.department.id)
        self.assertEqual(content['name'], self.department.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_employees_success(self):

        response = self.client.get(self.url_create_or_list)
        content = json.loads(response.content)[0]
        self.assertEqual(content['id'], self.employee.id)
        self.assertEqual(content['name'], self.employee.name)
        self.assertEqual(content['email'], self.employee.email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_findone_employee_success(self):

        response = self.client.get(self.url_findone_or_update_or_delete)
        content = json.loads(response.content)
        self.assertEqual(content['id'], self.employee.id)
        self.assertEqual(content['name'], self.employee.name)
        self.assertEqual(content['email'], self.employee.email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_findone_employee_not_found(self):

        url_findone_or_update_or_delete = reverse('employee_findone_or_update_or_delete', args=[2])
        response = self.client.get(url_findone_or_update_or_delete)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_employee_success(self):

        response = self.client.delete(self.url_findone_or_update_or_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_employee_not_found(self):
        
        url_findone_or_update_or_delete = reverse('employee_findone_or_update_or_delete', args=[2])
        response = self.client.delete(url_findone_or_update_or_delete)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_employee_success(self):
       
        data = {'name': 'jeff', 'email': 'other.kl@gmail.com', 'department': self.department.id}
        response = self.client.post(self.url_create_or_list, data, format='json')
        content = json.loads(response.content)
        self.assertEqual(content['name'], 'jeff')
        self.assertEqual(content['email'], 'other.kl@gmail.com')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_post_with_email_invalid(self):
        

        data = {'name': 'jeff', 'email': 'teste', 'department': self.department.id}
        response = self.client.post(self.url_create_or_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"email":["Enter a valid email address."]}')
    
    def test_post_with_email_exists(self):
        

        data = {'name': 'jeff', 'email': 'apolinario.kl@gmail.com', 'department': self.department.id}
        response = self.client.post(self.url_create_or_list, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"email":["employee with this email already exists."]}')

    def test_post_with_department_not_exists(self):

        data = {'name': 'jeff', 'email': 'other.kl@gmail.com', 'department': 2}
        response = self.client.post(self.url_create_or_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content, b'{"errorMessage":"Department not found"}')

    def test_put_employee_success(self):
        
        data = {'name': 'jeff', 'email': 'apolinario.kl@gmail.com', 'department': self.department.id}
        response = self.client.put(self.url_findone_or_update_or_delete, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_put_with_email_invalid(self):
        
        data = {'name': 'jeff', 'email': 'teste', 'department': self.department.id}
        response = self.client.put(self.url_findone_or_update_or_delete, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"email":["Enter a valid email address."]}')
    
    def test_put_with_email_exists(self):
        
        employee = Employee(name='maria', email='other.kl@gmail.com', department=self.department)
        employee.save()

        data = {'name': 'jeff', 'email': 'other.kl@gmail.com', 'department': self.department.id}
        response = self.client.put(self.url_findone_or_update_or_delete, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"email":["employee with this email already exists."]}')

    def test_put_with_department_not_exists(self):
    
        data = {'name': 'jeff', 'email': 'apolinario.kl@gmail.com', 'department': 2}
        response = self.client.put(self.url_findone_or_update_or_delete, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content, b'{"errorMessage":"Department not found"}')
    