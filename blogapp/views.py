from django.forms import SlugField
from django.shortcuts import render, redirect,get_object_or_404
from . models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from . filters import NoteFilter
from django.db.models import Count,Sum
from django . urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

# for user in UserAccount.objects.all():
#     user.coins_scored -=100
#     user.save()


def home(request):

    return render(request,'main/land.html')


def adminResponse(request):

    notes = Notes.objects.all()
    context = {
        'notes' : notes,
    }

    return render(request,'main/adminTem/adminCrud.html',context)


@login_required(login_url='/login/')
def dashboard(request):
    user_id=request.user.id
    user = UserAccount.objects.get(id=user_id)
    rank = UserAccount.objects.filter(coins_scored__gt=user.coins_scored).aggregate(rank=Count('coins_scored'))['rank'] + 1
    notes = Notes.objects.filter(author = request.user,status=True)
    note_likes = notes.annotate(likes_count=Count('likes')).aggregate(total_likes=Sum('likes_count'))['total_likes']
    context = {
        'notes' : notes,
        'note_likes':note_likes,
        'rank':rank,
        
    }
    return render(request,'main/dashboard.html',context)



# View for users to add notes starts here
@login_required(login_url='/login/')
def addNotes(request):    


    subs = Subject.objects.all()  #To display subjects in the dropdown menu

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
        details = f'{sub.name}  Module - {mod} - {typeN} by {request.user}'

        try:

            note = Notes(                    #creating a new object  of notes 
                desc = des,
                mod = mod,
                file = file,
                author = request.user,
                typeN = typeN,
                sub = sub,
                nDetail = details,
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
        notes = Notes.objects.filter(nDetail__contains = searchQ,status=True)

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

    notes = Notes.objects.filter(status=True,typeN='ReferenceBook')
    return render(request,'main/btmNavSort.html',{'notes':notes})



@login_required(login_url='/login/')
def pyqA(request):

    notes = Notes.objects.filter(status=True,typeN='PYQ')
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


def acceptStatus(request,slug):

    notes = Notes.objects.get(slug=slug)
    user = UserAccount.objects.get(email = notes.author.email)
    if notes.status:
        notes.status = False
        notes.save()
        user.coins_scored = user.coins_scored - 50
        user.save()
        messages.success(request,'Notes rejected successfully')
        return redirect('adminResponse')
    else:
        notes.status = True
        notes.save()
        user.coins_scored = user.coins_scored + 50
        user.save()
        messages.success(request,'Notes accepted successfully')
        return redirect('adminResponse')
    
def notesuploded(request):
    notes = Notes.objects.filter(author = request.user,status=True) #Fetches only those notes which are uploaded by the respected user
    context = {
        'notes' : notes,
    }

    return render(request,'main/notesuploded.html',context)




@login_required(login_url='/login/')
def leaderboard(request):
    # users_above = UserAccount.objects.filter(coins_scored__gt=UserAccount.coins_scored)
    # rank = users_above.count() + 1
    
    users = UserAccount.objects.all().order_by('-coins_scored')
    top_users = UserAccount.objects.order_by('-coins_scored')[:3] # Assuming 'coins' is the field used for ranking

    # users = UserAccount.objects.all().order_by('-coins_scored')[:10] 

    
    # users = UserAccount.objects.order_by('-coins_scored')
    paginator = Paginator(users, 15)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={
        'users': users,'notes' : notes,'page_obj':page_obj,'top_users': top_users,
    }
   
    return render(request, 'main/leader.html',context)

# @login_required(login_url='/login/')
# def like_notes(request,pk):
#      notes=get_object_or_404(Notes,id=request.POST.get('notes_like'))
#      notes.likes.add(request.user)

#      return HttpResponseRedirect(reverse('notesViewer',args=[str(pk)]))

# def like_notes(request,slug):
#     note= get_object_or_404(Notes, slug=SlugField)
#     if request.method == 'POST':
#         note.likes += 1
#         note.save()
#         note.likes.add(request.user)
#         return HttpResponseRedirect(reverse('notesViewer', args=[SlugField]))
     
@login_required(login_url='/login/')
def like_notes(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    user=request.user
    liked = note.likes.filter(id=user.id).exists()
    if request.method == 'POST':
        if note.likes.filter(id=user.id).exists():
            note.likes.remove(user)
        else:
            note.likes.add(user)
        return HttpResponseRedirect(reverse('notesViewer', args=[note.slug]))
   
    



    


#for the likes of the specific page
@login_required(login_url='/login/')
def notes_likes(request):
    user = request.user
    notes = Notes.objects.filter(author=user,status=True)
    notes_with_likes = []
    for note in notes:
        num_likes = note.likes.count()
        notes_with_likes.append((note, num_likes))
    context = {
        'notes':notes,
        'notes_with_likes': notes_with_likes
    }
    return render(request, 'main/noteslikes.html', context)
def addDriveLink(request,slug):

    if request.method == 'POST':
        try:

            link = request.POST.get('dLink')
            print(link)
            note = Notes.objects.get(slug=slug)
            note.docid = link
            note.save()
            messages.success(request,"Drive link added successfully")
            return redirect('adminResponse')
        except:
            messages.error(request,"Failed to add drive link")
            return redirect('adminResponse')


def upDelete(request,slug):
    try:
        note = Notes.objects.get(slug=slug)
        note.delete()
        messages.success(request,"Note Deleted Successfully")
        return redirect('adminResponse')
    except:
        messages.error(request,"Failed to Delete")
        return redirect('adminResponse')