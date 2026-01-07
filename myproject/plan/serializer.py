from rest_framework import serializers
from .models import Plan

class PlanSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length = 20)
    duration = serializers.IntegerField(default=0)
    created_at = serializers.DateTimeField(read_only=True)


    class Meta:
        model = Plan
        fields = '__all__'
