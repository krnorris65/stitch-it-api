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
    
    def update(self, request, pk=None):
        """Handle PUT requests for a follow. User can update the pending status for follows where they are the  stitcher

        Returns:
            Response -- Empty body with 204 status code or 403 error code
        """
        requesting_user = Stitcher.objects.get(user=request.auth.user)
        follow = Follow.objects.get(pk=pk)

        if follow.stitcher == requesting_user:
            follow.pending = request.data["pending"]
            follow.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': "Not authorized to edit this follow"}, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single follow. The user can only delete their own follows or follows they are the stitcher on

        Returns:
            Response -- 200, 403, 404, or 500 status code
        """
        try:
            requesting_user = Stitcher.objects.get(user=request.auth.user)
            follow = Follow.objects.get(pk=pk)
            if follow.follower == requesting_user or follow.stitcher == requesting_user:
                follow.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': "Not authorized to delete this follow"}, status=status.HTTP_403_FORBIDDEN)

        except Follow.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)