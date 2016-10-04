from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.
def index(request):
	resp_dic = {}
	return render_to_response('index.html',resp_dic,context_instance=RequestContext(request))