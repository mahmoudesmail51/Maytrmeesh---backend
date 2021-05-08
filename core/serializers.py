from rest_framework import serializers

from core.models import *

class CustomerRegestirationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'},write_only= True )
    password2 = serializers.CharField(style={'input_type': 'password'},write_only= True  )
    class Meta:
        model = Customer
        fields = ['email','password','password2','first_name', 
                'last_name','date_of_birth','phone_number']
        extra_kwargs = {
            'password':{'write_only': True},
            'password2':{'write_only': True}
        }
    
    def save(self):
        """ saves a new user and return it"""
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match'})  
        email = self.validated_data['email']
        user = User.objects.create_user(email=email, password= password)
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        date_of_birth = self.validated_data['date_of_birth']
        phone_number = self.validated_data['phone_number']
        user.is_customer = True
        user.save()
        customer = Customer.objects.create_customer(user=user, first_name=first_name, last_name=last_name,date_of_birth=date_of_birth,phone_number=phone_number)

        return customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class FoodVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodVenue
        fields = ['owner', 'name', 'location', 'image','bank_account_number'
                 ]
    
    def save(self):
        """ saves a new food venue and returns it"""
        owner_id = self.validated_data['owner']
        name = self.validated_data['name']
        location = self.validated_data['location']
        image = self.validated_data['image']
        bank_account_number = self.validated_data['bank_account_number']
        venues = FoodVenueManager.get_venues(self,location= location)
        for venue in venues:
            if(venue.name == name and venue.location == location):
                raise serializers.ValidationError ({'venue':'already exist with same name and location'})
        venue = FoodVenue.objects.create_venue(owner= owner_id, name= name, location= location, image= image, bank_account_number= bank_account_number)
        return venue