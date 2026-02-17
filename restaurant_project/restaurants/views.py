from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

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

    def post(self, request):
        serializer = RestaurantLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['restaurant_name']
            password = serializer.validated_data['password']
            try:
                restaurant = Restaurant.objects.get(restaurant_name=username)
                # Manually check password
                if check_password(password, restaurant.password):
                    # Log in the user manually
                    request.session['user_id'] = restaurant.pk
                    return redirect('restaurants-menu', pk=restaurant.pk)
                else:
                    return Response({'serializers': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            except Restaurant.DoesNotExist:
                return Response({'serializers': 'Invalid username'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'serializers': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantLogout(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return redirect('restaurants-login')


class RestaurantOwnMenuAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'OwnMenu.html'

    def get(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        menus = RestaurantMenu.objects.filter(restaurant=restaurant).select_related('menu_type')
        menu_data = [{'id': menu.id, 'name': menu.menu_type.menu_name} for menu in menus]
        return Response({'restaurant': restaurant, 'menus': menu_data}, status=status.HTTP_200_OK)


class AddRestaurantMenuAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'add_menu.html'

    def get(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        return Response({'restaurant': restaurant, 'menu_types': MenuType.objects.all()})

    def post(self, request, pk):
        try:
            restaurant = get_object_or_404(Restaurant, pk=pk)
            menu_type_id = request.data.get('menu_type_id')
            new_menu_type_name = request.data.get('new_menu_type')

            if new_menu_type_name:
                # Create new MenuType if provided
                menu_type, created = MenuType.objects.get_or_create(menu_name=new_menu_type_name)
            elif menu_type_id:
                # Use existing MenuType
                menu_type = get_object_or_404(MenuType, pk=menu_type_id)
            else:
                return Response({'error': 'Please select an existing menu type or provide a new one.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check if the menu already exists for this restaurant
            if RestaurantMenu.objects.filter(restaurant=restaurant, menu_type=menu_type).exists():
                return Response({'error': 'This menu already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the new menu
            RestaurantMenu.objects.create(restaurant=restaurant, menu_type=menu_type)
            return redirect('restaurants-menu', pk=restaurant.pk)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantMenuDeleteAPIView(APIView):
    def post(self, request, menu_id, *args, **kwargs):
        menu = get_object_or_404(RestaurantMenu, id=menu_id)
        restaurant_id = menu.restaurant.restaurant_id
        menu.delete()
        return redirect('restaurants-menu', pk=restaurant_id)


class RestaurantMenuDishesAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu_dishes.html'

    def get(self, request, menu_id):
        menu = get_object_or_404(RestaurantMenu, pk=menu_id)
        dishes = MenuDish.objects.filter(menu=menu)
        return Response({'menu': menu, 'dishes': dishes})


class AddDishToMenuAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'add_dish.html'

    def get(self, request, menu_id):
        menu = get_object_or_404(RestaurantMenu, pk=menu_id)
        return Response({'menu': menu})

    def post(self, request, menu_id):
        menu = get_object_or_404(RestaurantMenu, pk=menu_id)

        serializer = MenuDishCreateSerializer(
            data=request.data,
            context={'menu': menu}
        )

        if serializer.is_valid():
            serializer.save()
            return redirect('restaurants-menu-dishes', menu_id=menu.id)

        # If validation fails
        return Response(
            {'menu': menu, 'errors': serializer.errors},
            status=400
        )


class RestaurantDishDeleteAPI(APIView):
    def post(self, request, menu_id, *args, **kwargs):
        menu_dish = get_object_or_404(MenuDish, id=menu_id)
        restaurant_menu_id = menu_dish.menu.id
        menu_dish.delete()
        return redirect('restaurants-menu-dishes', menu_id=restaurant_menu_id)