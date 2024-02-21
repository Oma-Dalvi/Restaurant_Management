from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer

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
        serializers = RestaurantSerializer()
        return Response({'serializers': serializers})

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
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

    def post(self, request):
        serializer = RestaurantLoginSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('restaurants-home')
        else:
            return Response({'serializers': serializer})


class RestaurantListView(APIView):

    def get(self, request):
        try:
            queryset = Restaurant.objects.all()
            serializer = RestaurantSerializer(queryset, many=True)
            return Response({"data": serializer.data, "status": status.HTTP_201_CREATED})
        except:
            return Response({"error": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})

    def post(self, request):
        try:
            pass
        except:
            pass

    def put(self, request):
        try:
            pass
        except:
            pass
