from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stitchitapi.models import Stitcher, Follow

class FollowSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for follow

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Follow
        url = serializers.HyperlinkedIdentityField(
            view_name='follow',
            lookup_field='id'
        )
        fields = ('id', 'follower_id', 'stitcher_id', 'pending')
        depth = 2

class Follows(ViewSet):
    """Follows for Stitch It"""
    def retrieve(self, request, pk=None):
        """Handle GET requests for single follow

        Returns:
            Response -- JSON serialized follow instance
        """
        try:
            follow = Follow.objects.get(pk=pk)
            serializer = FollowSerializer(follow, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def list(self, request):
        """Handle GET requests to follows resource

        Returns:
            Response -- JSON serialized list of follows
        """
        follows = Follow.objects.all()
        serializer = FollowSerializer(
            follows,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)