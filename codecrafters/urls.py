
from django.contrib import admin
from django.urls import path
from project.views import login, api_create_user, user_info,logout, Profile_info, Profile_Create, Courses_info, Course_info, refresh_token,get_purchased_courses, purchase_course,get_course_video, Teachers_info,update_progress
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login, name='api-login'),
    path('api/refresh_token/', refresh_token, name='refresh-token'),
    path('api/create_user/', api_create_user, name='api-create-user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user-info/', user_info, name='user-info'),
    path('api/logout/', logout, name='logout'),
    path('api/Profile_info/', Profile_info, name='Profile-info'),
    path('api/Profile_Create/', Profile_Create, name='Profile-Create'),
    path('api/Courses_info/', Courses_info, name='Courses-info'),
    path('api/Course_info/<int:courseId>/', Course_info, name='course-details'),
    path('api/Course_video/<int:courseId>/', get_course_video, name='course-video'),
    path('api/Teacher_info/', Teachers_info, name='Teacher-info'),
    path('api/purchase_course/<int:courseId>/', purchase_course, name='purchase-course'),
    path('api/updateProgress/', update_progress, name='purchase-course'),


    






]
