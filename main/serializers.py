from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TimeSeries

class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class TimeSeriesSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format=None)
    full_name = serializers.CharField()
    age = serializers.IntegerField()
    department = serializers.CharField()
    wage = serializers.FloatField()

    class Meta:
        model = TimeSeries
        fields = '__all__'

from rest_pandas.serializers import PandasSerializer
class MyCustomPandasSerializer(PandasSerializer):
    def transform_dataframe(self, dataframe):
        dataframe.some_pivot_function(in_place=True)
        return dataframe