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

        size_param = self.request.query_params.get('size', None)

        if size_param is not None:
            sizes = sizes.filter(size=size_param)

        serializer = SizeSerializer(
            sizes,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized size instance
        """
        newsize = Size()
        newsize.size = request.data["size"]
        newsize.save()

        serializer = SizeSerializer(newsize, context={'request': request})

        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a size

        Returns:
            Response -- Empty body with 204 status code
        """
        size = Size.objects.get(pk=pk)
        size.size = request.data["size"]
        size.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single size

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            size = Size.objects.get(pk=pk)
            size.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Size.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
