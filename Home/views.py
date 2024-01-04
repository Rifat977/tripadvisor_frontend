from django.shortcuts import render




def home(request):

    return render(request,'home.html')


def places(request):

    return render(request,'places.html')


def chat(request):

    return render(request,'place_chat.html')



def sub_place(request):

    return render(request,'select_place.html')


def sub_sub_place(request):

    return render(request,'select-sub-place.html')


def sub_place_chatbox(request):

    return render(request,'select_sub_place_chat.html')