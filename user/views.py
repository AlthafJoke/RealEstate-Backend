from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializer import UserSerializer


# Create your views here.
User = get_user_model()

class RegisterView(APIView):
    permission_classes  = (permissions.AllowAny)
    
    def post(self, request):
        try:
            data = request.data
            name = data['name']
            email = data['email']
            email = email.lower()
            password = data['password']
            re_password = data['re_password']
            is_employer = data['is_employer']
            
            if is_employer == 'True':
                is_employer = True
            else:
                is_employer = False
                
            if password == re_password:
                if len(password) >=8:
                    if not User.object.filter(email=email).exists():
                        if not is_employer:
                            User.objects.create(name=name, email=email, password=password)
                            return Response(
                                {'success': 'User created successfully'},
                                status=status.HTTP_201_CREATED
                            )
                        else:
                            User.objects.create_employer(name=name, email=email, password=password)
                            return Response(
                                {'success': 'Employer account created successfully'},
                                status=status.HTTP_201_CREATED
                            )
                            
                    else:
                        return Response(
                    {'error': 'User with this email already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                    
                else:
                    return Response(
                    {'error': 'Password must be atleast 8 characters in length'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                    
            
            else:
                return Response(
                    {'error': 'Passwords does not match'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'something went wrong when registering an account'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                
            )
            
class RetreiveUserView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)
            
            return Response(
                {'user':user.data},
                status=status.HTTP_200_OK
            )
            
        except:
            return Response(
                {'error': 'something went wrong when retreiving user details'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                
            )
        
        
     
    

