from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, UserTokenSerializer

class UserSignUpAPIView(CreateAPIView):
    serializer_class = UserSerializer

class UserSignInAPIView(APIView):
    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        user = serializer.validated_data['user']

        token, is_created = Token.objects.get_or_create(
            user=user
        )

        return Response({'token': token.key})