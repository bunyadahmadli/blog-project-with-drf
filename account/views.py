from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView,get_object_or_404,CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer,ChangePassworSerializer, RegisterSerializer
from django.contrib.auth import update_session_auth_hash
from .permissions import NotAuthenticated
from .throttles import RegisterThrottle

# Create your views here.

class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer 
    queryset =User.objects.all()

        
    def get_object(self):
        queryset =self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

    def perform_update(self,serializer):
        serializer.save(user =self.request.user)


class UpdatePasswordView(APIView):
    permission_classes=(IsAuthenticated,)

    def get_object(self):
        return self.request.user
    
    def put(self,request,*args,**kwargs):
        self.object= self.get_object()
      
        serializer = ChangePassworSerializer(data=request.data)

        if serializer.is_valid():
            old_password =serializer.data.get("old_password")
            if self.object.check_password(old_password):
                return Response({"old_password": "wrong_password"},status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            update_session_auth_hash(request,self.object)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#create user

class CreateUserView(CreateAPIView):
    throttle_classes = [RegisterThrottle,]
    model = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes =[NotAuthenticated]