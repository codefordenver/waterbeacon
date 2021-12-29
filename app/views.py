from datetime import datetime
from django.shortcuts import render
from django.template import RequestContext
from django.http import JsonResponse
from django.middleware.csrf import get_token

# Create your views here.
def index(request):
	now = datetime.now()

	resp_dic = {
		'years': range(now.year -10, now.year),
		'months': [ datetime(1900, monthNum, 1).strftime('%b') for monthNum in range(1, now.month + 1 ) ]
	}

	return render(request, 'index.html' , resp_dic)

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})
