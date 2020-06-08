from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stitchitapi.models import Fabric, Size, Design, Stitcher
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser


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
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

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
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Design instance
        """
        fabric = Fabric.objects.get(pk=request.data['fabric_id'])
        size = Size.objects.get(pk=request.data['size_id'])
        stitcher = Stitcher.objects.get(user=request.auth.user)

        newdesign = Design()
        newdesign.title = request.data["title"]
        newdesign.description = request.data["description"]
        newdesign.completed_date = request.data["completed_date"]
        newdesign.photo = request.data["photo"]
        newdesign.fabric = fabric
        newdesign.size = size
        newdesign.stitcher = stitcher
        newdesign.save()

        serializer = DesignSerializer(newdesign, context={'request': request})

        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a design. The user can only edit their own designs

        Returns:
            Response -- Empty body with 204 status code or 403 error code
        """
        requesting_user = Stitcher.objects.get(user=request.auth.user)
        design = Design.objects.get(pk=pk)
        if design.stitcher == requesting_user:
            fabric = Fabric.objects.get(pk=request.data['fabric_id'])
            size = Size.objects.get(pk=request.data['size_id'])

            design.title = request.data["title"]
            design.description = request.data["description"]
            design.completed_date = request.data["completed_date"]
            design.photo = request.data["photo"]
            design.fabric = fabric
            design.size = size
            design.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': "Not authorized to edit this design"}, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single design. The user can only delete their own designs

        Returns:
            Response -- 200, 403, 404, or 500 status code
        """
        try:
            requesting_user = Stitcher.objects.get(user=request.auth.user)
            design = Design.objects.get(pk=pk)
            if design.stitcher == requesting_user:
                design.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': "Not authorized to delete this design"}, status=status.HTTP_403_FORBIDDEN)

        except Design.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
