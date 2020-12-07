from django.shortcuts import render,redirect
from .models import Person,Group,Membership,MessageForm,Messageship,Message_seen
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PersonSerializer,GroupSerializer,MessageSerializer,Mess
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .forms import SimpleForm
from django.utils import timezone
from phaseone.forms import TempForm
from django.http import Http404
from rest_framework.views import APIView
from pyfcm import FCMNotification
from datetime import datetime

def manage(request,ide):
    if not request.user.is_authenticated:
        return redirect('/login')
    profname=request.user
    form1 = SimpleForm()
    form2 = SimpleForm()
    l = []
    l2=[]
    grp=get_object_or_404(Group, name=ide,prof=request.user)


    
    if request.method =='POST': 
        dict=request.POST
        print(dict)
        a=dict.getlist('student')
        if 'add' in dict:
            for studentid in a:
                per=Person.objects.get(userid=studentid)
                Membership.objects.create(person=per,group=grp)
        if 'remove' in dict:
            for studentid in a:
                per=Person.objects.get(userid=studentid)
                grp.members.remove(per)

    a=Person.objects.all()
    members=grp.members.all()
    for x in a:
        if x not in members:
            l2.append((x.userid,x.name))
    form2.fields['student'].choices = l2
    for x in members:
        l.append((x.userid,x.name))
    form1.fields['student'].choices = l
    return render(request,'manage_students.html',{'form1':form1,'form2':form2,'course':ide})

def ta(request,ide):
    return render(request,'manage_ta.html',{ 'course':ide})

def course(request,ide):
    
        grp=get_object_or_404(Group, name=ide,prof=request.user)
        b=request.POST
        form = TempForm(request.POST or None, request.FILES or None)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")

        if request.method =='POST':     
            if form.is_valid(): 
                timezone.activate('Asia/Kolkata')
                time=datetime.utcnow()
                messenger = request.user
                print(messenger)
                printer=str(messenger)+"         "+str(time)
                MessageForm.objects.create(time=time,header=b['header'],text=b['text'],priority=b['priority'],printer=printer)
                print(timezone.now())
                message=MessageForm.objects.get(time=time)
                Messageship.objects.create(group=grp,form2=message)
                push_service = FCMNotification(api_key="AAAAvHIUUss:APA91bElas2wl0uWdjmnQimvMQBgYX2XpFr75ilust04cMLFzbe04eoNSPMK-3wV8DAMhgX8hvQ0LGyEhw4sCzSFY0D3abUEVZM8BBy6yhPTViO_f35LJaBwgdjFCio0Y9bOq-sSnNfI")
                registration_ids = []
                for x in grp.members.all():
                    registration_ids.append(x.Token_key)
                print(registration_ids)
                message_title = b['header']
                print(message_title)
                message_body = b['text']
                result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
                print(result)
                form = TempForm()      
        
        
        messages = grp.messages.all()
        
        return render(request,'courses.html',{ 'course' : ide , 'messages' : messages ,'form':form})

def home(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    msg=""
    if request.method =='POST': 
        dict=request.POST
        grpname=dict['group_name']
        grpname=str(grpname)+" "+str(request.user)
        a=Group.objects.filter(prof=request.user).filter(name=grpname).exists()
        if a :
            msg="course name already exists"
        elif grpname!="":
            Group.objects.create(name=grpname,prof=request.user,grp_name=grpname)
    a=Group.objects.filter(prof=request.user)
    print(a)
    bool=0
    for x in a:
        bool=x.bool

    return render(request,'home.html',{'courses':a,'msg':msg,'bool' : bool}) 

class PersonList(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class MessageList(generics.ListCreateAPIView):
    queryset = MessageForm.objects.all()
    serializer_class = MessageSerializer

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MessageForm.objects.all()
    serializer_class = MessageSerializer

class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Person.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PersonSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PersonSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessList(generics.ListCreateAPIView):
    queryset = Message_seen.objects.all()
    serializer_class = Mess

class MessDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message_seen.objects.all()
    serializer_class = Mess