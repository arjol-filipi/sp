from core.models import Emplyee,Event
from rest_framework import permissions, viewsets

from .serializers import EmpyeeSerializer,EventSerializer

class EmplyeeViewset(viewsets.ModelViewSet):
    queryset = Emplyee.objects.all()
    permission_classes= [
        permissions.AllowAny
    ]
    serializer_class = EmpyeeSerializer

class EventViewset(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes= [
        permissions.AllowAny
    ]
    serializer_class = EventSerializer
