from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, UserSignInSerializer

class UserSignUpAPIView(CreateAPIView):
    serializer_class = UserSerializer


class UserSignInAPIView(APIView):
    def post(self, request):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        user = serializer.validated_data['user']

        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})