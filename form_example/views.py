from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def myform(request):
    print(request.GET)
    return render(request, 'myform.html')
