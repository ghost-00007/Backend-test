from rest_framework  import serializers
from .models import Department,Project,Teams,Designation


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department  
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(format="%d-%m-%Y", input_formats=["%d-%m-%Y"])
    end_date = serializers.DateField(format="%d-%m-%Y", input_formats=["%d-%m-%Y"])
    class Meta:
        model = Project  
        fields = '__all__'

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams  
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation  
        fields = '__all__'