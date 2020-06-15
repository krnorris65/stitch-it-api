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

        type_param = self.request.query_params.get('type', None)
        count_param = self.request.query_params.get('count', None)

        if type_param is not None:
            fabrics = fabrics.filter(type=type_param)

        if count_param is not None:
            fabrics = fabrics.filter(count=count_param)

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
    
    def update(self, request, pk=None):
        """Handle PUT requests for a fabric

        Returns:
            Response -- Empty body with 204 status code
        """
        fabric = Fabric.objects.get(pk=pk)
        fabric.type = request.data["type"]
        fabric.count = request.data["count"]
        fabric.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single fabric

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            fabric = Fabric.objects.get(pk=pk)
            fabric.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Fabric.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)