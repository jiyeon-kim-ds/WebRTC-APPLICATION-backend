from rest_framework.generics         import CreateAPIView

from .serializers import UserSerializer

class UserSignUpAPIView(CreateAPIView):
    serializer_class = UserSerializer