import thread
import itertools
import ctypes   
import time
#import LanSend
import pykinect
from pykinect import nui
from pykinect.nui import JointId
from math import sqrt
import pygame
from pygame.color import THECOLORS
from pygame.locals import *
past_pos=''
pdemor=''
pdemol=''
pdemo1=''
pdemo2=''
histl=[]
histr=[]

draw_letter=False
Flying = False
chara = []
KINECTEVENT = pygame.USEREVENT
DEPTH_WINSIZE = 640,480
VIDEO_WINSIZE = 640,480
skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image
ActionPerforming={'MoveForward':False,'MoveBackward':False,'MoveLeft':False,'MoveRight':False,'MoveDown':False,'MoveUp':False,'TurnRight':False,'TurnLeft':False,'Hover':False,'Reset':False,'Clear':False,'Just':False}
pygame.init()
SKELETON_COLORS = [THECOLORS["red"], 
                   THECOLORS["blue"], 
                   THECOLORS["green"], 
                   THECOLORS["orange"], 
                   THECOLORS["purple"], 
                   THECOLORS["yellow"], 
                   THECOLORS["violet"]]

LEFT_ARM = (
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft,
             
            )
RIGHT_ARM = (
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             )
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image
if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
    Py_ssize_t = ctypes.c_int
elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
    Py_ssize_t = ctypes.c_int64
else:
    raise TypeError("Cannot determine type of Py_ssize_t")

_PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
_PyObject_AsWriteBuffer.restype = ctypes.c_int
_PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
                                    ctypes.POINTER(ctypes.c_void_p),
                                    ctypes.POINTER(Py_ssize_t)]
def draw_skeleton_data(pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
        curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)

        pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next

def shapedef(pSkelt, index,SKEL_CORD):
    shapster=['|']  
    mindis_low=25
    for i in range(0,len(SKEL_CORD)-1):
        start = pSkelt.SkeletonPositions[SKEL_CORD[i]]
        next =pSkelt.SkeletonPositions[SKEL_CORD[i+1]]
        curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h)
        curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)
        if((curstart[0]<curend[0]) and (curstart[1] >= curend[1])):
               shapster.append('ru')
        elif((curstart[0]>curend[0]) and (curstart[1] >= curend[1])):
               shapster.append('lu')
              
        elif((curstart[0]>curend[0]) and (curstart[1] < curend[1])):
                shapster.append('ld')
        elif((curstart[0]<curend[0]) and (curstart[1] < curend[1])):
                shapster.append('rd')
    

        #pygame.draw.line(screen, SKELETON_COLORS[index], curstart,     curend, width)
        start = next
    return shapster

    ''' born_len = sqrt(((SKEL_CORD[i+3]-SKEL_CORD[i+1]) **2)-((SKEL_CORD[i+2]-SKEL_CORD[i])**2))
       if SKEL_CORD:
       for i in range(0,len(SKEL_CORD-4,2):
            born_len = sqrt(((SKEL_CORD[i+3]-SKEL_CORD[i+1]) **2)-((SKEL_CORD[i+2]-SKEL_CORD[i])**2))'''

            
        
def surface_to_array(surface):
   buffer_interface = surface.get_buffer()
   address = ctypes.c_void_p()
   size = Py_ssize_t()
   _PyObject_AsWriteBuffer(buffer_interface,
                          ctypes.byref(address), ctypes.byref(size))
   bytes = (ctypes.c_byte * size.value).from_address(address.value)
   bytes.object = buffer_interface
   return bytes
def screen_draw(stri,x,y):
    font = pygame.font.SysFont("comicsansms", 44)
    text = font.render(str(stri), True, (0, 0, 0))
    try:screen.blit(text,(x - text.get_width() // 2, y- text.get_height() // 2))
    except:pass
def find_len_slop(p1,p2):
    born_len = sqrt(((p2[1]-p1[1]) **2)-((p2[0]-p1[0])**2)) 
    slp = ((p2[1]-p1[1])/(p2[0]-p1[0]))
    return born_len,slp
def convert_gest(stri):
    curen=""
    if len(stri)>1:
        for x in stri:
            if x == '|':
                curen=""
            else:
                curen=curen+x
    return curen


def draw_skeletons(skeletons):
    global draw_letter,chara,Flying,ActionPerforming,drn
    isTracked=False
    finleng =40
    global past_pos,pdemor,pdemol,pdemo2,pdemo1
  
    for index, data in enumerate(skeletons):
                    if data.eTrackingState == nui.SkeletonTrackingState.TRACKED and not(isTracked):
                        isTracked=True
                        ElbowPos=skeleton_to_depth_image(data.SkeletonPositions[JointId.WristLeft], dispInfo.current_w, dispInfo.current_h) 
                        HandPos=skeleton_to_depth_image(data.SkeletonPositions[JointId.WristRight], dispInfo.current_w, dispInfo.current_h) 
                         
                        if HandPos[0]==0.0:
                            break
                         

                        try:
                            leng,slp=find_len_slop((int( ElbowPos[0]), int( ElbowPos[1])),(int( HandPos[0]), int( HandPos[1])))
                        except:
                               pass
                       
                        
                        
                           #move to module
                        shapL,shapR=convert_gest(shapedef(data, index,LEFT_ARM)),convert_gest(shapedef(data, index,RIGHT_ARM))
                        push_history(shapR,shapL)

                        
                        screen_draw("X",ElbowPos[0],ElbowPos[1])
                        screen_draw("Y",HandPos[0],HandPos[1]) 
                        #screen_draw(pdemol,ElbowPos[0],ElbowPos[1]+20)
                        #screen_draw(pdemor,HandPos[0],HandPos[1]+20)
                        #finlen =(born_len/finleng) *finleng
                        #if shapR==demor:
                        LastAction=0
                        handr=skeleton_to_depth_image(data.SkeletonPositions[JointId.WristRight], dispInfo.current_w, dispInfo.current_h) 
                        handl=skeleton_to_depth_image(data.SkeletonPositions[JointId.WristLeft], dispInfo.current_w, dispInfo.current_h)
                        sholder=skeleton_to_depth_image(data.SkeletonPositions[JointId.ShoulderCenter], dispInfo.current_w, dispInfo.current_h)
                        head=skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h)
                        hip=skeleton_to_depth_image(data.SkeletonPositions[JointId.HipCenter], dispInfo.current_w, dispInfo.current_h)
                        if not(Flying):
                            if handr[1]<head[1] and  ActionPerforming['Just']==False:
                                   
                                    drn.takeoff()
                                    ActionPerforming['Just']= True
                                    Flying = True
                         #++++++++++++++++++++++++++++++++++++++++++++++The Remote , Need to impliment based on Continues Gestures than stattic one++++++++++++++          
                        else:
                            if (handr[1]>hip[1]) and ActionPerforming['Just']==False :
                                drn.land()
                                
                                Flying = False
                                ActionPerforming['Just']=False
                            '''elif (shapL=='ldld')and (pdemol=='lulu')  :
                                LanSend.send_dron(" ")
                                Flying = False'''
                            '''if (shapR=='rdrd')and (shapL=='ldrd')  :
                                LanSend.send_dron("hr")
                                Flying = False'''
                                                   
                            if (handr[1]<sholder[1] and handl[1]<sholder)  and ActionPerforming['MoveForward']==False:
                                drn.move_forward()
                                ActionPerforming['MoveForward']=True

                                resetflag('MoveForward')
                           
                            if (handr[1]<sholder[1]) and (handl[1]>sholder[1]) and ActionPerforming['MoveUp']==False:
                                drn.move_up()
                                drn.move_up()
                                ActionPerforming['MoveUp']=True
                                resetflag('MoveUp')
                            if (handr[0]<handl[0])  and ActionPerforming['Hover']==False:
                                drn.hover()
                                ActionPerforming['Hover']=True
                                resetflag('Hover')
                            '''if (shapR=='ldld') and (shapL=='rdrd') and ActionPerforming['Reset']==False:
                                 drn.reset()
                                 print "send Reset"
                                 resetflag('Reset')'''
                            

def resetflag(ind):
    global ActionPerforming

    for xx in ActionPerforming:
        ActionPerforming[xx]=False
        
    if len(ind)>3:
        ActionPerforming[ind]=True

        

     

def depth_frame_ready(frame):
    if video_display:
        return

    with screen_lock:
        address = surface_to_array(screen)
        frame.image.copy_bits(address)
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()    

def depth_frame_ready(frame):
    if video_display:
        return

    with screen_lock:
        address = surface_to_array(screen)
        frame.image.copy_bits(address)
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()    


def video_frame_ready(frame):
    if not video_display:
        return

    with screen_lock:
        address = surface_to_array(screen)
        frame.image.copy_bits(address)
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()



 
def push_history(right,left):
    global pdemor,pdemol,histl,histr
    if len(histl)<1:
        histl.insert(0,left)
        histr.insert(0,right)
        pdemor = right
        pdemol = left
    else:
        if (histl[len(histl)-1]!= left):
            histl.insert(len(histl),left) 
            pdemol=histl[len(histl)-2]
            print pdemor
        if (histr[len(histr)-1]!= right):
            histr.insert(len(histr),right) 
            pdemor=histr[len(histr)-2]
        
        if len(histl)>3:
            histr=histr[len(histr)-3:len(histr):1]
            histl=histl[len(histl)-3:len(histl):1]



if __name__ == '__main__':
        import libardrone
        drn=libardrone.ARDrone()

        full_screen = False
        draw_skeleton = True
        video_display = False

        screen_lock = thread.allocate()
        screen = pygame.display.set_mode(DEPTH_WINSIZE,0,16)    
        pygame.display.set_caption('Mirror Ver.K')
        Flight_mode=False
        Malayalam_mode=True

        skeletons = None
        #screen.fill(THECOLORS["black"])
        kinect = nui.Runtime()
        kinect.skeleton_engine.enabled = True
        
 
        def post_frame(frame):
            try:
                   pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
            except:
                # event queue full       
        
                pass
        kinect.skeleton_frame_ready+=  post_frame
    
        kinect.depth_frame_ready += depth_frame_ready    
        kinect.video_frame_ready += video_frame_ready  
        kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
        kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Depth)
        
        done = False

       
        while not done:
            
            e = pygame.event.wait()
            dispInfo = pygame.display.Info()

            if e.type == pygame.QUIT:
                done = True
                break
            elif e.type == KINECTEVENT:
                skeletons = e.skeletons
                if draw_skeleton:
                    
                    draw_skeletons(skeletons)

                    pygame.display.update()
            elif e.type == pygame.KEYUP:
                drn.hover()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    done = True
                    break
                elif e.key == pygame.K_RETURN:
                        drn.takeoff()
                elif e.key == pygame.K_SPACE:
                    print "keyboard land"
                    drn.land()
                    
                # emergency
                elif e.key == pygame.K_BACKSPACE:
                    print "keyboard reset"
                    drn.reset()
                # forward / backward
                elif e.key == pygame.K_t:
                    drn.trim()
                elif e.key == pygame.K_h:
                    drn.hover()
                elif e.key == pygame.K_w:
                    drn.move_forward()
                elif e.key == pygame.K_u:
                    arm =True
                elif e.key == pygame.K_s:
                    drn.move_backward()
                # left / right
                elif e.key == pygame.K_y:
                    drn.hover()
                elif e.key == pygame.K_a:
                    drn.move_left()
                elif e.key == pygame.K_d:
                    drn.move_right()
                # up / down
                elif e.key == pygame.K_UP:
                    drn.move_up()
                elif e.key == pygame.K_DOWN:
                    drn.move_down()
                # turn left / turn right
                elif e.key == pygame.K_LEFT:
                    drn.turn_left()
                elif e.key == pygame.K_RIGHT:
                    drn.turn_right()
                # speed
                elif e.key == pygame.K_1:
                    drn.speed = 0.1
                elif e.key == pygame.K_2:
                    drn.speed = 0.2
                elif e.key == pygame.K_3:
                    drn.speed = 0.3
                elif e.key == pygame.K_4:
                    drn.speed = 0.4
                elif e.key == pygame.K_5:
                    drn.speed = 0.5
                elif e.key == pygame.K_6:
                    drn.speed = 0.6
                elif e.key == pygame.K_7:
                    drn.speed = 0.7
                elif e.key == pygame.K_8:
                    drn.speed = 0.8
                elif e.key == pygame.K_9:
                    drn.speed = 0.9
                elif e.key == pygame.K_0:
                    drn.speed = 1.0