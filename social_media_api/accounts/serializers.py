from rest_framework import serializers
from rest_framework.authtoken.models import Token  # Import for Token creation
from django.contrib.auth import get_user_model  # Import for user creation

User = get_user_model()  # Get the User model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password field for registration

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            **validated_data  # Pass additional validated data to user creation (optional)
        )
        # Optionally create a token on user creation (adjust as needed)
        token = Token.objects.create(user=user)
        return user, token  # Return both user and token for further processing

    class Meta:
        model = User
        fields = ('id', 'username', 'password')  # Adjust fields as needed

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Username and password are required.')

        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError('Invalid username or password.')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        # Token creation can be done here or in UserSerializer.create()
        # user = validated_data['user']
        # token = Token.objects.create(user=user)
        # return user, token  # If returning both user and token
        pass  # No object creation for login serializer
