import random
import string

from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User


class RegisterVoterView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request: Request, *args, **kwargs):
        username = request.data.get('username')
        random_name = ''.join(random.sample(string.ascii_letters, 16))
        random_pass = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        user = User.objects.create_user(
            username=random_name,
            chosen_name=username,
            password=random_pass,
        )
        token = Token.objects.create(user=user)
        return Response({'token': token.key})
