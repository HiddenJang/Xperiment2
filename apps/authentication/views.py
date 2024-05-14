from django.shortcuts import render, redirect

from .services.login_and_registration_service import EntranceService

#_____________Page render views______________#

def home_page(request):
    return render(request, 'home_page.html')

def login_page(request):
    login_result = EntranceService(request).login_user()
    if login_result["result"]:
        return redirect(login_result["page"])
    else:
        return render(request, login_result["page"], login_result["context"])

def reg_page(request):
    reg_result = EntranceService(request).registrate_user()
    if reg_result["result"]:
        return redirect(reg_result["page"])
    else:
        return render(request, reg_result["page"], reg_result["context"])
