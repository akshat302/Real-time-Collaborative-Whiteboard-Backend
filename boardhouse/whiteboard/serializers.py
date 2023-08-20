from rest_framework import serializers
from whiteboard.models import WhiteBoard, UserBoardInformation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}   

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

class WhiteBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhiteBoard
        fields = ['name', 'description', 'created_at']
    
    def create(self, validated_data):
        board = WhiteBoard.objects.create(**validated_data)
        return board 
    

class UserBoardInformationSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    board = WhiteBoardSerializer()

    class Meta:
        model = UserBoardInformation
        fields = ['user', 'board', 'action', 'undo', 'created_at', 'updated_at']

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=256)
    password = serializers.CharField(write_only=True, max_length=128)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
  