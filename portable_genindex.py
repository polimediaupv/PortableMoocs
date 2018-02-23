import os
import codecs
import pdb
import bs4
import tarfile
import shutil
import requests
import urllib
import urllib2
import cookielib
import json
from lxml.cssselect import CSSSelector
from lxml import html
from bs4 import BeautifulSoup
import sys
import json
from lxml import etree
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


result = codecs.open('./data/index.html','w+','utf-8')
result.seek(0)
result.truncate()

def generate_header():
    header = u'<!DOCTYPE html>\n'
    header += u'<html><head>\n'
    header += u'<meta charset="UTF-8">\n'
    header += u'<link rel="stylesheet" href="./static/bootstrap/css/bootstrap.min.css">\n'
    header += u'<link rel="stylesheet" href="./static/bootstrap/css/bootstrap-theme.min.css">\n'
    header += u'<link rel="stylesheet" href="./static/bootstrap/css/style.css">\n'
   

    header += u'<script src="./static/bootstrap/js/jquery.slim.min.js"></script>\n'
    header += u'<script src="./static/bootstrap/js/tether.min.js"></script>\n'
    header += u'<script src="./static/bootstrap/js/popper.min.js"></script>\n'
    header += u'<script src="./static/bootstrap/js/bootstrap.min.js"></script>\n'  
    header += u'<script src="./static/bootstrap/js/problems.js"></script>\n'     
    header += u'<script src="./static/bootstrap/js/MathJax.js?config=TeX-MML-AM_HTMLorMML-full"></script>'      
    header += u'</head><body>\n'
    header += u'<div class="container-fluid">\n'
    return header

def generate_footer():
    footer = u'</div></body></html>'
    return footer

def get_course_title(coursedir):
    for f in os.listdir('./data/' + coursedir +'/courseoriginal/course/'):
        if '.xml' in f:        
            root = etree.parse('./data/' + coursedir +'/courseoriginal/course/' + f)        
            attributes = root.getroot().attrib        
            title = 'Sin titulo'
            image = 'Sin imagen'
            if 'display_name' in attributes:
                title = attributes['display_name']
            if 'course_image' in attributes:
                image = './static/' + attributes['course_image']
                #move_file(attributes['course_image'])
    gentitle = '<div class="row">\n'
    gentitle += '<div class="col-md-2" style="background: url('+ coursedir +'/generated/' + image.replace('./static','static') + ') no-repeat;height:100px;background-size:200px;">'
    
    
    
    #gentitle +='<img src="'+ coursedir +'/generated/' + image.replace('./static','static') + '">'
    gentitle +='</div>\n'
    gentitle += '<div class="col-md-8">\n' + title
    gentitle +='</div>\n'
    gentitle += '<div class="col-md-2">\n<a href="'+ coursedir +'/generated/index.html" class="btn btn-info" role="button">Ir al curso</a>'
    gentitle +='</div>\n'
    gentitle +='</div>\n'

    return gentitle

def get_course_overview(coursedir):
    if os.path.exists('./data/' + coursedir +'/courseoriginal/about/overview.html'):
        result = codecs.open('./data/' + coursedir +'/courseoriginal/about/overview.html','r','utf-8').read()
        result = result.replace('/static/',coursedir +'/generated/static/')
        return result    
    else:
        return 'overview'

def generate_index(coursedir):
    gencourse = u'<div class="panel panel-default">\n' 
    gencourse += u'<div class="panel-heading">\n'
    gencourse += u'<a class="panel-title collapsed" data-toggle="collapse" data-parent="#panel-inicial" href="#'+ coursedir.replace('.','_') + '">' + get_course_title(coursedir) + '</a>\n'
    gencourse += u'</div>\n'
    gencourse += u'<div id="'+ coursedir.replace('.','_') +'" class="panel-collapse collapse">\n'
    gencourse += u'<div class="panel-body">\n'
    gencourse += get_course_overview(coursedir)
    gencourse += u'</div>\n'
    gencourse += u'</div>\n'
    gencourse += u'</div>\n'
    return gencourse
    #link = '<a href="'+coursedir+'/generated/index.html"> TITULO </a>'
    #return link

result.writelines(generate_header())
for f in sorted(os.listdir('./data/')):
    if f != 'index.html' and f != 'static' and f != '.DS_Store':
        result.writelines(generate_index(f))

result.writelines(generate_footer())        
result.close()