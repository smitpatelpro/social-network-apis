from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status as resp_status
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle

from django.db.utils import IntegrityError
from api.user import models
from api.user.models import FriendRequest, User
from api.user.serializers import (
    FriendRequestSerializer,
    UserSerializer,
)
from api.utils import generate_error_response


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserSearchView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request, search_key):
        user = User.objects.filter(email__iexact=search_key)
        if user:
            users = user
        else:
            users = User.objects.filter(name__icontains=search_key.strip())

        users = self.paginate_queryset(users, request, view=self)

        serializer = UserSerializer(users, many=True)
        return self.get_paginated_response(serializer.data)


class FriendRequestSentView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status = request.query_params.get("status")
        friend_requests = request.user.friend_requests_sent.all()
        if status:
            friend_requests = friend_requests.filter(status=status)

        friend_requests = FriendRequestSerializer.eager_load(friend_requests)

        friend_requests = self.paginate_queryset(
            friend_requests, request, view=self
        )

        serializer = FriendRequestSerializer(friend_requests, many=True)
        return self.get_paginated_response(serializer.data)


class FriendRequestSendView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, id):
        # Dont allow duplicate when requests is already pending or accepted
        existing_requests = FriendRequest.objects.filter(
            requested_by=request.user, requested_to_id=id
        ).exclude(status=FriendRequest.Status.REJECTED)
        if existing_requests.exists():
            return generate_error_response("Request already exists")

        try:
            friend_request = FriendRequest.objects.create(
                requested_by=request.user, requested_to_id=id
            )
        except IntegrityError:
            return generate_error_response("Invalid user")

        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=resp_status.HTTP_201_CREATED)


class FriendRequestReceiveView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status = request.query_params.get("status")
        friend_requests = request.user.friend_requests_received.all()
        if status:
            friend_requests = friend_requests.filter(status=status)

        friend_requests = FriendRequestSerializer.eager_load(friend_requests)

        friend_requests = self.paginate_queryset(
            friend_requests, request, view=self
        )

        serializer = FriendRequestSerializer(friend_requests, many=True)
        return self.get_paginated_response(serializer.data)


class FriendRequestActionView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        status = request.data.get("status")
        valid_statuses = [
            FriendRequest.Status.ACCEPTED.value,
            FriendRequest.Status.REJECTED.value,
        ]
        if status not in valid_statuses:
            return generate_error_response(
                f"Provide valid status from {valid_statuses}"
            )

        friend_request = FriendRequest.objects.filter(
            id=id,
            requested_to=request.user,
            status=FriendRequest.Status.REQUESTED,
        ).first()

        if not friend_request:
            return generate_error_response("Invalid request id")

        if status == FriendRequest.Status.ACCEPTED:
            request.user.friends.add(friend_request.requested_by)
            friend_request.status = FriendRequest.Status.ACCEPTED
        elif status == FriendRequest.Status.REJECTED:
            friend_request.status = FriendRequest.Status.REJECTED

        friend_request.save(update_fields=["status"])
        return Response(
            {"detail": f"Friend request successfully {status.lower()}"}
        )


class FriendsListView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = request.user.friends.all()

        friends = self.paginate_queryset(friends, request, view=self)

        serializer = UserSerializer(friends, many=True)
        return self.get_paginated_response(serializer.data)


class EnumsView(APIView):
    def get(self, request):
        enums = {
            "FRIEND_REQUEST_STATUS": {
                k: v for k, v in models.FriendRequest.Status.choices
            }
        }
        return Response(enums)
