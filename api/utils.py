from rest_framework.response import Response
from rest_framework import status


def generate_error_response(message: str, status=status.HTTP_400_BAD_REQUEST):
    return Response({"details": message}, status=status)
