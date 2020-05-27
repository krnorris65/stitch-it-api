from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stitchitapi.models import Fabric

class FabricSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for fabric

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Fabric
        url = serializers.HyperlinkedIdentityField(
            view_name='fabric',
            lookup_field='id'
        )
        fields = ('id', 'type', 'count')

class Fabrics(ViewSet):
    """Fabrics for Stitch It"""
    def retrieve(self, request, pk=None):
        """Handle GET requests for single fabric

        Returns:
            Response -- JSON serialized fabric instance
        """
        try:
            fabric = Fabric.objects.get(pk=pk)
            serializer = FabricSerializer(fabric, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def list(self, request):
        """Handle GET requests to fabrics resource

        Returns:
            Response -- JSON serialized list of fabrics
        """
        fabrics = Fabric.objects.all()
        serializer = FabricSerializer(
            fabrics,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Fabric instance
        """
        newfabric = Fabric()
        newfabric.type = request.data["type"]
        newfabric.count = request.data["count"]
        newfabric.save()

        serializer = FabricSerializer(newfabric, context={'request': request})

        return Response(serializer.data)