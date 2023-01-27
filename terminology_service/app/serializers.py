from rest_framework import serializers

from . import models


class RefbookItemSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    
    class Meta:
        model = models.Directory
        fields = ['id', 'code', 'name']


class RefbooksResponseSerializer(serializers.Serializer):
    refbooks = serializers.ListField(child=RefbookItemSerializer())


class RefbookElementItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DirectoryElement
        fields = ['code', 'value']


class RefbooksElementsResponseSerializer(serializers.Serializer):
    elements = serializers.ListField(child=RefbookElementItemSerializer())


