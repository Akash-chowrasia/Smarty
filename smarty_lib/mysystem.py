from datetime import *
import urllib.parse
from time import sleep
import urllib.request
import webbrowser
import re
import os
import requests
import sys
sys.path.append('/libs/')
import libs
from multiprocessing import Lock
from libs.SpawnProcesses import MyProcess
from libs.ParseUrl import ParseUrl
from libs.TaskQueue import generate_queue
from libs.ProgressBar import ProgressBar
from libs.ColorPython import Color
class PdfDownloader:
    def __init__(self, url, name):
        self.url = url
        self.dump_dir = '.' + name
        self.chunk_size = 64 * 1024         # Write these bytes at a time
        self.content_length = ParseUrl(url).extract_info()['content-length']
        try:
            os.mkdir(self.dump_dir)
            self.que = generate_queue(2*1024*1024, self.content_length, None)
        except FileExistsError:
            offsets = self.fix_already_downloaded()
            self.que = generate_queue(2*1024*1024, self.content_length, offsets)
        self.lock=Lock()
        self.processes = []
        for i in range(3):
            t = MyProcess(name = "Process-" + str(i), handler=self.handler)
            t.start()
            self.processes.append(t)
        for process in self.processes:
            process.join()
        with open(name, "wb") as f:
            for file in sorted(map(int, os.listdir(self.dump_dir))):
                with open(self.dump_dir + f'/{file}', 'rb') as r:
                    f.write(r.read())
    def handler(self, name):
        while True:
            while not self.que.empty():
                self.lock.acquire()
                item = self.que.get(block = False)
                self.lock.release()
                print(f"[THREAD] {name}: popped {item} from QUEUE")
                self.worker(item)
            else:
                return
    def worker(self, item):
        response = requests.get(self.url, stream=True, headers = item[-1])
        with open(f"{self.dump_dir}/{item[0]}", 'ab') as f:
            for data in response.iter_content(chunk_size = self.chunk_size):
                try:
                    pass
                except KeyboardInterrupt:
                    pass
                finally:
                    f.write(data)
    def fix_already_downloaded(self):
        d = dict()
        for file in os.listdir(self.dump_dir):
            d[int(file)] = os.path.getsize(f'{self.dump_dir}/{file}')
        return d

def time():
    time = datetime.now()
    print( Color.bold['purple'] + "The current time is: " + Color.reset ,time.hour,":",time.minute,":",time.second)
def date():
    date=datetime.now()
    print( Color.bold['purple'] +"Today's date is: " + Color.reset,date.day,"/",date.month,"/",date.year)
def showcal(l):
    temp="cal"
    for i in l:
        if type(i)==type(temp):
            p=i.lower()
        else:
            p=i
        temp+=" "+str(p)
    os.system(temp)
def status():
    os.system('neofetch --ascii_distro arch')
def clear():
    os.system('clear')
def delay(a):
    sleep(a)
def shut_down():
    os.system('poweroff')
def restart():
    os.system('reboot')
def path(l):
    k=str(l[0])
    if k == 'CURRENT':
        os.system('pwd')
    if k == 'SYSTEM':
        os.system('echo $PATH')

def youtube(search):
    new=2
    query_string = urllib.parse.urlencode({"search_query" : {search}})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    play="http://www.youtube.com/watch?v=" + search_results[0]
    webbrowser.open(play,new=new)

def searching(search):
    l=os.listdir()
    temp=[]
    if search in l:
        return True
    for i in l:
        if os.path.isdir(i) == True:
            temp.append(i)
    if len(temp)==0:
        return False
    origindir=os.getcwd()
    for i in temp:
        os.chdir(i)
        t=searching(search)
        if t==True:
            return t
        os.chdir(origindir)
    else:
        return False

def searchfile(search):
    temp1=[]
    os.chdir(os.path.join(os.environ['HOME']))
    list=os.listdir()
    if search in list:
        return True
    for i in list:
        if os.path.isdir(i) == True:
            temp1.append(i)
    if len(temp1)==0:
        return False
    originaldir=os.getcwd()
    for i in temp1:
        os.chdir(i)
        result=searching(search)
        if result == True:
            return True
        os.chdir(originaldir)
    else:
        return False
def google(a):
    new=2
    taburl=taburl="http://google.com/?#q="
    webbrowser.open(taburl+a,new)

def  move_to_smartymusics():
    os.chdir(os.path.join(os.environ['HOME']))
    os.chdir('Workspace')
    os.chdir('python')
    os.chdir('projects')
    os.chdir('smartymusics')

def video_downloader(a):
    new=2
    query_string = urllib.parse.urlencode({"search_query" : {a}})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    play="http://www.youtube.com/watch?v=" + search_results[0]
    os.system("youtube-dl %s"%play)

def downloader(item):
    temp=item[0]
    t1=os.getcwd()
    move_to_smartymusics()
    if temp=='VIDEOS' or temp=='VIDEO':
        a=input( Color.bold['green'] + "Enter video name to download:" + Color.reset)
        os.chdir("videos")
        try:
            video_downloader(a)
        except:
            print( Color.bold['red'] + "Ooops......?\n.....Network is not connected" + Color.reset)
        os.chdir(t1)
        print( Color.bold['yellow'] + '..... downloading completed......' + Color.reset)
    elif temp=='PDF' or temp=='EBOOK' or temp=='E-BOOK':
        a=input( Color.bold['green'] + "Enter URL of E-BOOK:" + Color.reset)
        name=input( Color.bold['purple'] + "What name should be given to the E-BOOK:" + Color.reset)
        os.chdir("ebooks")
        try:
            p=PdfDownloader(a,name)
            print( Color.bold['yellow'] + '..... downloading completed......' + Color.reset)
        except:
            print( Color.bold['red'] + "Ooops.....?\n......Network is not connected" + Color.reset)
        os.chdir(t1)

def listsongs(song):
    t1=os.getcwd()
    temp=song[0]
    move_to_smartymusics()
    t=""
    if temp == 'VIDEOS' or temp=='VIDEO':
        os.chdir('videos')
        l=os.listdir()
        t="video's"
    elif temp == 'MUSICS' or temp=='MUSIC':
        os.chdir('musics')
        l=os.listdir()
        t="music's"
    elif temp == 'LOGS' or temp=='LOG':
        os.chdir('/home/akash/Videos/Webcam/')
        l=os.listdir()
        t="video log's "
    elif temp=='PDF' or temp=='PDFS' or temp=='EBOOKS' or temp=='E-BOOKS':
        os.chdir('ebooks')
        l=os.listdir()
        t="e-book's"
    elif temp=='PHOTO' or temp=='PHOTOS' or temp=='GALLERY' or temp=='PICS' or temp=='PICTURES':
        print( Color.bold['green'] + "We have four sets of gallery:........" + Color.reset)
        print( Color.bold['yellow'] + "1).....Downloaded pics.." + Color.reset)
        print( Color.bold['white'] + "2).....Personal pics.." + Color.reset)
        print( Color.bold['yellow'] + "3).....Screenshots.." + Color.reset)
        print( Color.bold['white'] + "4).....Webcam pic.." + Color.reset)
        a=int(input( Color.bold['cyan'] + "Which Gallery have to list:" + Color.reset))
        if a==1:
            os.chdir('/home/akash/Downloads/')
            l1=os.listdir()
            l=[]
            for i in l1:
                if i.endswith('.jpg') or i.endswith('.png') or i.endswith('.gif'):
                    l.append(i)
            t="picture's"
        elif a==2:
            os.chdir('/home/akash/Workspace/python/projects/smartymusics/pics/')
            l=os.listdir()
            t="pic's"
        elif a==3:
            os.chdir('/home/akash/Pictures/')
            l1=os.listdir()
            l=[]
            for i in l1:
                if i.endswith('.jpg') or i.endswith('.png'):
                    l.append(i)
            t="picture's"
        elif a==4:
            os.chdir('/home/akash/Pictures/Webcam/')
            l=os.listdir()
            t="picture's"
    if len(l) == 0:
        os.chdir(t1)
        print( Color.bold['red'] + "we don't have list  ....." + Color.reset)
    else:
        print( Color.bold['cyan'] +"***we have %s with us are...***"%t + Color.reset)
        for i in range(len(l)):
            print(i+1,end="     ")
            if i%2 == 0:
                print( Color.bold['purple'] + l[i] + Color.reset)
            else:
                print( Color.bold['yellow'] + l[i] + Color.reset)
        os.chdir(t1)

def playsongs(song):
    temp=song[0]
    t1=os.getcwd()
    move_to_smartymusics()
    if temp == 'VIDEOS' or temp=='VIDEO':
        a=input( Color.bold['green'] + "Enter the video to play:" + Color.reset)
        os.chdir('videos')
        l=os.listdir()
        if a in l:
            os.system("vlc %s"%a)
            clear()
        else:
            result=searchfile(a)
            if result:
                os.system("vlc %s"%a)
                os.chdir(t1)
                clear()
            else:
                try:
                    os.chdir(t1)
                    youtube(a)
                    clear()
                except:
                        print( Color.bold['red'] + "Ooops...?\n............Network is not connected" + Color.reset)

    elif temp=='MUSICS' or temp=='MUSIC':
        a=input( Color.bold['green'] + "Enter the Music to play:" + Color.reset)
        os.chdir('musics')
        l=os.listdir()
        if a in l:
            os.system("play %s"%a)
            os.chdir(t1)
            clear()
        else:
            result=searchfile(a)
            if result:
                os.system("play %s"%a)
                os.chdir(t1)
                clear()
            else:
                os.chdir(t1)
                print(Color.bold['red'] + "Music not found" + Color.reset)
    elif temp=='LOGS' or temp=='LOG':
        a=input(Color.bold['green'] + "Enter the log to play:" + Color.reset )
        os.chdir('/home/akash/Videos/Webcam/')
        l=os.listdir()
        if a in l:
            os.system("vlc %s"%a)
            clear()
        else:
            print( Color.bold['red'] + "the log is not found" + Color.reset)

def createfile():
    t1=os.getcwd()
    try:
        for i in range(3):
            name=input( Color.bold['green'] + "Enter name of the file:" +  Color.reset)
            result=searchfile(name)
            if result:
                print( Color.bold['purple'] + "An file with this name is already existing....\n.........Try another name" + Color.reset)
            else:
                move_to_smartymusics()
                os.chdir("programs")
                os.system("vim %s"%name)
                break
        os.chdir(t1)
    except:
        pass
    os.chdir(t1)
def runfile():
    t1=os.getcwd()
    name=input( Color.bold['green'] + "enter name of file to run:" + Color.reset)
    base,ext=os.path.splitext(name)
    result=searchfile(name)
    if result:
        if ext=='.py':
            os.system("python %s"%name)
        elif ext=='.html':
            os.system("firefox %s"%name)
        elif ext=='.cpp' or ext=='.cxx':
            os.system("g++ -o %s %s"%(base,name))
            os.system("./%s"%base)
    else:
        print( Color.bold['red'] + "File not exist....." + Color.reset)

def openfile(file):
    temp=file[0]
    t1=os.getcwd()
    if temp=='CAMERA' or temp=='CAMRECODER' or temp=='CAM' or temp=='VIDEO' or temp=='WEBCAM' or temp=='LOG':
        os.system('cheese -f')
        os.chdir('/home/akash/Videos/Webcam/')
        l=os.listdir()
        temp1=[]
        try:
            for i in l:
                if i.endswith('.webm'):
                    for j in l:
                        if j!=i:
                            temp1.append(j)
                    a=max(temp1)
                    os.rename(str(i),str(int(a[0])+1)+'log.avi')
                    break
        except:
            pass
        clear()
        return
    if temp=='PHOTO' or temp=='PHOTOS' or temp=='GALLERY' or temp=='PICS' or temp=='PICTURES':
        print( Color.bold['green'] + "We have four sets of gallery:........" + Color.reset)
        print( Color.bold['yellow'] + "1).....Downloaded pics.." + Color.reset)
        print( Color.bold['white'] + "2).....Personal pics.." + Color.reset)
        print( Color.bold['yellow'] + "3).....Screenshots.." + Color.reset)
        print( Color.bold['white'] + "4).....Webcam pic.." + Color.reset)
        a=int(input( Color.bold['cyan'] + "Which Gallery have to list:" + Color.reset))
        if a==1:
            os.chdir('/home/akash/Downloads/')
            l1=os.listdir()
            for i in l1:
                if i.endswith('.jpg') or i.endswith('.png') or i.endswith('.gif'):
                    os.system('nomacs %s -f'%i)
                    break
        elif a==2:
            os.chdir('/home/akash/Workspace/python/projects/smartymusics/pics/')
            l=os.listdir()
            os.system('nomacs %s -f'%l[0])
        elif a==3:
            os.chdir('/home/akash/Pictures/')
            l1=os.listdir()
            print(l1)
            for i in l1:
                if i.endswith('.png'):
                    print(i)
                    os.system('nomacs %s -f'%i)
                    break
        elif a==4:
            os.chdir('/home/akash/Pictures/Webcam/')
            l=os.listdir()
            os.system('nomacs %s -f'%l[0])
        clear()
        return
    move_to_smartymusics()
    a=input(Color.bold['green'] + "Enter file name:" + Color.reset)
    base,ext=os.path.splitext(a)
    if ext =='.pdf':
        os.chdir("ebooks")
        l=os.listdir()
        if a in l:
            os.system("evince %s"%a)
            os.chdir(t1)
            clear()
        else:
            result=searchfile(a)
            if result:
                os.system("evince %s"%a)
                os.chdir(t1)
                clear()
            else:
                os.chdir(t1)
                print( Color.bold['red'] + "........%s is not found"%a + Color.reset)
    elif ext=='.py' or ext=='.cpp' or ext=='.c' or ext=='.txt':
        os.chdir("programs")
        l=os.listdir()
        if a in l:
            os.system("vim %s"%a)
            os.chdir(t1)
        else:
            result=searchfile(a)
            if result:
                os.system("vim %s"%a)
                os.chdir(t1)
            else:
                os.chdir(t1)
                print( Color.bold['red'] + "%s not found"%a + Color.reset)

commands1={'CONFIG':status,'CONFIGURE':status,'CONFIGURATION':status,'RUN':runfile,'EXECUTE':runfile,'CREATE':createfile,'MAKE':createfile,'DATE':date,'TIME':time,'STATUS':status,'POWEROFF':shut_down,'SHUT':shut_down,'OFF':shut_down,'TURNOFF':shut_down,'RESTART':restart,'REBOOT':restart}
commands2={'CALENDAR':showcal,'CAL':showcal,'PATH':path,'LIST':listsongs,'PLAYLIST':listsongs,'PLAY':playsongs,'OPEN':openfile,'DOWNLOAD':downloader}
