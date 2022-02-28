import re

from rest_framework.authtoken.models import Token
from rest_framework.response         import Response
from rest_framework.decorators       import APIView
from rest_framework                  import status

from .models      import User
from .serializers import UserSerializer

class UserSignUpAPIView(APIView):
    def post(self, request):
        REGEX_PASSWORD = r'^(?=.*\w)(?=.*\d)[\w\d@$!%*?&]{8,}$'
        
        if not re.fullmatch(REGEX_PASSWORD, request.data['password']):
            return Response('비밀번호 조건에 성립하지 않습니다.', status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token      = Token.objects.create(user=serializer.instance)
            token_data = {'token': token.key}
            return Response(token_data['token'], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)