import asyncio

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView

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
    def get(self, request, formant=None):
        start_time = time.time()
        res = start_scan.apply_async().get()
        finish_time = time.time()
        work_time = finish_time - start_time
        print(f'task {start_time} done success, finish_time={finish_time}, work_time=', work_time)
        return JsonResponse({"Success": f'{res}'}, status=200)


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
