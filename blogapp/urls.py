from django.urls import path, include
from . import views
urlpatterns = [

    path('', views.home,name='home'),
    path('addNotes/', views.addNotes,name='addNotes'),
    path('notes/', views.notes,name='notes'),
    path('dashboard/', views.dashboard,name='dashboard'),
    
    path('notes/<slug:slug>/',views.noteViewer,name='notesViewer'),
    path('status/',views.status,name='status'),
    path('status/<slug:slug>/',views.noteDelete,name='noteDelete'),
    path('searchNotes/',views.searchNotes,name='searchNotes'),
    path('login/', views.loginR,name='loginR'),
    path('logout/',views.logoutR,name='logout'),
    path('aboutus/',views.aboutUs,name='about'),
    path('register/',views.registerR,name='register'),
    path('teacher/',views.teacher,name='teacher'),
    path('btmNav/',views.btmNav,name='btmNav'),
    path('btmNav/<slug:slug>',views.noteViewer,name='btmNav'),
    path('referenceBooks/',views.refeBk,name='referenceBooks'),
    path('pyq/',views.pyqA,name='pyqA'),
    path('searchRecmd/',views.searchRecmd,name='searchRecmd'),
    path('adminResponse/',views.adminResponse,name='adminResponse'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
    path('acceptStatus/<slug:slug>/',views.acceptStatus,name='acceptStatus'),

]