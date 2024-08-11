from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.models import User
from account.serializers import UserRegistrationSerializer


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
