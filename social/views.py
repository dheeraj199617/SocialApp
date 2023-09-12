from datetime import datetime,timedelta
from rest_framework import status 
from rest_framework.response import Response 
from rest_framework.generics import GenericAPIView ,CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Friend, Follow, Block,FriendshipRequest
from .serializers import SocialAppSerializer,ReceivedRequestSerializer
from authapp.models import User
from .exceptions import AlreadyExistsError,FromUserToUserSame
from datetime import timedelta,datetime
from django.db.models import Q 
from django.core.paginator import Paginator
from authapp.serializer import SignupSerializer
from django.db.models.functions import Now




class SendFriendRequestView(GenericAPIView):
    '''
    API FOR SENDING FRIEND REQUEST 
    Note : Instead of writing return Response multiple times, we can make it reusable by writing the code in a seperate function but here our main aim is to design model properly
    '''

    serializer_class = SocialAppSerializer

    authentication_classes = (TokenAuthentication,)

    permission_classes = (IsAuthenticated,)

    def post(self,request,*args,**kwargs):
        
        params = request.data

        serializer = self.serializer_class()

        #Note  :this can be achieved using throttling also

        friendship_object = FriendshipRequest.objects.filter(created__gt=Now()-timedelta(seconds=60)).count()

        if friendship_object > 3:
            return Response({
                'status' : False,
                "message"  : "You cannot send more then 3 friend request within one minute"
            })

        serializer.validate(params)

        user = User.objects.filter(id=params.get('user_id')).last()
        try:

            Friend.objects.add_friend(
                request.user,
                user,
                message="Hi,I would like to add you as a friend"
            )
        except AlreadyExistsError:
            return Response({
                'status' : False,
                "message"  :"Seems you have already sent friend request to {}, please wait for their response".format(user.first_name)
            })  
        except FromUserToUserSame as msg:
            return Response({
                "status" : False,
                "message" : msg.args[0]
            })
        return Response({
            'status' : True,
            "message"  :"Friend request has been sent successfully to {}".format(user.first_name)
        })


class ReceivedFriendRequest(GenericAPIView):
    '''
    '''
    authentication_classes = (TokenAuthentication,)

    permission_classes =(IsAuthenticated,)

    serializer_class = ReceivedRequestSerializer

    def get(self,request,*args,**kwargs):
        
        all_request = Friend.objects.unread_requests(user = request.user)
        
        serializer = self.serializer_class(all_request,many=True)
        
        return Response({
            'status': True,
            "message": "List of friend request received",
            "data" : serializer.data
        })


class AcceptFriendRequestView(GenericAPIView):
    '''
    API FOR ACCEPTING FRIEND REQUEST 
    '''
    authentication_classes = (TokenAuthentication,)
    
    permission_classes = (IsAuthenticated,)

    serializer_class = SocialAppSerializer

    def post(self,request,*args,**kwargs):
        
        params =  request.data

        serializer = self.serializer_class()

        serializer.validate(params) 
        
        user = User.objects.filter(id=params.get('user_id')).last()
                #if they are not a friend then only execute below logic 
        if not Friend.objects.are_friends(request.user,user):
            friend_request = FriendshipRequest.objects.get(from_user=request.user, to_user=user) 
            friend_request.accept()
            return Response({
                'status' : True,
                "message" : "You and {} are friend now".format(user.first_name)
            })
        else:
            return Response({
                'status' : False,
                "message"  :"Seems {} is already in your friend".format(user.first_name)
            })

class SearchUserView(GenericAPIView):
    ''' 
    API FOR SEARCHING USER BASED ON EMAIL OR NAME 
    NOTE : HERE WE WOULD HAVE USED INBUILT FILTER, BUT INSTEAD OF USING INBUILT I HAVE USED CUSTOM 

    ******* Note = In this API there is some code which we could have written more better way, like return Response ,this can be reusable,we generally follow such approach when we are coding for real time.
    '''
    
    
    authentication_classes = (TokenAuthentication,)

    serializer_class = SignupSerializer


    permission_classes = (IsAuthenticated,)


    def post(self,request,*args,**kwargs):
        params = request.data

        if 'email' in params.keys() and not len(str(params.get('email')).strip()) == 0:
            #client may sent data in any form and can add spaces also, so here we are removing spaces and converting it to lower
            user = User.objects.filter(email__iexact = str(params.get('email')).strip().lower()).exclude(email=request.user.email)
            if user.exists():
                data = user.values('first_name','email','last_name','id')
                return Response({
                    'status' : True,
                    "message"  :"User  fetched successfully",
                    "data": data 
                })
            else:
                return Response({
                    'status' : False,
                    "message"  :"No user found"
                })
       
        page_number = self.request.query_params.get('page_number')

        if not page_number:
            page_number= 1
        
        page_size = self.request.query_params.get('page_size')

        if not page_size:
            page_size = 10 
        
        if 'name' in params.keys() and not len(str(params.get('name')).strip()) == 0:
            #perform filter on first and last name both 
            filtered_user = User.objects.filter(Q(first_name__icontains = params.get('name')) |Q(last_name__icontains=params.get('name'))).exclude(id=request.user.id)
            paginator = Paginator(filtered_user , page_size)
            serializer = self.serializer_class(paginator.page(page_number),many=True)
            print("data is ",serializer.data)
            return Response({
                    'status': True,
                    "message"  : "User  fetched successfully",
                    "data" : serializer.data
            }) 
        
        #if nothing supplied from client ,just return all the user except current user 
        else:
            user_list = User.objects.all().exclude(id=request.user.id)
            paginator = Paginator(user_list , page_size)
            serializer = self.serializer_class(paginator.page(page_number),many=True)
            return Response({
                'status' : True,
                "message"  :"User fetched successfully",
                "data" : serializer.data

            })