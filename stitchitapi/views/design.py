from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stitchitapi.models import Fabric, Size, Design

class DesignSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for design

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Design
        url = serializers.HyperlinkedIdentityField(
            view_name='design',
            lookup_field='id'
        )
        fields = ('id', 'title', 'description', 'completed_date', 'photo', 'fabric', 'size', 'stitcher_id')
        depth = 2

class Designs(ViewSet):
    """Designs for Stitch It"""
    def retrieve(self, request, pk=None):
        """Handle GET requests for single design

        Returns:
            Response -- JSON serialized design instance
        """
        try:
            design = Design.objects.get(pk=pk)
            serializer = DesignSerializer(design, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def list(self, request):
        """Handle GET requests to designs resource

        Returns:
            Response -- JSON serialized list of designs
        """
        designs = Design.objects.all()
        serializer = DesignSerializer(
            designs,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)