from django.contrib import admin
from django.urls import path
from rest_framework import routers
from api import views
from django.conf.urls import url, include
from .views import CustomObtainAuthToken,CreateRating,UserCreate,SpecificMovieRatingView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'movies', views.MovieViewSet)
router.register(r'ratings', views.RatingViewSet)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('authentication', CustomObtainAuthToken.as_view()),
    path('create_rating',views.CreateRating.as_view()),
    path('create_user',views.UserCreate.as_view()),
    path('specific_movierating/<movie>',views.SpecificMovieRatingView.as_view()),

]
