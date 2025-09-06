from __future__ import annotations

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import LoginSerializer, UserInfoSerializer
from ..common.responses import success_response


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):  # type: ignore[override]
        response = super().post(request, *args, **kwargs)
        data = response.data
        # Ensure user info inside top-level data.user
        return Response(success_response(data=data, message='Login success'))


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):  # type: ignore[override]
        response = super().post(request, *args, **kwargs)
        return Response(success_response(data=response.data, message='Token refreshed'))


class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):  # type: ignore[override]
        return self.request.user

    def get(self, request, *args, **kwargs):  # type: ignore[override]
        serializer = self.get_serializer(self.get_object())
        return Response(success_response(data=serializer.data, message='User info'))
