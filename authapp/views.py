from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializer import SignupSerializer,LoginSerializer
from datetime import datetime
from rest_framework.authtoken.models import Token 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User 
 

class SignUpView(GenericAPIView):
    '''
    API FOR SIGNUP 
    '''
    serializer_class = SignupSerializer 

    def post(self,request,*args,**kwargs):
        
        params = request.data 

        serializer = self.serializer_class()

        validated_data = serializer.validate(params)

        validated_data.update(created_at =datetime.now())   #we can maintain datetime according to timezone of registered user also,if required

        serializer.create(validated_data)

        return Response({
            'status' : True,
            "message"  : "Registration successful"
        })


class LoginView(GenericAPIView):
    '''
    API FOR LOGIN 
    '''
    serializer_class =  LoginSerializer


    def post(self,request,*args,**kwargs):
        
        params = request.data

        serializer = self.serializer_class()

        user = serializer.validate(params)

        token,created_at = Token.objects.get_or_create(user=user)

        return Response({
            'status' :  True,
            "message"  : "Login successful",
            "data"  : {
                "token" : token.key, #jwt would have been also implemented, but ok for now 
                "user_id" : user.id  #ok one extra hit of db here, can be minimized with caching technique 
            }
        })



class FetchMyProfile(GenericAPIView):
    '''
    API FOR FETCHING MY PROFILE 
    '''
    permission_classes = (IsAuthenticated,)

    authentication_classes = (TokenAuthentication,)

    def post(self,request,*args,**kwargs):

        #for now our requirement is to send limited fields (means there are just 4-5  fiels so we are querying like this,if the number of the fields to be sent is more, obviously this approach will not make sense)
    
        user_data = User.objects.filter(id=request.user.id).values('id','first_name','last_name','full_name','email').last()    
        
        return Response({
            'status' : True,
            "message" : "details fetched successfully",
            "data"  : user_data
        })


class LogOutView(GenericAPIView):
    '''
    '''
    permission_classes = (IsAuthenticated,)

    authentication_classes = (TokenAuthentication,)

    def post(self,request,*args,**kwargs):
        request.user.auth_token.delete() #deleting the token 
        return Response({
            'status' : True,
            "message"  :"Logout successful"
        })
