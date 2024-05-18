from authentication.models import User
from authentication.permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.serializers import (
    UserRegisterSerializer, 
    LoginSerializer, 
    UserSerializer, 
    UserProfileSerializer, 
    LogoutSerializer, 
)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Register a new user.

        Creates a new user with the provided information. This endpoint expects a payload containing user details.
        """
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Login a user.

        Login a user with the provided information. This endpoint expects a payload containing user details.
        """
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({"error": "User not found!"}, status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            raise AuthenticationFailed({"error": "Incorrect password!"})

        refresh = RefreshToken.for_user(user)

        return Response(
            {   
                "user": user.id,    
                "username": user.username,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logout a user.

        Logout a user with the provided information. This endpoint expects a payload containing user details.
        """
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh_token"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "You have successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Unable to log out {e}."}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return User.objects.get(id=user_id)
    
    def get(self, request, *args, **kwargs):
        """
        Profile of user.

        Profile of user with the provided information. This endpoint expects a payload containing user details.
        """
        return super().get(request, *args, **kwargs)


class ProfileUpdateView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request):
        """
        Users profile update.

        Users profile update with the provided information. This endpoint expects a payload containing user details.
        """
        user = request.user

        serializer = UserProfileSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully!'}, status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)