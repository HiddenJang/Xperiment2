from django.shortcuts import render

#_____________Page render views______________#

def home_page(request):
    return render(request, 'home_page.html')

def login_page(request):
    return render(request, 'login_page.html')

def reg_page(request):
    return render(request, 'reg_page.html')
