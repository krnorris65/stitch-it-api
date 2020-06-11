from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stitchitapi.models import Stitcher, Follow
import operator


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
        fields = ('id', 'follower_id', 'stitcher_id', 'pending', 'stitcher')
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
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Follow instance
        """
        follower = Stitcher.objects.get(user=request.auth.user)
        stitcher = Stitcher.objects.get(pk=request.data["stitcher_id"])
        newfollow = Follow()
        newfollow.follower = follower
        newfollow.stitcher = stitcher
        # if public profile is true then the request is not pending, if public profile is false then the request is pending
        newfollow.pending = operator.not_(stitcher.public_profile)

        newfollow.save()

        serializer = FollowSerializer(newfollow, context={'request': request})

        return Response(serializer.data)
