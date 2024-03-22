from django.urls import path
from api.user import views


urlpatterns = [
    # Signup
    path("users/", views.UserCreateView.as_view(), name="user_create"),
    # Search
    path(
        "users/search/<str:search_key>",
        views.UserSearchView.as_view(),
        name="user_search",
    ),
    # Friend Requests : Send
    path(
        "users/<uuid:id>/send_friend_request/",
        views.FriendRequestSendView.as_view(),
        name="send_request",
    ),
    path(
        "me/friend_requests/sent/",
        views.FriendRequestSentView.as_view(),
        name="friend_requests_sent",
    ),
    # Friend Requests : Receive
    path(
        "me/friend_requests/received/",
        views.FriendRequestReceiveView.as_view(),
        name="friend_requests_received",
    ),
    path(
        "me/friend_requests/received/<uuid:id>",
        views.FriendRequestActionView.as_view(),
        name="friend_requests_received_action",
    ),
    path(
        "me/friends/",
        views.FriendsListView.as_view(),
        name="friend_requests_received_action",
    ),
    # Enums
    path("enums/", views.EnumsView.as_view(), name="enums"),
]
