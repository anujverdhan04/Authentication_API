from django.http import JsonResponse
from rest_framework import generics, status
from django.contrib.auth.models import User
from django.views import View
from .serializers import UserSerializer, LoginSerializer
from .utils import generate_email_verification_token, verify_email_token
from django.contrib.auth import login
from django.urls import reverse

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Serialize the input data and validate
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate email verification token
        token = generate_email_verification_token(user)

        # Create the verification URL
        verification_url = reverse('verify-email') + f'?token={token}'

        # In a real-world scenario, you would send this URL in an email
        # Here we are just returning the URL for testing purposes
        return JsonResponse(
            {"message": "User created. Please verify your email.", "verification_url": verification_url},
            status=status.HTTP_201_CREATED
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # Serialize the input data and validate
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Log the user in
        login(request, user)

        return JsonResponse({"message": "Login successful!"}, status=status.HTTP_200_OK)


class VerifyEmailView(View):
    def get(self, request):
        # Local import to avoid circular import issues
        from .utils import verify_email_token

        # Get the token from query params
        token = request.GET.get('token')

        # If token is provided, verify it
        email = verify_email_token(token)

        if email:
            # If the token is valid and email is retrieved
            return JsonResponse({'message': 'Email verified successfully!'}, status=200)
        
        else:# If token is invalid or expired
            return JsonResponse({'message': 'Invalid or expired token.'}, status=400)
