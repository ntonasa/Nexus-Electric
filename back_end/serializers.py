from rest_framework import serializers
from back_end.models import *
from datetime import datetime, timezone

# Base Serializer
class BaseDatasetSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields_exclude = kwargs.pop('exclude', {})
        super(BaseDatasetSerializer, self).__init__(*args, **kwargs)
        
        for field in fields_exclude:
            self.fields.pop(field)
    
    Source = serializers.ReadOnlyField(default="entso-e")
    #Dataset = serializers.ReadOnlyField(default="Dataset")
    DateTimeUTC = serializers.DateTimeField(read_only=True, source="DateTime", format="%Y-%m-%d %H:%M:%S.%f")
    UpdateTimeUTC = serializers.DateTimeField(read_only=True, source="UpdateTime", format="%Y-%m-%d %H:%M:%S.%f")
    #AreaTypeCode = serializers.SlugRelatedField(read_only=True, source="AreaTypeCodeId", slug_field="AreaTypeCodeText")
    AreaTypeCode = serializers.CharField(read_only=True, source="AreaTypeCodeId__AreaTypeCodeText")
    #MapCode = serializers.SlugRelatedField(read_only=True, source="MapCodeId", slug_field="MapCodeText")
    MapCode = serializers.CharField(read_only=True, source="MapCodeId__MapCodeText")
    #ResolutionCode = serializers.SlugRelatedField(read_only=True, source="ResolutionCodeId", slug_field="ResolutionCodeText")
    ResolutionCode = serializers.CharField(read_only=True, source="ResolutionCodeId__ResolutionCodeText")

    def to_internal_value(self, data):
        tmpcreate = data['EntityCreatedAt']
        tmpmodified = data['EntityModifiedAt']
        tmpdatetime = data['DateTime']
        tmpupdatime = data['UpdateTime']
        if 'ProductionTypeId' in data:
            data['ProductionTypeId'] = ProductionType.objects.get(Id=data['ProductionTypeId'])
        data['AreaTypeCodeId'] = AreaTypeCode.objects.get(Id=data['AreaTypeCodeId'])
        data['MapCodeId'] = MapCode.objects.get(Id=data['MapCodeId'])
        data['AreaCodeId'] = AllocatedEICDetail.objects.get(Id=data['AreaCodeId'])
        data['ResolutionCodeId'] = ResolutionCode.objects.get(Id=data['ResolutionCodeId'])
        data['EntityCreatedAt'] = datetime.strptime((tmpcreate[:26]+tmpcreate[27:]).strip(), '%Y-%m-%d  %H:%M:%S.%f %z')
        data['EntityModifiedAt'] = datetime.strptime((tmpmodified[:26]+tmpmodified[27:]).strip(), '%Y-%m-%d  %H:%M:%S.%f %z')
        data['DateTime'] = datetime.strptime((tmpdatetime[:26]+tmpdatetime[27:]).strip(), '%Y-%m-%d  %H:%M:%S.%f').replace(tzinfo=timezone.utc)
        data['UpdateTime'] = datetime.strptime((tmpupdatime[:26]+tmpupdatime[27:]).strip(), '%Y-%m-%d  %H:%M:%S.%f').replace(tzinfo=timezone.utc)
        return data

# Actual Total Load
class ActualTotalLoadSerializer(BaseDatasetSerializer):
    Dataset = serializers.ReadOnlyField(default="ActualTotalLoad")
    ActualTotalLoadValue = serializers.FloatField(read_only=True,source="TotalLoadValue", required=False)
    ActualTotalLoadByDayValue = serializers.FloatField(read_only=True, required=False)
    ActualTotalLoadByMonthValue = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = ActualTotalLoad
        fields = ['Source', 'Dataset', 'AreaName', 'AreaTypeCode', 'MapCode', 
                'ResolutionCode', 'Year', 'Month', 'Day', 'DateTimeUTC', 'ActualTotalLoadValue', 
                'ActualTotalLoadByDayValue', 'ActualTotalLoadByMonthValue', 'UpdateTimeUTC']

# Day Ahead Total Load Forecast
class DayAheadTotalLoadForecastSerializer(BaseDatasetSerializer):
    Dataset = serializers.ReadOnlyField(default="DayAheadTotalLoadForecast")
    DayAheadTotalLoadForecastValue = serializers.FloatField(read_only=True, source="TotalLoadValue", required=False)
    DayAheadTotalLoadForecastByDayValue = serializers.FloatField(read_only=True, required=False)
    DayAheadTotalLoadForecastByMonthValue = serializers.FloatField(read_only=True, required=False)
    
    
    class Meta:
        model = DayAheadTotalLoadForecast
        fields = ['Source', 'Dataset', 'AreaName', 'AreaTypeCode', 
                'MapCode', 'ResolutionCode', 'Year', 'Month', 'Day', 
                'DateTimeUTC', 'DayAheadTotalLoadForecastValue', 'DayAheadTotalLoadForecastByDayValue', 
                'DayAheadTotalLoadForecastByMonthValue', 'UpdateTimeUTC']

# Aggregated Generation Per Type
class AggregatedGenerationPerTypeSerializer(BaseDatasetSerializer):
    Dataset = serializers.ReadOnlyField(default="AggregatedGenerationPerType")
    ProductionType = serializers.CharField(read_only=True, source="ProductionTypeId__ProductionTypeText")
    ActualGenerationOutputValue = serializers.FloatField(read_only=True, source="ActualGenerationOutput", required=False)
    ActualGenerationOutputByDayValue = serializers.FloatField(read_only=True, required=False)
    ActualGenerationOutputByMonthValue = serializers.FloatField(read_only=True, required=False)
    
    class Meta:
        model = AggregatedGenerationPerType
        fields = ['Source', 'Dataset', 'AreaName', 'AreaTypeCode', 'MapCode', 
                'ResolutionCode', 'Year', 'Month', 'Day', 'DateTimeUTC', 
                'ProductionType', 'ActualGenerationOutputValue', 'ActualGenerationOutputByDayValue', 
                'ActualGenerationOutputByMonthValue', 'UpdateTimeUTC']

# # User Serializer
class NexusUserSerializer(serializers.ModelSerializer):
    quota = serializers.IntegerField(source="nexususer.quota")
    API_key = serializers.CharField(source="auth_token.key",read_only=True)

    class Meta:
        model = User
        fields = ['username', 'API_key', 'email', 'quota']

    def update(self, instance, validated_data):
        nexususer_data = validated_data.pop('nexususer')

        nexususer = instance.nexususer

        instance.username = instance.username
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        nexususer.quota = nexususer_data.get('quota', nexususer.quota)
        nexususer.save()

        return instance
