from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stitchitapi.models import Stitcher
from django.contrib.auth.models import User


class StitcherSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for stitcher

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Stitcher
        url = serializers.HyperlinkedIdentityField(
            view_name='stitcher',
            lookup_field='id'
        )
        fields = ('id', 'user_id', 'public_profile', 'user')
        depth = 1

class Stitchers(ViewSet):
    """Stitchers for Stitch It"""
    def retrieve(self, request, pk=None):
        """Handle GET requests for single stitcher

        Returns:
            Response -- JSON serialized fabric instance
        """
        try:
            stitcher = Stitcher.objects.get(pk=pk)
            serializer = StitcherSerializer(stitcher, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def list(self, request):
        """Handle GET requests to stitchers resource

        Returns:
            Response -- JSON serialized list of stitchers
        """
        stitchers = Stitcher.objects.all()
        serializer = StitcherSerializer(
            stitchers,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)