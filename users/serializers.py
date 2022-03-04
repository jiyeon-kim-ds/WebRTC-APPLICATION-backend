import re

from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def validate(self, data):
        REGEX_PASSWORD = r'^(?=.*\w)(?=.*\d)[\w\d@$!%*?&]{8,}$'
            
        if not re.fullmatch(REGEX_PASSWORD, data['password']):
            raise serializers.ValidationError({'비밀번호 조건에 성립하지 않습니다.'})
        return data
            
    def create(self, validated_data):
        user = User.objects.create_user(
            email      = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name  = validated_data['last_name'],
            password   = validated_data['password']
        )
        user.save()
        return user


class UserSignInSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email    = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('사용자 확인이 불가능합니다.')

        if not user.check_password(password):
                raise serializers.ValidationError('사용자 확인이 불가능합니다.')
        
        data['user'] = user
        return data