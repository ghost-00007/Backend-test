from rest_framework import serializers
from .models import User
from project_management.serializers import DepartmentSerializer, DesignationSerializer, TeamsSerializer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)

    department = DepartmentSerializer(read_only=True)
    designation = DesignationSerializer(read_only=True)
    team = TeamsSerializer(read_only=True)
    reporting_manager = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_reporting_manager(self, obj):
        if obj.reporting_manager:
            return {
                "id": obj.reporting_manager.id,
                "employee_name": obj.reporting_manager.employee_name,
                "email": obj.reporting_manager.email
            }
        return None
