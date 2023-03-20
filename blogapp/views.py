from django.shortcuts import render, redirect
from . models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from . filters import NoteFilter
# Create your views here.


def home(request):

    return render(request,'main/land.html')
@login_required(login_url='/login/')
def dashboard(request):

    return render(request,'main/dashboard.html')



# View for users to add notes starts here

@login_required(login_url='/login/')
def addNotes(request):    


    subs = Subject.objects.all()  #To display subjects in the dropdown menu
    coins = UserAccount.objects.get()

    context = {

        'subj' : subs,

    }

    if request.method == 'POST':

        desc = request.POST.get('desc')
        mod = request.POST.get('moduleNo')
        file = request.FILES.get('file')
        typeN = request.POST.get('typeN')
        subje = request.POST.get('subjectName')
        sub = Subject.objects.get(name = subje)   #Referencing Subject model since it is a foreignKey for Notes model

        des = f'{desc} - {mod} of {subje} : {typeN} by {request.user.name}'   #Creating custom description
        # detail = f'{subje}+ Module - {mod} - {typeN} by {request.user}'


        try:

            note = Notes(                    #creating a new object  of notes 
                desc = des,
                mod = mod,
                file = file,
                author = request.user,
                typeN = typeN,
                sub = sub,
                # nDetail = detail,
            )

            note.save()     #Saving the newly created object into the database

            messages.success(request,'Sent for Verification Succesfully')
            return redirect('home')
        
        except:
            messages.error(request,"Something went wrong please try again")
            return redirect('addNotes')

        
    else:
        return render(request,'main/addNotes.html',context)

#View for users to add notes ends here


#View for displaying notes in the notepage starts here

@login_required(login_url='/login/')
def notes(request):

    notes = Notes.objects.filter(status = True)      #Fetches only that notes which are accepted by the admin
    filteredNotes = NoteFilter(request.GET, queryset = notes)      #Using django-filter extension declared in filters.py file 
    context = {
        'notes' : filteredNotes,
    }
    return render(request,'main/realHome.html',context)

#View for displaying notes in the notepage ends here


#Status page table starts here

@login_required(login_url='/login/')
def status(request):

    notes = Notes.objects.filter(author = request.user) #Fetches only those notes which are uploaded by the respected user
    context = {
        'notes' : notes,
    }

    return render(request,'main/status.html',context)

#Status page table ends here


#For deleting uploaded notes by the respective user itself starts here
@login_required(login_url='/login/')
def noteDelete(request,slug):

    notes = Notes.objects.filter(slug = slug)
    notes.delete()
    messages.success(request,'Deleted Successfully')

    return redirect('status')

#deleting uploaded notes by the respective user itself ends here



@login_required(login_url='/login/')
def searchNotes(request):

    if request.method == 'POST':

        searchQ = request.POST.get('searchQ')
        notes = Notes.objects.filter(nDetail__contains = searchQ)

        if notes is not None:
            context = {
                'notes' : notes,
                'ser' : searchQ
            }
            return render(request,'main/searchR.html',context)
        else:
            return render(request,'main/searchR.html')

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



#Bottom nav views starts here
@login_required(login_url='/login/')
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

#bottom nav views ends here


def error_404(request, exception):
    return render(request,'authentication/404.html')



def searchRecmd(request):

    notes = request.GET.get('searchQ')
    rcmdList = []
    if notes:
        note = Notes.objects.filter(nDetail__icontains=notes)

        for n in note:
            rcmdList.append(n.nDetail)

    return JsonResponse({'status':200 , 'data' : rcmdList})