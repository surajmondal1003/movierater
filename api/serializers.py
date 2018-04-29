from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from api.models import Movie,Rating

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ( 'id','username', 'email')
        extra_kwargs={'password':{'write_only':True,'required':True}}

        def create(self,validated_data):
            user=User.objects.create(**validated_data)

            return user



class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',


        ]

class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'description',
            'avg_rating',
            'no_of_ratings'


        ]

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            'stars',
            'user',
            'movie',


        ]