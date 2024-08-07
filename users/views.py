from rest_framework import viewsets,status
from .serializers import ProfileSerializer,ProfileUpdateSerializer,UserLoginSerializer
from config.tokens import get_tokens_for_user
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import UserProfile,CustomUser
from rest_framework.decorators import action


class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_classes = {
        "list":ProfileSerializer,
        "create":ProfileSerializer,
        "retrieve":ProfileSerializer,
        "update":ProfileUpdateSerializer,
        "partial_update":ProfileUpdateSerializer,
        "destroy":ProfileUpdateSerializer,
        "user_login":UserLoginSerializer
    }

    def get_permissions(self):
        print("action",self.action)
        if self.action in ['list','retrieve','update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes=[AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        return self.serializer_classes[self.action]
    
    def get_object(self):
        if self.kwargs["pk"] == "me":
            return UserProfile.objects.get(user = self.request.user)
        return super().get_object()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        user = instance.user
        tokens = get_tokens_for_user(user)
        return Response(tokens,status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=["post"])
    def user_login(self,request,*args,**kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user =  CustomUser.objects.get(username=username)
        except:
            return Response({"message":"Incorrect Username"},status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({"message":"Incorrect Password"},status=status.HTTP_404_NOT_FOUND)
        
        tokens = get_tokens_for_user(user)
        # profile_name = user.customer.profile_name
        # profile_data = {
        #     "profile_name":profile_name
        # }
        # tokens.update(profile_data)
        return Response(tokens,status=status.HTTP_200_OK)

