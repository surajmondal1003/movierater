from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from api.models import Movie,Rating
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ( 'id','username', 'email','url')


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=5)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')



class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',


        ]


# def restrict_rating(value):
#     raise serializers.ValidationError("You are no eligible for the job")



class RatingSerializer(ModelSerializer):

    #stars=serializers.IntegerField(validators=[restrict_rating])

    class Meta:
        model = Rating
        fields = [
            'stars',
            'user',
            'movie',

        ]


class MovieSerializer(ModelSerializer):
    movie_ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [

            'id',
            'title',
            'description',
            'avg_rating',
            'no_of_ratings',
            'movie_ratings'
        ]






