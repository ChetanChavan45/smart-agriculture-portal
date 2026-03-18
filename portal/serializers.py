from rest_framework import serializers
from .models import User, Crop, FarmerQuery, ExpertResponse

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'

class ExpertResponseSerializer(serializers.ModelSerializer):
    expert = UserSerializer(read_only=True)
    class Meta:
        model = ExpertResponse
        fields = '__all__'

class FarmerQuerySerializer(serializers.ModelSerializer):
    farmer = UserSerializer(read_only=True)
    response = ExpertResponseSerializer(read_only=True)

    class Meta:
        model = FarmerQuery
        fields = '__all__'
        read_only_fields = ('farmer', 'is_answered', 'date_created')
