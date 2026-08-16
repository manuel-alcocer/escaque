from rest_framework import generics, permissions

from .serializers import UserSerializer


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """Read or update the signed-in account."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
