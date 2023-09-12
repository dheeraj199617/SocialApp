from authapp.models import User 
from re import search
from rest_framework.serializers import ModelSerializer,ValidationError,Serializer
from django.contrib.auth import authenticate


class SignupSerializer(ModelSerializer):
    '''
    '''
    class Meta:
        model = User 
        fields = [
            'id','first_name','last_name','full_name','email'
        ]
    
    def validate(self,data):
        
        if not data.get("password") or str(data.get("password")).isspace():
            raise ValidationError({
                "status" : False,
                "message" : "Please enter your password"
            }) 
        
        if not data.get("email") or str(data.get("email")).isspace():
            raise ValidationError({
                "status" : False,
                "message" : "Please enter your password"
            }) 
        
        if not data.get("first_name") or str(data.get("first_name")).isspace():
            raise ValidationError({
                "status" : False,
                "message" : "first name cannot be blank"
            }) 
        
        if len(data.get('first_name')) > 50:
            raise ValidationError({
                'status' : False,
                "message" :"Maxium 50 characters are allowed in first name"
            })
        #digit not allowed in first name 
        if bool(search(r'\d',data.get('first_name'))):
            raise ValidationError({
                "status": False,
                "message" : "first name should not contains digit"
            })
        
        if data.get('last_name') and not  str(data.get('last_name')).isspace():
            #digit not allowed in last name 
            if bool(search(r'\d',data.get('last_name'))):
                raise ValidationError({
                "status": False,
                "message" : "last name should not contains digit"
            })
            
            if len(data.get('last_name')) > 50:
                raise ValidationError({
                'status' : False,
                "message" :"Maxium 50 characters are allowed in last name"
            })
        
        if User.objects.filter(email__iexact = data.get('email')).exists():
            raise ValidationError({
                'status' : False,
                "message" :"An account with this email already exist"
            })
        
        return data 

    def create(self,data):
        user =  User.objects.create(**data) 
        user.set_password(data.get("password"))
        user.save()
        return data 



class LoginSerializer(Serializer):
    '''
    serializer for login 
    '''

    def validate(self,data):
        
        if not data.get('email') or str(data.get("email")).isspace():
            raise ValidationError({
                'status' : False,
                "message" :"Please enter your email"
            }) 
        
        if not data.get('password') or str(data.get("password")).isspace():
            raise ValidationError({
                'status' : False,
                "message" :"Please enter your password"
            }) 
        
        #email may be provided in any form from client , also removing any extra space if there is any
        if not authenticate(email = str(data.get('email')).lower().strip(),password = data.get('password')):
           
            raise ValidationError({
                'status' : False,
                "message": "Invalid Credentials"
            }) 
    
        user = User.objects.get(email__iexact =str(data.get('email')).lower().strip())

        return user 