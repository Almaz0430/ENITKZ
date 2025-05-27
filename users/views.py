from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import login, logout, get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from .models import PasswordResetToken
from .serializers import (
    UserSerializer, UserCreateSerializer, UniversityCreateSerializer, LoginSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    PasswordChangeSerializer
)

User = get_user_model()

@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с пользователями."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """Определяет права доступа в зависимости от действия."""
        if self.action in ['create', 'register_university', 'login', 'reset_password_request', 'reset_password_confirm']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'change_password', 'me', 'logout']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Возвращает соответствующий сериализатор в зависимости от действия."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'register_university':
            return UniversityCreateSerializer
        elif self.action == 'login':
            return LoginSerializer
        elif self.action == 'reset_password_request':
            return PasswordResetRequestSerializer
        elif self.action == 'reset_password_confirm':
            return PasswordResetConfirmSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        return self.serializer_class
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Получение информации о текущем пользователе."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def register_university(self, request):
        """Регистрация нового ВУЗа."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': UserSerializer(user).data,
                'message': 'ВУЗ успешно зарегистрирован'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(csrf_exempt)
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Выход пользователя."""
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Пользователь не аутентифицирован."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        logout(request)
        response = Response({"detail": "Успешный выход из системы."})
        response.delete_cookie('sessionid')  # Удаляем cookie сессии
        return response
    
    @action(detail=False, methods=['post'])
    def reset_password_request(self, request):
        """Запрос на сброс пароля."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Генерация токена
        token = get_random_string(64)
        PasswordResetToken.objects.create(user=user, token=token)
        
        # Отправка письма
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}/"
        send_mail(
            'Сброс пароля',
            f'Для сброса пароля перейдите по ссылке: {reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return Response({"detail": "Инструкции по сбросу пароля отправлены на указанный email."})
    
    @action(detail=False, methods=['post'])
    def reset_password_confirm(self, request):
        """Подтверждение сброса пароля."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token_obj = serializer.validated_data['token_obj']
        user = token_obj.user
        user.set_password(serializer.validated_data['password'])
        user.save()
        
        # Отметка токена как использованного
        token_obj.is_used = True
        token_obj.save()
        
        return Response({"detail": "Пароль успешно изменен."})
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Изменение пароля пользователем."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({"detail": "Пароль успешно изменен."})
    
    def create(self, request, *args, **kwargs):
        """Создание нового пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Автоматическая аутентификация после регистрации
        login(request, user)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """Аутентификация пользователя."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            response = Response({
                'user': UserSerializer(user).data,
                'message': 'Успешный вход в систему'
            })
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
