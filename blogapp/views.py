from django.shortcuts import render, redirect
from . models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from . filters import NoteFilter
# Create your views here.
def home(request):

    return render(request,'main/land.html')

@login_required(login_url='/login/')
def addNotes(request):


    subs = Subject.objects.all()

    context = {

        'subj' : subs,

    }

    if request.method == 'POST':

        desc = request.POST.get('desc')
        mod = request.POST.get('moduleNo')
        file = request.FILES.get('file')

        typeN = request.POST.get('typeN')
        subje = request.POST.get('subjectName')

        # fs = FileSystemStorage()
        # filename=fs.save(file.name, file)
        # url = fs.url(filename)

        # if file.size < 20000000 :
        sub = Subject.objects.get(name = subje)
        des = f'{desc} - {mod} of {subje} : {typeN} by {request.user.name}'
        note = Notes(
            desc = des,
            mod = mod,
            file = file,
            author = request.user,
            typeN = typeN,
            sub = sub,
        )

        note.save()
        messages.success(request,'Sent for Verification Succesfully')
        return redirect('home')

        # else:

        #     messages.error(request,'file size should be less than 20 mb')
        #     return redirect('addNotes')
    else:
        return render(request,'main/addNotes.html',context)












@login_required(login_url='/login/')
def notes(request):
    notes = Notes.objects.filter(status = True)
    filteredNotes = NoteFilter(request.GET, queryset = notes)
    context = {
        'notes' : filteredNotes,
    }
    return render(request,'main/realHome.html',context)


@login_required(login_url='/login/')
def status(request):

    notes = Notes.objects.filter(author = request.user)
    context = {
        'notes' : notes,
    }

    return render(request,'main/status.html',context)

@login_required(login_url='/login/')
def noteDelete(request,slug):

    notes = Notes.objects.filter(slug = slug)
    notes.delete()
    messages.success(request,'Deleted Successfully')

    return redirect('status')

@login_required(login_url='/login/')
def searchNotes(request):

    if request.method == 'POST':

        searchQ = request.POST.get('searchQ')
        notes = Notes.objects.filter(desc__contains = searchQ)

        if notes is not None:
            context = {
                'notes' : notes,
                'ser' : searchQ
            }
            return render(request,'main/searchR.html',context)
    else:

        return render(request,'main/searchR.html')

def loginR(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email = email, password = password)

        if user is not None:
            login(request,user)
            messages.success(request,'Logged In Successfully')
            return redirect('home')

        else:
            messages.error(request,'Invalid Credentials')
            return render(request,'authentication/login.html')

    else:
        return render(request,'authentication/login.html')

def registerR(request):


    if request.method == 'POST':

        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')

        if UserAccount.objects.filter(email=email).exists():
            messages.warning(request,'User with this email already exists')
            return render(request,'authentication/register.html')
        else:

            myuser = UserAccount.objects.create_user(email, name, password)
            myuser.save()
            messages.success(request,'User Created Successfully')
            return render(request,'authentication/register.html')

    else:
        return render(request,'authentication/register.html')

def logoutR(request):
    logout(request)
    messages.success(request,'Logged Out Successfully')
    return redirect('loginR')

@login_required(login_url='/login/')
def noteViewer(request, slug):

    note = Notes.objects.filter(slug = slug)
    context = {
        'note' : note,
    }
    return render(request,'main/noteViewer.html',context)

def aboutUs(request):

    return render(request,'main/about.html')

@login_required(login_url='/login/')
def teacher(request):
    sub=Subject.objects.all()
    context={
        'sub':sub,
    }
    return render(request,'main/teacher.html',context)

def btmNav(request):

    notes = Notes.objects.filter(typeN='LectureSlides')
    return render(request,'main/btmNavSort.html',{'notes':notes})

@login_required(login_url='/login/')
def refeBk(request):

    notes = Notes.objects.filter(typeN='ReferenceBook')
    return render(request,'main/btmNavSort.html',{'notes':notes})

@login_required(login_url='/login/')
def pyqA(request):

    notes = Notes.objects.filter(typeN='PYQ')
    return render(request,'main/btmNavSort.html',{'notes':notes})

def error_404(request, exception):
    return render(request,'authentication/404.html')