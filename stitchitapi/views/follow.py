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