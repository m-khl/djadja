from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import libxml2dom
import urllib2
from django.conf import settings


def index(request):
    return render_to_response('bn/form.html',{'trs':[], 
                                              'subways':settings.SUBWAYS,
                                              "stations": [[code, text, False] for code, text in settings.SUBWAYS]},context_instance=RequestContext(request))

def handleAsk(request):
    formData = {"roomsFr" : request.POST.getlist('roomsFr')[0],
                                  "roomsTo" : request.POST.getlist('roomsTo')[0],
                                  "priceFr" : request.POST.getlist('priceFr')[0],
                                  "priceTo" : request.POST.getlist('priceTo')[0],
                                  "metros": "&".join([ "metro%5B%5D={0}".format(code) for code in request.POST.getlist('stations')]) }
    
    url = 'http://www.bn.ru/zap_fl.phtml?kkv1={roomsFr}&kkv2={roomsTo}&price1={priceFr}&price2={priceTo}&so1=&so2=&sk1=&sk2=&type%5B%5D=1&type%5B%5D=3&sorttype=0&sort_ord=0&{metros}&text='.format(**formData)
    formData["url"]=url
    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla Firefox"}) 
    f = urllib2.urlopen(req) 
    doc = libxml2dom.parse(f, html=1)
    trs=doc.xpath('//table[@class="results"]/tr')[3:]
    
    formData["trs"] = [ [ td.textContent for td in tds] for tds in 
                                      [tr.getElementsByTagName('td') for tr in trs] ]
    formData["stations"] = [[code, text, request.POST.getlist('stations').count(code)>0] for code, text in settings.SUBWAYS]
    
    return formData
    
def ask(request):
    return render_to_response('bn/form.html',
                              handleAsk(request) ,context_instance=RequestContext(request)) 
    
def ajaxAsk(request):
    return render_to_response('bn/table.html',
                              handleAsk(request) ,context_instance=RequestContext(request))
#HttpResponse("Hello, world. You're at the poll index %s." % request.POST.getlist('field')[0])

# Create your views here.
