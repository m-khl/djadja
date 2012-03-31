from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import libxml2dom
import urllib2


def index(request):
    return render_to_response('bn/form.html',{'trs':[]},context_instance=RequestContext(request))

def handleAsk(request):
    formData = {"roomsFr" : request.POST.getlist('roomsFr')[0],
                                  "roomsTo" : request.POST.getlist('roomsTo')[0],
                                  "priceFr" : request.POST.getlist('priceFr')[0],
                                  "priceTo" : request.POST.getlist('priceTo')[0]}
    req = urllib2.Request('http://www.bn.ru/zap_fl.phtml?kkv1={roomsFr}&kkv2={roomsTo}&price1={priceFr}&price2={priceTo}'
                          .format(**formData), headers={'User-Agent' : "Mozilla Firefox"}) 
    f = urllib2.urlopen(req) 
    doc = libxml2dom.parse(f, html=1)
    trs=doc.xpath('//table[@class="results"]/tr')[3:]
    
    formData["trs"] = [ [ td.textContent for td in tds] for tds in 
                                      [tr.getElementsByTagName('td') for tr in trs] ]
    return formData
    
def ask(request):
    return render_to_response('bn/form.html',
                              handleAsk(request) ,context_instance=RequestContext(request)) 
    
def ajaxAsk(request):
    return render_to_response('bn/table.html',
                              handleAsk(request) ,context_instance=RequestContext(request))
#HttpResponse("Hello, world. You're at the poll index %s." % request.POST.getlist('field')[0])

# Create your views here.
