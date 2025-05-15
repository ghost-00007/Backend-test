from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from rest_framework import status

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from .authentication import AuthBackend
from .serializers import UserSerializer


class UserLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = AuthBackend().authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': True,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user.email,
                'role': user.role,
                'department': user.department,
                'designation': user.designation,
                'team': user.team,
            })
        else:   
            return Response({"message": "Invalid credentials"}, status=401)


User = get_user_model()

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        new_password = request.data.get("new_password")

        if not new_password:
            return Response({"error": "New password is required."}, status=400)

        user = request.user
        user.set_password(new_password)
        user.save()

        return Response({"message": f"Password reset successful for {user.email}."}, status=200)

class UserCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(user)
            return Response({
                "status":True,
                "message": "User details fetched!",
                "data": serializer.data,
            },status=status.HTTP_200_OK,
            )
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response({
                "status":True,
                "message": "User details fetched!",
                "data": serializer.data,
            },status=status.HTTP_200_OK,
            )

    def post(self, request):
        data = {
            'email' : request.data.get('email'),
            'role' : request.data.get('role_id'),
            'employee_name' : request.data.get('employee_name'),
            'employee_code' : request.data.get('employee_code'),
            'department' : request.data.get('department_id'),
            'designation' : request.data.get('designation_id'),
            'reporting_manager' : request.data.get('reporting_manager_id'),
            'team' : request.data.get('team_id'),
        }


        userSerializer = UserSerializer(data=data)
        if userSerializer.is_valid():
            userSerializer.save()
            currentUser = User.objects.get(email=request.data.get('email'))
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(currentUser)
            uid = urlsafe_base64_encode(force_bytes(currentUser.pk))

            set_link = f"{settings.FRONTEND_URL}/setPassword/{uid}/{token}/"

            subject = "Set Password Request"

            html_message = render_to_string(
                "Email_HTML/set_password.html",
                {
                    "user": currentUser,
                    "reset_link": set_link,
                    "role": currentUser.role
                },
            )
            plain_message = strip_tags(html_message)
            try:
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.data.get('email')],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to send email. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            return Response(
                {
                    'status': True,
                    'message': 'Employee added successfully!',
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'status': False,
                    'message': 'Something went wrong!',
                    'error': userSerializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        data = {
            'email': request.data.get('email'),
            'role': request.data.get('role_id'),
            'employee_name': request.data.get('employee_name'),
            'employee_code': request.data.get('employee_code'),
            'department': request.data.get('department_id'),
            'designation': request.data.get('designation_id'),
            'reporting_manager': request.data.get('reporting_manager_id'),
            'team': request.data.get('team_id'),
        }

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': True, 'message': 'Employee updated successfully!'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'status': False, 'message': 'Update failed!', 'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(
            {'status': True, 'message': 'Employee deleted successfully!'},
            status=status.HTTP_204_NO_CONTENT
        )

class UserEmailConfirmation(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        requestedUser = User.objects.get(email=email)

        if requestedUser is not None:
            currentUser = User.objects.get(email=request.data.get('email'))
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(currentUser)
            uid = urlsafe_base64_encode(force_bytes(currentUser.pk))

            set_link = f"{settings.FRONTEND_URL}/resetPassword/{uid}/{token}/"

            subject = "Reset Password Request"

            html_message = render_to_string(
                "Email_HTML/reset_password.html",
                {
                    "user": currentUser,
                    "reset_link": set_link,
                    "role": currentUser.role
                },
            )
            plain_message = strip_tags(html_message)
            try:
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.data.get('email')],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to send email. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            return Response(
                {
                    'status': True,
                    'message': 'Reset Link send successfully!',
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'status': False,
                    'message': 'No User Details Found!',
                },
                status=status.HTTP_400_BAD_REQUEST
            )