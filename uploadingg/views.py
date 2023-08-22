from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from . models import ProjectItem
from django.core.files.storage import FileSystemStorage
from . forms import CardForm
from . models import Card
import os
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# for camera
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

# Create your views here.
# def home(request):
#     return HttpResponse('du befindest dich auf home')

#Login Requrierd


@login_required(login_url='login')
def inside(request):
    return render(request, '')

def loginPage(request):
    
    if request.user.is_authenticated:
        
        return redirect('postlogin')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            context={} 
            user = authenticate(request, username=username, password = password)

            if user is not None:
                
                login(request, user)
                
                return redirect('postlogin')
        
            else:
                
                messages.info(request, 'Username OR Password is Incorrect')
                return render(request, 'uploadd/login.html', context)

        context={} 
         
        return render(request, 'uploadd/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect ('login')


def home(request):
    return render(request, "uploadd/login.html")

def projects(request):
    return render(request, "uploadd/projects.html")

def camera(request):
    return render(request, 'uploadd/camera.html')

# ##### KAMERA DOPPELT DEFINIERT


# @gzip.gzip_page
# def camera(request):
#     try:
#         cam = VideoCamera()
#         return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
#     except:
#         pass
#     return render(request, 'uploadd/camera.html')

# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#         (self.grabbed, self.frame) = self.video.read()
#         threading.Thread(target=self.update, args=()).start
    
#     def __del__(self):
#         self.video.release()
    
#     def get_frame(self):
#         image = self.frame
#         _, jpeg = cv2.imencode('.jpeg', image)
#         return jpeg.tobytes()
    
#     def update(self):
#         while True:
#             (self.grabbed, self.frame) =self.video.read()

# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n\' + frame + b'\r\n\r\n')



def index(request):
    return render(request, 'uploadd/index.html')

def postlogin(request):
    return render(request, 'uploadd/postlogin.html')

def modal(request):
    return render(request, 'uploadd/modal.html')

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        # print(uploaded_file.name)
        # print(uploaded_file.size)
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name,uploaded_file)
        context['url'] = fs.url(name)
        # print(url)
        return render(request, "uploadd/upload.html", context, status=201)
    return render(request, "uploadd/upload.html", context)

def card_list(request):
    cards=Card.objects.all()
    return render(request, 'uploadd/card_list.html', {'cards': cards})

def card_question(request, *, id):
    cards=Card.objects.all()
    questioncard=None
    try:
         
        after=request.GET.get('after', None)
        before=request.GET.get('before', None)
        both=after and before
        if after is not None:
            questioncard=Card.objects.filter(id__gt=after).order_by('id')[0]
        elif before is not None:
            questioncard=Card.objects.filter(id__lt=before).order_by('-id')[0]
        # elif both:
        #     questioncard=Card.objects.filter(id__gt=after).order_by('id')[0]
        else:
            questioncard=Card.objects.all().order_by('id')[0]
    except IndexError:
        if len(cards) > 0:
            questioncard=cards[0]
    except ValueError:
        if len(cards) > 0:
            questioncard=cards[0]
    
    return render(request, 'uploadd/questionmodal.html', {'cards': cards,'questioncard': questioncard })
# #####


def questtheproject(request, *, id):
    cards=Card.objects.all()
    # questioncard=Card.objects.all()
    projectcards = cards.filter(side=id)
    # side = Card.objects.filter(side=id)

    # row_id = ProjectItem.objects.get(id=id)
    row_id = None
    # cards=Card.objects.filter(side=id)
    # questioncard=Card.objects.filter(side=id)

    # if row_id == side:
    #     print("name")
        
    # if row_id != side:
    #     print('noname')
    #     print(row_id)
    #     print(str(side))
    # questioncard=None
    try:
         
        after=request.GET.get('after', None)
        before=request.GET.get('before', None)
        both=after and before
        if after is not None:
            questioncard=projectcards.filter(id__gt=after).order_by('id')[0]
        elif before is not None:
            questioncard=projectcards.filter(id__lt=before).order_by('-id')[0]
        # elif both:
        #     questioncard=Card.objects.filter(id__gt=after).order_by('id')[0]
        else:
            print("hiiii")
            questioncard=projectcards.order_by('id')[0]
    
    except IndexError:
        if len(cards) > 0:
            questioncard=projectcards[0]
    except ValueError:
        if len(cards) > 0:
            questioncard=projectcards[0]
    return render(request,"uploadd/questionmodal.html",{'row':row_id,'cards':cards, 'questioncard': questioncard,'projectcards':projectcards })

    # except IndexError:
    #     if len(questioncard) > 0:
    #         questioncard=questioncard[0]
    # except ValueError:
    #     if len(questioncard) > 0:
    #         questioncard=questioncard[0]

    # return render(request,"uploadd/123.html",{'row':row_id,'questioncard':questioncard, 'questioncard': questioncard })


######123
def upload_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            # print("hez")
            form.save()
            return redirect('/card/')

    else: 
        form = CardForm()

    return render(request,'uploadd/upload_card.html',{'form' : form})

def delete_card(request, pk):
    if request.method == "POST":
        card = Card.objects.get(pk=pk)
        if card.front:
            
            os.remove(card.front.file.name)
        if card.back:
            os.remove(card.back.file.name)
        card.delete()
    return redirect('card_list')

def delete_project(request, pk):
    if request.method == "POST":
        projectitem = ProjectItem.objects.get(pk=pk)
        projectitem.delete()
    return redirect('myprojects')


def base(request):
    return render(request, "uploadd/base.html")
   

def logoutUser(request):
    logout(request)
    return redirect('/')

    ##############

def myprojects(request):
    
    if request.method == 'POST':
        
        print('Received data: ', request.POST['itemName'])
        ProjectItem.objects.create(name = request.POST['itemName']) 

    project_items = ProjectItem.objects.all()
    return render(request,"uploadd/myprojects.html", {'project_items': project_items})


def myprojects_details(request, * , id):
    row_id = ProjectItem.objects.get(id = id)
    cards=Card.objects.filter(side=id)
    return render(request,"uploadd/theproject.html",{'row':row_id,'cards':cards})





def addtheproject(request, * , id):
    row_id = ProjectItem.objects.get(id = id)
    cards=Card.objects.all()

    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            front = form.cleaned_data['front']
            back = form.cleaned_data['back']
            title = form.cleaned_data['title']
            # print("hez")
            card = Card.objects.create(title=title,front=front,back=back,side=id)
            card.save()
            return redirect('/myprojects/'+str(id))

    else: 
        form = CardForm()
    return render(request,"uploadd/addtheproject.html",{'row':row_id,'cards':cards,'form':form})



# def card_list(request):
#     cards=Card.objects.all()
#     return render(request, 'uploadd/card_list.html', {'cards': cards})

class CardListView(ListView):
    model=Card
    template_name="card_list.html" 
    context_object_name = 'card'


# class CardList(View):
#     def get(self, request):
#         pass
#     def post(self, request):
#         pass



# def delete_project(request, * ,id):
    
#     print('Received data: ', id)
#     ProjectItem.objects.filter(id=id).delete()

def search(request):
    print("asjdfkasf")

#### ausprobieren CSS und HTML scripts
def trial(request):
    return render(request, "triall/trial.html")
def hower(request):
    return render(request, "triall/hower.html")
def glowunder(request):
    return render(request, "triall/glowunder.html")
def modalpopup(request):
    return render(request, "triall/modalpopup.html")
def modalpopup2(request):
    return render(request, "triall/modalpopup2.html")
def altupload(request):
    return render(request, "triall/altupload.html")

def mutliple(request):
    return render(request, "triall/multiple.html")