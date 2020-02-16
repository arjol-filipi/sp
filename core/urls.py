from django.urls import include, path
from rest_framework import routers
from core import views
from core.views import EventDetail,EventList
from .api import EmplyeeViewset,EventViewset
app_name = 'core'


router = routers.DefaultRouter()
router.register(r'api/emplyee',EmplyeeViewset,'emplyee')
router.register(r'api/event',EventViewset,'event')
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.Home, name='home'),
    path('event/<pk>/', EventDetail.as_view(), name='event'),
    path('eventlist/', EventList.as_view(), name='eventlist'),
    path('add/', views.Add, name='add'),
    path('monitor/', views.Monitor, name='monitor'),
    path('card/', views.CardView, name='card'),
    path('change-event/', views.ChangeEvent, name='change-event'),
    path('make-card/<pk>/', views.MakeCard, name='make-card'),
    path('make-event/', views.MakeEvent, name='make-event'),
    path('manual-event/', views.MakeView, name='manual-event'),
    path('norma/', views.Norma, name='norma'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]