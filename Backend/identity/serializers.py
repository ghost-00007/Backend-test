from rest_framework  import serializers
from .models import AppDetails,ModuleDetails,ComponentDetails,Roles,RolePermission


class AppDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppDetails  
        fields = '__all__'

class ModuleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleDetails  
        fields = '__all__'

class ComponentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentDetails  
        fields = '__all__'

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles  
        fields = '__all__'

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission  
        fields = '__all__'

class ComponentDetailsSerializer(serializers.ModelSerializer):
    component_id = serializers.IntegerField(source='id')

    class Meta:
        model = ComponentDetails
        fields = ['component_id', 'component_name']


class ModuleWithComponentsSerializer(serializers.ModelSerializer):
    App_id = serializers.IntegerField(source='app.id')
    app_name = serializers.CharField(source='app.app_name')
    module_id = serializers.IntegerField(source='id')
    component = serializers.SerializerMethodField()

    class Meta:
        model = ModuleDetails
        fields = ['App_id', 'app_name', 'module_id', 'module_name', 'component']

    def get_component(self, obj):
        components = ComponentDetails.objects.filter(module=obj)
        return ComponentDetailsSerializer(components, many=True).data
