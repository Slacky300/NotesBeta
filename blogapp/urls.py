from django.urls import path, include
from . import views
urlpatterns = [

    path('', views.home,name='home'),
    path('addNotes/', views.addNotes,name='addNotes'),
    path('notes/', views.notes,name='notes'),
    path('notes/<slug:slug>/',views.noteViewer,name='notesViewer'),
    path('status/',views.status,name='status'),
    path('status/<slug:slug>/',views.noteDelete,name='noteDelete'),
    path('searchNotes/',views.searchNotes,name='searchNotes'),
    path('login/', views.loginR,name='loginR'),
    path('logout/',views.logoutR,name='logout'),
    path('aboutus/',views.aboutUs,name='about'),
]