from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie,Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,) #AllowAny must be imported to use
    
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:      

            movie=Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            #user = User.objects.get(id=1)
            print('user',user)

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating)
                response = {'message': 'Rating updated successfully','result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating)
                response = {'message': 'Rating created!!','result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'you need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)

    def update(self, request ,*args, **kwargs):
        response = {'message': 'you can not update the rating'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request ,*args, **kwargs):
        response = {'message': 'you can not create the rating'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

