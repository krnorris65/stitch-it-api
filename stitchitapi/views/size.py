from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stitchitapi.models import Size

class SizeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Size

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Size
        url = serializers.HyperlinkedIdentityField(
            view_name='size',
            lookup_field='id'
        )
        fields = ('id', 'size')

class Sizes(ViewSet):
    """Sizes for Stitch It"""
    def retrieve(self, request, pk=None):
        """Handle GET requests for single size

        Returns:
            Response -- JSON serialized fabric instance
        """
        try:
            size = Size.objects.get(pk=pk)
            serializer = SizeSerializer(size, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def list(self, request):
        """Handle GET requests to sizes resource

        Returns:
            Response -- JSON serialized list of sizes
        """
        sizes = Size.objects.all()
        serializer = SizeSerializer(
            sizes,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
