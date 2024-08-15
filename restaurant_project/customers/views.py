from django.contrib.auth import logout
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password

from .serializers import *
from restaurants.models import Restaurant
from .serializers import RestaurantListSerializer


class CustomerRegistrationAPi(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customerregister.html'

    def get(self, request):
        serializer = CustomerRegisterSerializer()
        return Response({'serializers': serializer})

    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('restaurants-login')
        else:
            return Response({'serializers': serializer})


class CustomerLoginAPi(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer_login.html'

    def get(self, request):
        serializer = CustomerLoginSerializer()
        return Response({'serializers': serializer})

    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['customer_name']
            password = serializer.validated_data['password']
            try:
                customer = Customer.objects.get(customer_name=username)
                # Manually check password
                if check_password(password, customer.password):
                    # Log in the user manually
                    request.session['user_id'] = customer.pk
                    return redirect('restaurant-list')
                else:
                    return Response({'serializers': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            except Customer.DoesNotExist:
                return Response({'serializers': 'Invalid username'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'serializers': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantListApi(APIView):
    # permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'restaurant_list.html'

    def get(self, request):
        try:
            queryset = Restaurant.objects.all()

            serializer = RestaurantListSerializer(queryset, many=True)
            return Response({"data": serializer.data, "status": status.HTTP_201_CREATED})
        except:
            return Response({"error": serializers.error, "status": status.HTTP_400_BAD_REQUEST})


class CustomerLogout(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return redirect('restaurants-login')
