from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer

# Create your views here.

class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            return Response(
                {'profile': user_profile.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving profile'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


