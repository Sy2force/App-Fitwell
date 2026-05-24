from rest_framework_simplejwt.views import TokenObtainPairView
from api.serializers import EmailTokenObtainPairSerializer

class EmailTokenObtainPairView(TokenObtainPairView):
    """
    Login view that uses email instead of username.
    """
    serializer_class = EmailTokenObtainPairSerializer
