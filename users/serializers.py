from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, data):
        user = User.objects.create_user(
            email        = data['email'],
            first_name = data['first_name'],
            last_name  = data['last_name'],
            password   = data['password']
        )
        user.save()
        return user