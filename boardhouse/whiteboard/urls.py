from django.urls import path
from whiteboard.views import RegisterUserView, LoginAPIView, WhiteBoardCreationView, ListAllBoardsView, ListBoardView, ListAllActions, LogoutView

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("create_whiteboard/", WhiteBoardCreationView.as_view(), name="create_whiteboard"),
    path("list_all_boards/", ListAllBoardsView.as_view(), name="list_all_boards"), 
    path("list_board/", ListBoardView.as_view(), name="list_board"),
    path("list_all_actions/", ListAllActions.as_view(), name="list_all_actions"),
    path("logout/", LogoutView.as_view(), name="logout")
]