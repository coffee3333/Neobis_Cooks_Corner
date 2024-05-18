from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from cooks_corner.models import Follow
from cooks_corner.serializers import FollowListSerializer, FollowSerializer
from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authentication.permissions import IsOwnerOrReadOnly


class FollowListView(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowListSerializer
    permission_classes = [IsAuthenticated]


class FollowCreateView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(follower=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError({"error": "You have already followed this author."})


class FollowDestroyView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        follower = self.request.user
        followed_id = kwargs.get('followed_id')

        try:
            liked_recipe = get_object_or_404(Follow, follower=follower, followed_id=followed_id)
            liked_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response({"error": "Follow author not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)