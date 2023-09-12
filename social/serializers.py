from rest_framework.serializers import Serializer,ModelSerializer
from .models import Friend
from rest_framework.serializers import ValidationError
from authapp.models import User 
from .models import Friend
from authapp.serializer import SignupSerializer


class SocialAppSerializer(Serializer):
    '''
    '''
    def validate(self,data):
        
        
        if not data.get('user_id') or str(data.get('user_id')).isspace():
            raise ValidationError({
                'status' : False,
                "message" : "Please select whom you want to add as a friend"
            })
        #instead of digit (user id is digit), if something else is passed
        if not str(data.get('user_id')).isdigit():
            raise ValidationError({
                'status' : False,
                "message": "Please provide valid input"
            })
        if not User.objects.filter(id = data.get('user_id')).exists():
            raise ValidationError({
                'status' : False,
                "message" : "This user has been either removed or does  not exist"
            })
        

        
        return data 
    
class ReceivedRequestSerializer(ModelSerializer):
    '''
    '''
    from_user = SignupSerializer()  
    class Meta:
        model =Friend
        fields =[
            'id','from_user'
        ]