import asyncio
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from rest_framework.views import APIView
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view

from celery.result import AsyncResult
from .tasks import start_scan
import time
import random



#_____________Page render views______________#
def scan_page(request):
    return render(request, 'scan_page.html')


#_____________API______________#
class ScannerStarter(View):

    def get(self, request):
        csrf = get_token(request)
        return JsonResponse({"csrftoken": csrf}, status=200)

    def post(self, request):
        start_time = time.time()
        scan_res = start_scan.apply_async(kwargs=json.loads(request.body)).get()
        finish_time = time.time()
        work_time = finish_time - start_time
        print(f'task {start_time} done success, finish_time={finish_time}, work_time=', work_time)
        return JsonResponse({"Success": f'{scan_res}'}, status=200)


# class TaskStateGetter(APIView):
#     def get(self, request, formant=None):
#         task_id = request.GET.get('task_id')
#         if task_id:
#             result = AsyncResult(task_id)
#             print(result.state)
#             return JsonResponse({"Success": result.state}, status=200)
#         return JsonResponse({"Success": "in progress"}, status=200)



# @api_view(['GET'])
# def run_scanning(request):
#     res = start_scan.delay()
#     print('flag1', res.state)
#     return JsonResponse({"Success": "success!"}, status=200)
