from django.shortcuts import render
# Create your views here.
from django.contrib.auth.models import User
from api.models import Movie,Rating
from rest_framework.views import APIView
from rest_framework import viewsets,status
from api.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    MovieSerializer,
    RatingSerializer)


from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from api.pagination import RatingLimitOffestpagination,RatingPageNumberPagination




class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]


class CustomObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response=super(CustomObtainAuthToken,self).post(request,*args,**kwargs)
        token=Token.objects.get(key=response.data['token'])
        user=User.objects.get(id=token.user_id)
        serializer=UserLoginSerializer(user,many=True)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username':user.username,
            'email': user.email


        })

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [TokenAuthentication]

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    #permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = RatingPageNumberPagination



class UserCreate(APIView):
    """
    Creates the user.
    """

    def post(self, request, format='json'):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateRating(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    #serializer_class = RatingSerializer

    def post(self,request,format=None):


        if 'movie' in request.data and 'user' in request.data and 'stars' in request.data:
            movie=Movie.objects.get(id=request.data['movie'])
            user=User.objects.get(id=request.data['user'])
            stars=request.data['stars']

            try:
                rating=Rating.objects.get(movie=movie,user=user)
                rating.stars=stars
                rating.save()
                serializer=MovieSerializer(movie,many=True)
                data={'movie':movie.id,'user':user.id,'stars':stars}
                response={'message':'Rating Updated','data':data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                Rating.objects.create(movie=movie,user=user,stars=stars)
                serializer = MovieSerializer(movie, many=True)
                data = {'movie': movie.id, 'user': user.id, 'stars': stars}
                response = {'message': 'Rating Created','data':data}
                return Response(response, status=status.HTTP_200_OK)



        else:
            response={'message':'You need to pass All parameters'}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)







