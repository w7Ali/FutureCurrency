from django.urls import path
from .views import user_signup, user_login, user_logout, user_reset_password, user_edit_profile, user_details

urlpatterns = [
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('reset/', user_reset_password, name='reset'),
    path('edit/', user_edit_profile, name='edit-profile'),
    path('detail/<int:id>', user_details, name='user-detail'),
]
