from django.urls import path
from .import views

urlpatterns = [
    path('add-friend/',views.SendFriendRequestView.as_view(),name="add_friend"),

    path('received-friend-request/',views.ReceivedFriendRequest.as_view(),name="received_friend_request"),

    path('accept-friend-request/',views.AcceptFriendRequestView.as_view(),name="accept_friend_request"),

    path('search-friends/',views.SearchUserView.as_view(),name="search_user_view")
]