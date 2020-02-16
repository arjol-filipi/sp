from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django.core import serializers
from .serializers import UserSerializer, GroupSerializer
from django.views.decorators.http import require_GET,require_POST
from django.contrib.auth.decorators import login_required
from .models import Emplyee,UserProfile,Event
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView,ListView

# qr
import django.contrib.staticfiles.finders as finders
from PIL import ImageDraw, ImageFont,Image
import datetime
import qrcode

from io import BytesIO


@csrf_exempt
@require_POST
def ChangeEvent(request):
    type_of = request.POST.get('type')
    data = request.POST.get('data')
    ev_pk = request.POST.get('pk')
    ev = Event.objects.filter(pk=ev_pk)[0]
    userprofile = UserProfile.objects.get(user=request.user)
    if userprofile.trusted_by:
        o = userprofile.trusted_by
    else:
        o = request.user    
    if type_of=='make':
        name = request.POST.get('name')
        start = datetime.datetime.strptime(data, "%m/%d/%Y %I:%M %p")
        t =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emp = Emplyee.objects.filter(name = name)[0]
        to_change_ev = Event.objects.filter(emplyee=emp).filter(time__lte=t,
            time__gt=start)
            
        for chev in to_change_ev:
            
            chev.enter = not chev.enter
            chev.save()
        emp.at_work = not emp.at_work
        emp.save()
        new_ev=Event.objects.create(emplyee= emp,user=o,enter= emp.at_work,time = datetime.datetime.strptime(data, "%m/%d/%Y %I:%M %p"))
        
        return HttpResponse(new_ev.id)
    elif type_of=='change':
        if o == ev.emplyee.user:
            ev.time = datetime.datetime.strptime(data, "%m/%d/%Y %I:%M %p")
            ev.save()
            return HttpResponse(ev.time)
        else:
            return HttpResponse("You are not authorised")
    elif type_of=='delete':
        if o == ev.emplyee.user:
            start = datetime.datetime.strptime(data, "%m/%d/%Y %I:%M %p")
            t =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            to_change_ev = Event.objects.filter(emplyee=ev.emplyee).filter(time__lte=t,
            time__gt=start)
            
            for chev in to_change_ev:
                
                chev.enter = not chev.enter
                chev.save()
            ev.emplyee.at_work = not ev.emplyee.at_work
            ev.emplyee.save()
            ev.delete()
            return HttpResponse("Deleted")
        else:
            return HttpResponse("You are not authorised")
    return HttpResponse("Type not specified")
@csrf_exempt
@require_POST
# @login_required
def MakeEvent(request):
    data = request.POST.get('data')
    
    name,card_id = data.split(':::with:::')
    
    emp = Emplyee.objects.filter(name = name)[0]
    userprofile = UserProfile.objects.get(user=request.user)
    if userprofile.trusted_by:
        o = userprofile.trusted_by
    else:
        o = request.user
    emp.at_work = not emp.at_work
    emp.save()
    new_ev=Event.objects.create(emplyee= emp,user=o,enter= emp.at_work)
    return HttpResponse(new_ev.id)

# @login_required
class EventDetail(DetailView):
    model = Event
    template_name = "event.html"

# @login_required
class EventList(ListView):
    
    model = Event
    template_name = "eventlist.html"
    def get_queryset(self):
        userprofile = UserProfile.objects.get(user= self.request.user)
        if userprofile.trusted_by:
            o = userprofile.trusted_by
        else:
            o = self.request.user
        object_list = Event.objects.filter(user=o)
        return object_list.order_by('-time')


@require_POST
@login_required
def MakeCard(request,pk=None):
    print(str(type(pk)))
    if pk==None:
        return HttpResponseBadRequest("Must provide employee")
    if request.method == 'POST':
        emp = Emplyee.objects.filter(pk=int(pk))[0]
        userprofile = UserProfile.objects.get(user=request.user)
        if userprofile.trusted_by:
            o = userprofile.trusted_by
        else:
            o = request.user
        
        bg = Image.open(finders.find('bg.jpg'))
         
        image = bg.resize((1000,620))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 15)
        d_date = datetime.datetime.now()
        draw.text((50, 50),"Company:   "+ o.username, fill=('rgb(0,0,0)'), font=font)
        draw.text((50, 250), "Name:     "+emp.name, fill=('rgb(0,0,0)'), font=font)
        if emp.position:
            draw.text((50, 350), "Position:    "+emp.position, fill=('rgb(0,0,0)'), font=font)
        else:
            draw.text((50, 350), "Position:    Unspecified", fill=('rgb(0,0,0)'), font=font)
        draw.text((250, 350), "created on:     "+d_date.strftime("%m/%d/%Y"), fill=('rgb(0,0,0)'), font=font)
        # image.save(str(name)+".png")
        img = qrcode.make(str(emp.name)+':::with:::'+emp.card_id)
        img = img.resize((300,300),Image.ANTIALIAS)
        image.paste(img,(590,340))
        import base64
        buffered = BytesIO()
        image.save(buffered, "PNG")
        
        img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
        return HttpResponse(img_str)
        # image.save(blob, 'JPEG')
        # return HttpResponse(emp.card.url)
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
def Home(request):
    return render(request,'home.html')

@login_required
def Add(request):
    return render(request,'add.html')

@login_required
def Monitor(request):
    return render(request,'qrcode.html')
    

@login_required
def CardView(request):
    userprofile = UserProfile.objects.get(user=request.user)
    if userprofile.trusted_by:
        o = userprofile.trusted_by
    else:
        o = request.user
    qs = Emplyee.objects.filter(user=o)
    context={
        'emp':qs
    }
    return render(request,'card.html',context)

@login_required
def MakeView(request):
    userprofile = UserProfile.objects.get(user=request.user)
    if userprofile.trusted_by:
        o = userprofile.trusted_by
    else:
        o = request.user
    qs = Emplyee.objects.filter(user=o)
    context={
        'emp':qs
    }
    return render(request,'make-event.html',context)

@login_required
def Norma(request):
    userprofile = UserProfile.objects.get(user=request.user)
    if userprofile.trusted_by:
        o = userprofile.trusted_by
    else:
        o = request.user
    qs = Emplyee.objects.filter(user=o)

    context={
        'emp':qs
    }
    if request.method=='GET':
        return render(request,'norma.html',context)