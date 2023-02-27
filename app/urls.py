from django.urls import path
from app.views import HomeView, LoginRequestView, LogoutRequestView, UserDelete, UserCreate, UserDetail, UserEdit, UserList            

app_name = 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("login/", LoginRequestView.as_view(),name="login_page"),
    path("logout/", LogoutRequestView.as_view(),name="logout_page"),
    path("userlist/", UserList.as_view(),name="user_list"),
    path("createuser/", UserCreate.as_view(),name="create_user"),
    path("userdetail/<int:pk>/", UserDetail.as_view(),name="user_detail"),
    path("updateuser/<int:pk>/", UserEdit.as_view(),name="update_user"),
    path("deleteuser/<int:pk>/", UserDelete.as_view(),name="delete_user"),

]