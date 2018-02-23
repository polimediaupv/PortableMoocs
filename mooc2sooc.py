import os
import codecs
import tarfile
import shutil
import requests
import json
from pytube import YouTube
from bs4 import BeautifulSoup
import sys
from lxml import etree
import argparse
reload(sys)
sys.setdefaultencoding('UTF8')

def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)

def get_video(video_id,args):    
    if not os.path.exists(args.dest + '/' + args.course+'/generated/static/videos/' + video_id + '/'):
        os.makedirs(args.dest + '/' + args.course+'/generated/static/videos/' + video_id + '/')
    if not os.path.exists(args.dest + '/' + args.course+'/generated/static/videos/' + video_id + '/' + args.ress + '.mp4'):
        yt = YouTube('http://youtube.com/watch?v=' + video_id)
        #could use a control when youtube doesnt have that resolution    
        if yt.streams.filter(res=args.ress,mime_type='video/mp4').first() != None:
            yt.streams.filter(res=args.ress,mime_type='video/mp4').first().download(args.dest + '/' + args.course+'/generated/static/videos/' + video_id ,args.ress)
        elif yt.streams.filter(mime_type='video/mp4').first() != None:
            print "No source find for video " + video_id + " at the desired ress of  " + args.ress + " downloading alternative instead."
            yt.streams.filter(mime_type='video/mp4').first().download(args.dest + '/' + args.course+'/generated/static/videos/' + video_id ,args.ress)
        else:
            print "No source find for video " + video_id

def move_file(filename,curso):
    shutil.copyfile(args.dest + '/' + curso +'/courseoriginal/static/'+filename,args.dest + '/' + curso +'/generated/static/'+filename)

def generate_header():
    header = u'<!DOCTYPE html>\n'
    header += u'<html><head>\n'
    header += u'<meta charset="UTF-8">\n'
    header += u'<link rel="stylesheet" href="../../static/bootstrap/css/bootstrap.min.css">\n'
    header += u'<link rel="stylesheet" href="../../static/bootstrap/css/bootstrap-theme.min.css">\n'
    header += u'<link rel="stylesheet" href="../../static/bootstrap/css/style.css">\n'
   

    header += u'<script src="../../static/bootstrap/js/jquery.slim.min.js"></script>\n'
    header += u'<script src="../../static/bootstrap/js/tether.min.js"></script>\n'
    header += u'<script src="../../static/bootstrap/js/popper.min.js"></script>\n'
    header += u'<script src="../../static/bootstrap/js/bootstrap.min.js"></script>\n'  
    header += u'<script src="../../static/bootstrap/js/problems.js"></script>\n'     
    header += u'<script src="../../static/bootstrap/js/MathJax.js?config=TeX-MML-AM_HTMLorMML-full"></script>'      
    header += u'</head><body>\n'
    header += u'<div class="container-fluid">\n'
    return header

def generate_title(title,image):
    gen_title = '<div class="row">\n' 
    gen_title += '<div class="col-md-12 cabecera" style="background-image: url('+ image +');">\n'
    gen_title += '<h1>\n' 
    gen_title += title 
    gen_title += '</h1>\n' 
    gen_title += '</div>\n'     
    gen_title += '</div>\n' 
    return gen_title

def generate_footer():
    footer = u'</div></body></html>'
    return footer

def get_chapter_title(chapter_url,args):
    root = etree.parse(args.dest + '/' + args.course +'/courseoriginal/chapter/' + chapter_url + '.xml').getroot()        
    attributes = root.attrib        
    if 'display_name' in attributes:
        print('Creating chapter: ' + attributes['display_name'])
        return attributes['display_name']
    else:
        return 'Sin titulo'

def generate_video(video_url,args):   
    print('Generating video:' + video_url)
    root = etree.parse(args.dest + '/' + args.course +'/courseoriginal/video/' + video_url + '.xml').getroot()        
    
    get_video(root.attrib['youtube_id_1_0'],args)
   
    video = u'<div class="row">\n<div class="col-md-12 video">\n<h4>'+ root.attrib['display_name'] +'</h4>\n'
    video += u'<video class="img-responsive"  width="70%" controls>\n'
    #src="./static/videos/' + root.attrib['youtube_id_1_0'] +  '.mp4"
    for f in os.listdir(args.dest + '/' + args.course+'/generated/static/videos/' + root.attrib['youtube_id_1_0']):
        if '.mp4' in f:
            video+='<source src="./static/videos/' + root.attrib['youtube_id_1_0'] + '/' + f + '" />'
    video += '</video>\n'
    video += u'</div>\n</div>\n'    
    return video

def generate_html(html_url,args):
    print('Generating html:' + html_url)    
    root = etree.parse(args.dest + '/' + args.course +'/courseoriginal/html/' + html_url + '.xml').getroot()            
    root_html = BeautifulSoup(codecs.open(args.dest + '/' + args.course +'/courseoriginal/html/' + html_url + '.html','r','utf-8').read(), "lxml")
    
    html_txt = u'<div class="row">\n<div class="col-md-12 html">\n' 
    if 'display_name' in root.attrib:
        html_txt += '<h4>'+ root.attrib['display_name'] +'</h4>\n'
    
    html_txt += root_html.prettify()
    html_txt += u'</div>\n</div>\n' 
    return html_txt 

def generate_problem(problem_url,args):
    print('Generating problem:' + problem_url)    
    root = etree.parse(args.dest + '/' + args.course +'/courseoriginal/problem/' + problem_url + '.xml').getroot()            
    problem=''
    if root.find('multiplechoiceresponse') != None:
        
        problem = u'<div class="row">\n<div class="col-md-12 problem">\n<h4>'+ root.attrib['display_name'] +'</h4>\n'
        problem += u'</div>\n</div>\n'
        problem += u'<div class="row">\n<div class="col-md-12 problem_enun">\n'        
        enun = ''
        
        if root.text != None:
            enun = root.text
        for child in root:
            if child.tag != 'multiplechoiceresponse' and child.attrib!={'class': 'resetcustom'}: 
                               
                enun += etree.tostring(child,pretty_print=True, xml_declaration=False, encoding='utf-8')

        problem += enun
        problem += u'</div>\n</div>\n'
        problem += u'<div class="row">\n<div class="col-md-12 problem_options">\n'
        problem+='<form id='+ problem_url +'>\n'
        txt_choice = ''
        for choice in root.find('multiplechoiceresponse').find('choicegroup').findall('choice'):            
            if choice.text != None:                
                txt_choice = choice.text
            for child in choice:
                if child.tag !='choicehint':                    
                    txt_choice += etree.tostring(child,pretty_print=True, xml_declaration=False, encoding='utf-8')          
            problem +='<input type="radio" name="choice" value="'+ choice.attrib['correct'] +'">  ' + txt_choice + '<br>'
            
        problem+='<p class="answer"></p>\n'
        problem+='</form>'
        problem+='<button onclick="submitAnswer('+ problem_url +')">Responder</button>'        
        problem += u'</div>\n</div>\n'    
    return problem

def get_vertical_content(vertical_url,args):
    print('Generating vertical:' + vertical_url)    
    vertical =''    
    root = etree.parse(args.dest + '/' + args.course +'/courseoriginal/vertical/' + vertical_url + '.xml').getroot()        
    if root.attrib['display_name'] != 'Final del curso': 
        vertical = u'<div class="row">\n<div class="col-md-12 vertical">\n<h3>'+ root.attrib['display_name'] +'</h3>\n'
        for child in root:
            if child.tag =='video':            
                vertical += generate_video(child.attrib['url_name'],args)
            if child.tag =='html':
                vertical += generate_html(child.attrib['url_name'],args)
            if child.tag =='problem':
                vertical += generate_problem(child.attrib['url_name'],args)
            
        vertical += u'</div>\n</div>\n'    
    return vertical 


def get_sequential_content(sequential_url,args):
    print('Generating sequential:' + sequential_url)    
    root = etree.parse(args.dest + '/' + args.course +'/courseoriginal/sequential/' + sequential_url + '.xml').getroot()        
    sequential = u'<div class="row">\n<div class="col-md-12 sequential">\n<h2>'+ root.attrib['display_name'] +'</h2>\n'
    verticals = root.findall('vertical')
    for vertical in verticals:
        sequential += u'<div class="row">\n<div class="col-md-12">'
        sequential += get_vertical_content(vertical.attrib['url_name'],args)
        sequential += u'</div>\n</div>\n'        
    sequential += u'</div>\n</div>\n'    
    return sequential    

def get_chapter_content(chapter_url,args):
    root = etree.parse(args.dest + '/' + args.course +'/courseoriginal/chapter/' + chapter_url + '.xml').getroot()        
    sequentials = root.findall('sequential')
    chaptercontent = '<div class="row">\n<div class="col-md-12 chapter">\n'
    for sequential in sequentials:
        chaptercontent += '<div class="row">\n<div class="col-md-12">\n'        
        chaptercontent += get_sequential_content(sequential.attrib['url_name'],args)
        chaptercontent += '</div>\n</div>\n'    
    chaptercontent += '</div>\n</div>\n'
    return chaptercontent


def generate_chapter(chapter,args): 
    genchapter=u''
    if get_chapter_title(chapter.attrib['url_name'],args) != u'Funcionamiento de la plataforma edX':
        genchapter = u'<div class="panel panel-default">\n' 
        genchapter += u'<div class="panel-heading">\n'
        genchapter += u'<a class="panel-title collapsed" data-toggle="collapse" data-parent="#panel-inicial" href="#C'+ chapter.attrib['url_name'].replace('.','_') + '">' + get_chapter_title(chapter.attrib['url_name'],args) + '</a>\n'
        genchapter += u'</div>\n'
        genchapter += u'<div id="C'+ chapter.attrib['url_name'].replace('.','_') +'" class="panel-collapse collapse">\n'
        genchapter += u'<div class="panel-body">\n'
        genchapter += get_chapter_content(chapter.attrib['url_name'],args)
        genchapter += u'</div>\n'
        genchapter += u'</div>\n'
        genchapter += u'</div>\n'
    return genchapter

def init(args):
    if not os.path.exists(args.dest):
        os.makedirs(args.dest)
    if not os.path.exists(args.dest + '/' + args.course +'/'):
        os.makedirs(args.dest + '/' + args.course +'/')
    if os.path.exists(args.dest + '/' + args.course +'/courseoriginal/'):
        shutil.rmtree(args.dest + '/' + args.course +'/courseoriginal/', ignore_errors=True)            
    tar_name=''
    if args.file == None:
        for f in os.listdir(args.dest + '/' + args.course +'/'):
            if '.tar.gz' in f:            
                tar_name = args.dest + '/' + args.course +'/' + f
    else:
        tar_name = args.file
    if tarfile != '':
        tar = tarfile.open(tar_name)
        tar.extractall()
        folder_name = tar.getnames()[0]
        tar.close()
        shutil.move(folder_name,args.dest + '/' + args.course +'/courseoriginal/')
        
    recursive_overwrite(args.dest + '/' + args.course +'/courseoriginal/static/',args.dest + '/' + args.course +'/generated/static/')
    if not os.path.exists(args.dest + '/' + args.course +'/generated/'):
        os.makedirs(args.dest + '/' + args.course +'/generated/')
    if not os.path.exists(args.dest + '/' + args.course +'/generated/static/'):
        os.makedirs(args.dest + '/' + args.course +'/generated/static/')
    if not os.path.exists(args.dest + '/' + args.course +'/generated/static/videos'):
        os.makedirs(args.dest + '/' + args.course +'/generated/static/videos')    
    if not os.path.exists(args.dest + '/' + 'static/'):        
        shutil.copytree('assets/static/',args.dest + '/' + 'static/')
   
    



def generate_portable(args):
    print("Starting generation of : " + args.course)
    init(args)        
    result = codecs.open(args.dest + '/' + args.course +'/generated/index.html','w+','utf-8')
    result.seek(0)
    result.truncate()
    result.writelines(generate_header())
    for f in os.listdir(args.dest + '/' + args.course +'/courseoriginal/course/'):
        if '.xml' in f:        
            root = etree.parse(args.dest + '/' + args.course +'/courseoriginal/course/' + f)        
            attributes = root.getroot().attrib        
            title = 'Sin titulo'
            image = 'Sin imagen'
            if 'display_name' in attributes:
                title = attributes['display_name']
            if 'course_image' in attributes:
                image = './static/' + attributes['course_image']
                move_file(attributes['course_image'],args.course)
            result.writelines(generate_title(title,image).replace('src="/static','src="./static')) #revisar
            chapters = root.getroot().findall('chapter')
            if len(chapters) >0:
                result.writelines(u'<div class="panel-group" id="panel-inicial">\n')
                for chapter in chapters:                
                    result.writelines(generate_chapter(chapter,args).replace('src="/static','src="./static')) #revisar
                result.writelines(u'</div>\n')
    result.writelines(generate_footer())        
    result.close()



parser = argparse.ArgumentParser(description='Portable Course generator')
parser.add_argument('--course', dest='course',default=None,help='the folder of the generated course, if --file not defined will search here for the tar.gz to uncompress. if course not defined will try to generate all the folders into dest param')
parser.add_argument('--file', dest='file',default=None,help='tar.gz file containing the original course, if not declared will search for a tar file into the course folder')
parser.add_argument('--dest', dest='dest',default='./data',help='a container folder where we will copy our assets and generate the course courses in same dest will share assets and will be capable of being indexed')
parser.add_argument('--ress', dest='ress',default='720p',help='video resolution that will be downloaded from youtube 1080p,720p,360p,240p if more than one is picked will be downloaded in all resolutions avaiable but this could increase the result size')


args = parser.parse_args()
if args.course!=None:    
    generate_portable(args)
else:    
    for f in os.listdir(args.dest):
        if f != 'static' and f != 'index.html' and f != '.DS_Store' :
            args.course = f
            generate_portable(args)