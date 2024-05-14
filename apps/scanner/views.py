from django.shortcuts import render
from .tasks import start_scan

from django.http import JsonResponse
from rest_framework.decorators import api_view


#_____________Page render views______________#
def scan_page(request):
    return render(request, 'scan_page.html')


#_____________API______________#
@api_view(['GET'])
def run_scanning(request):
    forks = start_scan.delay()
    print(forks)
    return JsonResponse({"Success": "true"}, status=200)
