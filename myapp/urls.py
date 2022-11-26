from . import views
from django.urls import path
 
urlpatterns = [
    path('',views.index, name='index'),
    path('story',views.story, name='story'),
    path('showIm',views.showIm, name='showIm'),
    path('landingpage',views.landingpage, name='landingpage'),
    path('show',views.show, name='show')
]