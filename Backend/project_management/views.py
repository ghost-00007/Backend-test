from functools import partial

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import DepartmentSerializer,ProjectSerializer,TeamsSerializer,DesignationSerializer
from .models import Department,Project,Teams,Designation
# from users.serializers import UserSerializer
# from users.views import IsSuperUser
# from users.models import User


class DepartmentView(APIView):
    permission_classes = [IsAuthenticated]

class DepartmentView(APIView):  # Assuming you're using APIView
    def post(self, request):
        department_code = request.data.get("department_code")
        department_name = request.data.get("department_name")

        if department_name:
            department_name = "_".join(word.capitalize() for word in department_name.strip().split())

        if department_code:
            department_code = department_code.strip().upper()

        data = {
            "department_code": department_code,
            "department_name": department_name,
        }

        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Department details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Failed to add Department details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            department = get_object_or_404(Department, pk=pk)
            serializer = DepartmentSerializer(department)
            data = serializer.data
        else:
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            data = serializer.data

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        department_code = request.data.get("department_code", department.department_code)
        department_name = request.data.get("department_name", department.department_name)

        data = {
            "department_code": department_code,
            "department_name": department_name,
        }

        serializer = DepartmentSerializer(department, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Department details updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "message": "Failed to update Department details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return Response({
            "status": True,
            "message": "Department deleted successfully."
        }, status=status.HTTP_200_OK)
    

class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project_code = request.data.get("project_code")
        project_name = request.data.get("project_name")
        description = request.data.get("description")
        manager = request.data.get("manager")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        milestone = request.data.get("milestone")
        budget = request.data.get("budget")
        resource_allocation_front_end = request.data.get("resource_allocation_front_end")
        resource_allocation_back_end = request.data.get("resource_allocation_back_end")
        resource_allocation_ba = request.data.get("resource_allocation_ba")
        resource_allocation_tester = request.data.get("resource_allocation_tester")
        resource_allocation_design = request.data.get("resource_allocation_design")
        resource_allocation_project_coordinator = request.data.get("resource_allocation_project_coordinator")

        # Capitalize project_name
        if project_name:
            project_name = " ".join(word.capitalize() for word in project_name.strip().split())

        # Check for duplicate project name (case-insensitive)
        if Project.objects.filter(project_name__iexact=project_name).exists():
            return Response({
                "status": False,
                "message": "Project with this name already exists.",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "project_code": project_code,
            "project_name": project_name,
            "description": description,
            "manager": manager,
            "start_date": start_date,
            "end_date": end_date,
            "milestone": milestone,
            "budget": budget,
            "resource_allocation_front_end": resource_allocation_front_end,
            "resource_allocation_back_end": resource_allocation_back_end,
            "resource_allocation_ba": resource_allocation_ba,
            "resource_allocation_tester": resource_allocation_tester,
            "resource_allocation_design": resource_allocation_design,
            "resource_allocation_project_coordinator": resource_allocation_project_coordinator,
        }

        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Project details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Failed to add Project details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            project = get_object_or_404(Project, pk=pk)
            serializer = ProjectSerializer(project)
            data = serializer.data
        else:
            project = Project.objects.all()
            serializer = ProjectSerializer(project, many=True)
            data = serializer.data

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project_code = request.data.get("project_code", project.project_code)
        project_name = request.data.get("project_name", project.project_name)
        description = request.data.get("description", project.description)
        manager = request.data.get("manager", project.manager)
        start_date = request.data.get("start_date", project.start_date)
        end_date = request.data.get("end_date", project.end_date)
        milestone = request.data.get("milestone", project.milestone)
        budget = request.data.get("budget", project.budget)
        resource_allocation_front_end = request.data.get("resource_allocation_front_end", project.resource_allocation_front_end)
        resource_allocation_back_end = request.data.get("resource_allocation_back_end", project.resource_allocation_back_end)
        resource_allocation_ba = request.data.get("resource_allocation_ba", project.resource_allocation_ba)
        resource_allocation_tester = request.data.get("resource_allocation_tester", project.resource_allocation_tester)
        resource_allocation_design = request.data.get("resource_allocation_design", project.resource_allocation_design)
        resource_allocation_project_coordinator = request.data.get("resource_allocation_project_coordinator", project.resource_allocation_project_coordinator)

        data = {
            "project_code": project_code,
            "project_name": project_name,
            "description": description,
            "manager": manager,
            "start_date": start_date,
            "end_date": end_date,
            "milestone": milestone,
            "budget": budget,
            "resource_allocation_front_end": resource_allocation_front_end,
            "resource_allocation_back_end": resource_allocation_back_end,
            "resource_allocation_ba": resource_allocation_ba,
            "resource_allocation_tester": resource_allocation_tester,
            "resource_allocation_design": resource_allocation_design,
            "resource_allocation_project_coordinator": resource_allocation_project_coordinator,
        }

        serializer = ProjectSerializer(project, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Project details updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "message": "Failed to update Project details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response({
            "status": True,
            "message": "Project deleted successfully."
        }, status=status.HTTP_200_OK)
    
class TeamsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        team_name = request.data.get("team_name")

        if team_name:
            team_name = " ".join(word.capitalize() for word in team_name.strip().split())

        data = {
            "team_name": team_name,
        }

        serializer = TeamsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Teams details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Failed to add Teams details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            teams = get_object_or_404(Teams, pk=pk)
            serializer = TeamsSerializer(teams)
            data = serializer.data
        else:
            teams = Teams.objects.all()
            serializer = TeamsSerializer(teams, many=True)
            data = serializer.data

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        teams = get_object_or_404(Teams, pk=pk)
        team_name = request.data.get("team_name", teams.team_name)

        data = {
            "team_name": team_name,
        }

        serializer = TeamsSerializer(teams, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Teams details updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "message": "Failed to update Teams details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        teams = get_object_or_404(Teams, pk=pk)
        teams.delete()
        return Response({
            "status": True,
            "message": "Teams deleted successfully."
        }, status=status.HTTP_200_OK)
    
class DesignationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        department = request.data.get("department_id")
        designation = request.data.get("designation")

        data = {
            "department": department,
            "designation": designation,
        }

        serializer = DesignationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Designation details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Failed to add Designation details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            designation = get_object_or_404(Designation, pk=pk)
            serializer = DesignationSerializer(designation)
            data = serializer.data
        else:
            designation = Designation.objects.all()
            serializer = DesignationSerializer(designation, many=True)
            data = serializer.data

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        designation = get_object_or_404(Department, pk=pk)
        department = request.data.get("department_id", designation.department)
        designation = request.data.get("designation", designation.designation)

        data = {
            "department": department,
            "designation": designation,
        }

        serializer = DesignationSerializer(designation, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Designation details updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "message": "Failed to update Designation details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        designation = get_object_or_404(Designation, pk=pk)
        designation.delete()
        return Response({
            "status": True,
            "message": "Designation deleted successfully."
        }, status=status.HTTP_200_OK)