from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *


class RestaurantHome(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'restaurant_home.html'

    def get(self, request):
        return Response({"status": status.HTTP_201_CREATED})


class RestaurantRegister(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'restaurant_registration.html'

    def get(self, request):
        serializers = RestaurantRegisterSerializer()
        return Response({'serializers': serializers})

    def post(self, request):
        serializer = RestaurantRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('restaurants-login')
        else:
            return Response({'serializers': serializer})


class RestaurantLogin(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'restaurant_login.html'

    def get(self, request):
        serializers = RestaurantLoginSerializer()
        return Response({'serializers': serializers})

    # def post(self, request):
    #     serializer = RestaurantLoginSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return redirect('restaurants-home')
    #     else:
    #         return Response({'serializers': serializer})

    def post(self, request):
        serializer = RestaurantLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                restaurant = Restaurant.objects.get(restaurant_name=username)
                if check_password(password, restaurant.password):
                    return redirect('restaurants-menu', pk=restaurant.pk)
                    # return Response({'message': 'Authentication successful'}, status=status.HTTP_200_OK)
                else:
                    return Response({'serializers': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            except Restaurant.DoesNotExist:
                return Response({'serializers': 'Invalid username'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'serializers': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantOwnMenuAPI(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'OwnMenu.html'

    def get(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            serializers = restaurant.menus.all()
            return Response({'serializers': serializers}, status=status.HTTP_200_OK)
        except:
            return Response({'serializers': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantListView(APIView):

    def get(self, request):
        try:
            queryset = Restaurant.objects.all()
            serializer = RestaurantSerializer(queryset, many=True)
            return Response({"data": serializer.data, "status": status.HTTP_201_CREATED})
        except:
            return Response({"error": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})
