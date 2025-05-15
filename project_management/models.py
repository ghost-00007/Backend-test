from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.timezone import now
from django.conf import settings

class Department(models.Model):
    department_code = models.CharField(max_length=25, blank=True, null=False, unique=True)
    department_name = models.CharField(max_length=25, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "department_details"

class Project(models.Model):
    project_code = models.CharField(max_length=25, blank=True, null=False, unique=True)
    project_name = models.CharField(max_length=25, blank=True, unique=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    manager = models.CharField(max_length=25, blank=True, null=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    milestone = models.IntegerField(blank=True, null=False)
    budget = models.IntegerField(blank=True, null=False)
    resource_allocation_front_end = models.JSONField(blank=True, null=True)
    resource_allocation_back_end = models.JSONField(blank=True, null=True)
    resource_allocation_ba = models.JSONField(blank=True, null=True)
    resource_allocation_tester = models.JSONField(blank=True, null=True)
    resource_allocation_design = models.JSONField(blank=True, null=True)
    resource_allocation_project_coordinator = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "project_details"


class Teams(models.Model):
    team_name = models.CharField(max_length=25, blank=True, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "team_details"

class Designation(models.Model):
    department= models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.CharField(max_length=25, blank=True, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "designation_details"

