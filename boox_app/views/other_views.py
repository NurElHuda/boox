import subprocess
from datetime import timedelta

import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response




class PullAndUpdate(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        subprocess.run(["bash", "update.sh"])

        username = settings.PA_USERNAME
        domain_name = settings.PA_DOMAIN_NAME
        token = settings.PA_TOKEN

        if username and domain_name and token:
            response = requests.post(
                f"https://www.pythonanywhere.com/api/v0/user/{settings.PA_USERNAME}/webapps/{settings.PA_DOMAIN_NAME}/reload/",
                headers={"Authorization": "Token {settings.PA_TOKEN}"},
            )
            if response.status_code == 200:
                message = response.json()
            else:
                message = f"Got unexpected status code {response.status_code}: {response.content}"
        return Response(message)
