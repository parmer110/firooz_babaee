from django.urls import path
from .views import userAPIView,login,LoginView,CustomUserListView,UserRetrieveUpdateDestroyView,UserListPublishedView
from . import views





urlpatterns = [
     path('signup/', views.SignUpView.as_view(),name='signup'),
     # path('login/', login_page, name='login'),
     path('APIUserLogin/', login, name='APIlogin'),
     path('loginAPP/', views.LoginView.as_view(), name='loginapi'),#this is for login 
     
     #path('users/', UserListCreateView.as_view(), name='user-list-create'),
     path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
     path('users/published/', UserListPublishedView.as_view(), name='user-list-published'),

]

urlpatterns += [
path('userslist/', CustomUserListView.as_view(), name='userslist'),
]