from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from .models import Profile, CourseEnrollment, PythonCourse, Purchase, Teacher
from rest_framework.permissions import IsAuthenticated
from .serializers import PythonCourseSerializer, TeacherSerializer
from datetime import datetime
from django.core.files.base import ContentFile
import boto3
from django.utils import timezone
from django.http import Http404

from django.db import IntegrityError

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Perform authentication logic here
    user = authenticate(username=username, password=password)
    if user is not None:
        # Authentication successful

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Set token expiration time
        access_token_lifetime = timedelta(minutes=5)
        refresh_lifetime = timedelta(days=1)
        refresh.set_exp(lifetime=refresh_lifetime)
        access_token_exp = timezone.now() + access_token_lifetime
        refresh_token_exp = timezone.now() + refresh_lifetime

        # Return the tokens and expiration time in the response
        response_data = {
            'access_token': access_token,
            'access_token_exp': access_token_exp,
            'refresh_token': str(refresh),
            'refresh_token_exp': refresh_token_exp,
        }
        # print(refresh)
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        # Invalid credentials
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])

def refresh_token(request):
    refresh_token = request.data.get('refresh_token')
    print(request.data)
    if refresh_token == 'undefined':
        return Response({'error': 'Refresh token is undefined'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        refresh = RefreshToken(refresh_token)

        # Check if the refresh token is expired or invalid
        if not refresh.token:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        # Set token expiration time
        access_token_lifetime = timedelta(minutes=5)
        refresh_lifetime = timedelta(days=1)
        refresh.set_exp(lifetime=refresh_lifetime)
        access_token_exp = timezone.now() + access_token_lifetime
        refresh_token_exp = timezone.now() + refresh_lifetime

        access_token = str(refresh.access_token)

        # Return the new access token and its expiration time in the response
        response_data = {
            'access_token': access_token,
            'access_token_exp': access_token_exp,
            'refresh_token_exp': refresh_token_exp,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        # Invalid refresh token
        return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    # Extract the required information from the user object
    user_info = {
        'username': user.username,
        'email': user.email,
        'name' : user.first_name
        # Add any additional fields you need
    }
    return Response(user_info)

@api_view(['GET'])
def Courses_info(request):
    courses = PythonCourse.objects.all()  # Query all PythonCourse instances from the database
    serializer = PythonCourseSerializer(courses, many=True)  # Serialize the queryset

    return Response(serializer.data)

@api_view(['GET'])
def Course_info(request, courseId):
    try:
        course = get_object_or_404(PythonCourse, id=courseId)
        course_data = {}

        # Iterate over the model fields and add them to course_data
        for field in PythonCourse._meta.get_fields():
            if field.concrete and not field.is_relation:
                course_data[field.name] = getattr(course, field.name)
        course_data['instructor'] = (f'{course.instructor.name} {course.instructor.lastname}')
            
           
        print(course_data)
        return Response(course_data)
    except PythonCourse.DoesNotExist:
        return Response({'error': 'Course not found.'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Profile_info(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profile = request.user.profile  # Assuming you have a one-to-one relationship between User and Profile
    purchased_courses = profile.purchases.all()
    enrollments = CourseEnrollment.objects.filter(profile=profile).values('course__id', 'course__title')
    progresss = CourseEnrollment.objects.filter(profile=profile).values('progress')

    profile_info = {
        'username': user.username,
        'name': user.first_name,
        'lastname': user.last_name,
        'email': user.email,
        'phone_number': profile.phone_number,
        'date_of_birth': profile.date_of_birth,
        "profileImage" : profile.profile_image.url,
        "PurchasedCourses" : [course.title for course in purchased_courses],
        "enrollment_progress": [
            {"course_id": enrollment['course__id'], "enrollment": enrollment['course__title'], "progress": progress['progress']}
            for enrollment, progress in zip(enrollments, progresss)
        ],
        # Add any additional fields you need
    }

    print(profile_info)
    return Response(profile_info)


from django.core.files.base import ContentFile

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Profile_Create(request):
    user = request.user

    # Get the data from the request body
    name = request.data.get('name')
    lastname = request.data.get('lastName')
    phone_number = request.data.get('phone_number')
    date_of_birth = request.data.get('date_of_birth')
    profile_image = request.FILES.get('profileImage')

    if name:
        user.first_name = name
    if lastname:
        user.last_name = lastname

    # Save the user changes
    user.save()

    # Check if the user has a profile, create one if not
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    # Update the profile fields if provided
    if phone_number:
        profile.phone_number = phone_number
    if date_of_birth:
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        profile.date_of_birth = date_of_birth

    # Save the profile changes
    profile.save()

    # Process the profile image if provided
    if profile_image:
        # Read the file content
        image_content = profile_image.read()
        # Generate a unique filename
        filename = f"profile_image_{user.id}_{profile.id}_{profile_image.name}"
        # Create a ContentFile object with the file content
        content_file = ContentFile(image_content, name=filename)
        # Assign the content file to the profile_image field
        profile.profile_image.save(filename, content_file)

    return Response("Profile information updated successfully.")




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Get the user's refresh token
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        refresh_token = RefreshToken(token)

        # Blacklist the refresh token to invalidate it
        refresh_token.blacklist()

        return Response({'detail': 'Logout successful'})
    except Exception as e:
        return Response({'detail': 'Logout failed'}, status=400)
    
@api_view(['POST']) 
def api_create_user(request):
    try:
        userName = request.data.get('username')
        passWord = request.data.get('password')
        emaiL = request.data.get('email')

        user = User.objects.create_user(username=userName,
                                    email=emaiL,
                                    password=passWord)
        return Response({'detail': 'Create successful'})
    except Exception as e:
        return Response({'detail': 'Logout failed'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def purchase_course(request, courseId):
    course = PythonCourse.objects.get(id=courseId)
    profile = request.user.profile  # Assuming you have a one-to-one relationship between User and Profile
    CourseEnrollment.objects.create(profile=profile , course=course)
    # Create a Purchase instnce
    purchase = Purchase.objects.create(profile=profile, course=course)
    
    # Add the purchased course to the user's profile
    profile.purchases.add(course)
    
    # Return success response or redirect to a confirmation page
    return Response("Course purchased successfully!")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_purchased_courses(request):
    profile = request.user.profile  # Assuming you have a one-to-one relationship between User and Profile
    purchased_courses = profile.purchases.all()
    
    # Return the purchased courses as JSON or render a template with the course data
    return Response({'courses': [course.title for course in purchased_courses]})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course_video(request, courseId):
    usr = request.user

    try:
        profile = Profile.objects.get(user=usr)
        course = PythonCourse.objects.get(id=courseId)
        purchased_courses = Purchase.objects.filter(profile=profile, course=course)
        progress = CourseEnrollment.objects.filter(profile=profile, course=course)

        if purchased_courses.exists():
            videos = course.videos.all()
            video_data = [
                {
                    'id': video.id,
                    'title':video.title,
                    'url': video.file.url
                }
                for video in videos
            ]

            response_data = {
                'videos': video_data,
                'progress': progress[0].progress if progress else 0  # Retrieve the progress value if it exists, otherwise set it to 0
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response("You have not purchased this course.", status=status.HTTP_403_FORBIDDEN)
    except Profile.DoesNotExist:
        return Response("User profile does not exist.", status=status.HTTP_404_NOT_FOUND)
    except PythonCourse.DoesNotExist:
        return Response("Course does not exist.", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def Teachers_info(request):
    teachers = Teacher.objects.all()

    data = []
    for teacher in teachers:
        teacher_data = {
            'name': teacher.name,
            'lastname': teacher.lastname,
            'Imgurl': teacher.profileImage.url,
            'description': teacher.description
            # Add other fields as needed
        }
        data.append(teacher_data)
    
    return Response(data)





@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_progress(request):
    course_id = request.data.get('courseId')  # Updated key to 'courseId'
    progress = request.data.get('progress')
    print(request.data)
    try:
        try:
            course = PythonCourse.objects.get(id=course_id)
        except PythonCourse.DoesNotExist:
            raise Http404("Course not found.")
        
        usr = request.user.profile

        course_info = CourseEnrollment.objects.filter(course=course, profile=usr)
        
        for enrollment in course_info:
            enrollment.progress += int(progress)  # Convert progress to an integer

            if enrollment.progress >= 10:
                enrollment.completed = True
                enrollment.progress =10
            else:
                enrollment.completed = False
            
            try:
                enrollment.save()
            except IntegrityError:
                # Handle IntegrityError if saving the model fails
                return Response({'error': 'Failed to update progress.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Progress updated successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
