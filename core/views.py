from django.db.models import query
from django.shortcuts import render

from core.models import *
from core.serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.permissions import BasePermission

class UnauthenticatedPost(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['POST']


class UnauthenticatedGet(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET']


# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    
    queryset = Customer.objects.all()
    serializer_class = CustomerRegestirationSerializer
    permission_classes = [UnauthenticatedPost|UnauthenticatedGet]
 
    def create(self, request, *args, **kwargs):
        """ post request"""


        
        serializer = self.get_serializer(data=request.data)
        data = {}
        if serializer.is_valid():
            customer = serializer.save()
            data['response'] = "Customer registered successfully"
            data['email'] = customer.user.email
            data['first_name'] = customer.first_name
            token = Token.objects.get(user=customer.user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
    
    
    def list(self, request, *args, **kwargs):
        customers = self.get_queryset()
        serializer = CustomerSerializer(customers, many= True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def hi(self, request,**kwargs):
        item = Item.objects.get(id = 3)
        serailizer = ItemSerializer(item)
        return Response(serailizer.data)


class FoodVenueViewSet(viewsets.ModelViewSet):
    queryset = FoodVenue.objects.all()
    serializer_class = FoodVenueSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'location']



    def create(self, request, *args , **kwargs):
        serializer = self.get_serializer(data = request.data)
        data = {}
        if serializer.is_valid():
            venue = serializer.save()
            data['response'] = "Saved successfully"
            data['name'] = venue.name
        else:
            data = serializer.errors
        return Response(data)

  
    def update(self, request, *args, **kwargs):
        venue = self.get_object()
        data = request.data
        manager = User.objects.get_user(id= data['manager'])
        if manager:
            venue.manager = manager
            venue.name = data['name']
            venue.location = data['location']
            venue.image = data['image']
            venue.bank_account_number = data['bank_account_number']
            venue.save()
            serializer = self.get_serializer(venue)
            return Response(serializer.data)
        else:
            return Response("Manager not found",status = 404)
    

    @action(detail=True,url_path='Items')
    def getItems(self,request,**kwargs):
        food_venue = self.get_object()
        items = Item.objects.filter(food_venues=food_venue)
        serializer = ItemSerializer(items, many = True)
        if serializer.data:
            return Response(serializer.data)      
        return Response("No items available for this food venue", status = 404)

    
    @action(detail=True,methods=['POST','GET'])
    def review(self,request,**kwargs):
        if request.method == 'GET':
            """ get all reviews for a specific food venue"""
            food_venue = self.get_object()
            reviews = Review.objects.filter(food_venue= food_venue )
            serializer = ReviewSerializer(reviews, many= True)
            if serializer.data:
                return Response(serializer.data)
            return Response("No reviews available for this food venue",status = 404)
        else:
            """ Post request , add review for a specific food venue for a specific customer"""
            data = {}
            data['comment']= request.data['comment']
            data['rating']= request.data['rating']
            data['customer']= request.data['customer_id']
            data['food_venue']= kwargs['pk']
            serializer = ReviewSerializer(data= data)
            temp = {}
            if serializer.is_valid():
                review = serializer.save()
                temp['response'] = "Review added"
                temp ['comment'] = review.comment
            else:
                temp = serializer.errors
            return Response(temp)

        
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(detail=True,methods=['POST'])
    def favorite(self, request, **kwargs):
        """ get customer """
        item = self.get_object()
        customer = Customer.objects.get(user= request.user.id)
        item.favorite_by.add(customer)
        item.save()
        return Response("Success")
        

    @action(detail=False,methods=['GET'])
    def get_favorites(self, request, **kwargs):
        """ retruns all items favourite by a customer"""
        customer = Customer.objects.get(user= request.user.id)
        items = customer.item_set.all()
        serializer = ItemSerializer(items, many = True)
        return Response(serializer.data)
        
    @action(detail=True,methods=['GET'])
    def x(self, request, **kwargs):
        """ retruns all items favourite by a customer"""
        item = self.get_object()
        customers = item.favourite_by.all()
        serializer = CustomerSerializer(customers,many = True)
        return Response(serializer.data)


    @action(detail=True, methods=['POST'],url_path='assign')
    def assign_foodvenue(self,request, **kwargs):
        item = self.get_object()
        food_venue_id = request.data['food_venue']
        exist = FoodVenue.objects.is_exist(food_venue_id)
        if exist:
            food_venue = FoodVenue.objects.get(id=food_venue_id)
            item.food_venues.add(food_venue)
            return Response("Assigned Successfully")
        else:
            return Response("Food venue not found")

        
class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    
    @action(detail=True,methods=['POST'])
    def favorite(self, request, **kwargs):
        """ get customer """
        package = self.get_object()
        customer = Customer.objects.get(user= request.user.id)
        package.favorite_by.add(customer)
        package.save()
        return Response("Success")
        
    
class AvailableItemsViewSet(viewsets.ModelViewSet):
    queryset = available_item.objects.all()
    serializer_class = AvailableItemsCreateSerialzier

    def create(self, request, *args , **kwargs):
        """ adds a new item"""

        venue = FoodVenue.objects.get(manager = request.user)
        """ use filter 3shan lw msh mwgoda trg3 array fadya badl error"""
        item = Item.objects.filter(id = request.data['item'])
        if(item):
            data = {}
            data['food_venue'] = venue.id
            data['item'] = item[0].id
            data['quantity'] = request.data['quantity']
            data['discount'] = request.data['discount']
            data['price'] =  item[0].original_price - (item[0].original_price * int(data['discount'])/100)
            data['availablity_time'] = request.data ['availablity_time']

            serializer = self.get_serializer(data = data)
            response = {}
            if serializer.is_valid():
                available_item = serializer.save()
                response['response'] = "Added successfully"
                response['item_name'] = available_item.item.name
            else:
                data = serializer.errors
            return Response(data)
        return Response("no item found with this id")
       

    def list(self, request, *args, **kwargs):
        available_items = self.get_queryset()
        location = self.request.query_params.get('location')
        filtered_available_items =  []

        for item in available_items:
            if(item.food_venue.location ==location):
                filtered_available_items.append(item)

        serializer = AvailableItemsSerialzier(filtered_available_items, many= True)

        if(serializer.data):
        
            return Response(serializer.data)
        else:
            return Response("No available items for your current location" , status = 404)


class AvailablePackagesViewSet(viewsets.ModelViewSet):
    queryset = available_package.objects.all()
    serializer_class = AvailablePackagesCreateSerialzier

    def create(self, request, *args , **kwargs):
        """ adds a new item"""

        venue = FoodVenue.objects.get(manager = request.user)
        """ use filter 3shan lw msh mwgoda trg3 array fadya badl error"""
        package = Package.objects.filter(id = request.data['package'])
        
        if(package):
            data = {}
            data['food_venue'] = venue.id
            data['package'] = package[0].id
            data['quantity'] = request.data['quantity']
            data['discount'] = request.data['discount']
            data['price'] = 0
            for item in package[0].items.all():
                data['price'] += item.original_price
            data['price'] = data['price'] - (data['price'] * int(data['discount'])/100)
            data['availablity_time'] = request.data ['availablity_time']
            serializer = self.get_serializer(data = data)
            response = {}
            if serializer.is_valid():
                available_package = serializer.save()
                response['response'] = "Added successfully"
                response['package'] = available_package.package.name
            else:
                data = serializer.errors
            return Response(data)
        return Response("no package found with this id")
       
    

    def list(self, request, *args, **kwargs):
        available_packages = self.get_queryset()
        location = self.request.query_params.get('location')
        filtered_available_packages =  []

        for item in available_packages:
            if(item.food_venue.location ==location):
                filtered_available_packages.append(item)

        serializer = AvailablePackagesSerialzier(filtered_available_packages, many= True)

        if(serializer.data):
            return Response(serializer.data)
        else:
            return Response("No available items for your current location" , status = 404)



class OrdersViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    def create(self, request, *args , **kwargs):
        """post request for orders"""
        data = request.data
        return Response(data)