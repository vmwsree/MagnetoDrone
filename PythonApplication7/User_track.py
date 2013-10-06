import thread
import itertools
import ctypes
import time
import pykinect
from pykinect import nui
import CharRecg
#import LanSend
from pykinect.nui import JointId
from math import sqrt
import pygame
from pygame.color import THECOLORS
from pygame.locals import *
draw_letter=False
Show_Video = False
WriteMode = True
LineSize= 7
Color = (0,0,255)
tot=chara = []
paintlines=[]
KINECTEVENT = pygame.USEREVENT
DEPTH_WINSIZE = 640,480
VIDEO_WINSIZE = 640,480
skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image
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
            JointId.HandLeft, 
            )
RIGHT_ARM = (
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.HandRight, 
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
def draw_skeleton_data(pSkelton,positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
        curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)

        pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next

def shapedef(pSkelt,SKEL_CORD):
    shapster=['|']
    mindis_low=25
    start = pSkelt.SkeletonPositions[SKEL_CORD[0]]
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

def screen_draw(stri,x,y,width=18):
    font = pygame.font.SysFont("comicsansms", width)
    text = font.render(str(stri), True, (0, 128, 0))
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

def draw_everythingelse():
    global paintlines,Color,LineSize
    for lines in paintlines:
        if len(lines)==2:
            Color,LineSize=lines[0],lines[1]
        elif len(lines):
            for i in range(0,len(lines),2):
                try:pygame.draw.line(screen,Color,(lines[i],lines[i+1]),(lines[i+2],lines[i+3]),LineSize)
                except:
                    pass
    pygame.display.update()          


def draw_skeletons(skeletons):
    global WriteMode,LineSize,Color,paintlines
    global draw_letter,chara
    finleng =20
    past_pos=''
    demor=''
    Istrack = False
    demol=''
    screen.fill(THECOLORS["white"])
    for skelt in skeletons:
                    if skelt.eTrackingState == nui.SkeletonTrackingState.TRACKED and not(Istrack):
                        ElbowPos=skeleton_to_depth_image(skelt.SkeletonPositions[JointId.ElbowRight], dispInfo.current_w, dispInfo.current_h) 
                        HandPos=skeleton_to_depth_image(skelt.SkeletonPositions[JointId.HandRight], dispInfo.current_w, dispInfo.current_h) 
                        try:
                            leng,slp=find_len_slop((int( ElbowPos[0]), int( ElbowPos[1])),(int( HandPos[0]), int( HandPos[1])))
                            #screen_draw(leng,HandPos[0],HandPos[1])
                            #screen_draw(slp,HandPos[0],HandPos[1]++15) 
                            

                        except:
                               pass
                           #move to module
                        pygame.draw.circle(screen, SKELETON_COLORS[1], (int( HandPos[0]), int( HandPos[1])), 6, 0)
                        shapL,shapR=convert_gest(shapedef(skelt, LEFT_ARM)),convert_gest(shapedef(skelt,RIGHT_ARM))
                        Istrack=True
                        if shapR=='ldld' and shapL== 'ldld':
                             WriteMode=True
                        if shapR=='rdrd' and shapL== 'rdrd':

                             WriteMode=False
                        def drawframe(WriteMode):
                          
                            if WriteMode:
                                screen_draw("WritePad",400,50)
                                
                            else:
                               
                                screen_draw("Paint",400,50)
                                
                        drawframe(WriteMode)
                       
                        if WriteMode:

                            if past_pos=='':
                                    past_pos=shapL
                                    demor=shapR
                                    demoL=shapL
                                    #pygame.draw.circle(screen, SKELETON_COLORS[1], (int( HandPos[0]), int( HandPos[1])), 6, 0)
                            #finlen =(born_len/finleng) *finleng
                            '''if shapR!=demor:
                                print shapR
                            drawn=False
                            if shapR == 'rulu' and shapL!='luru' :
                                if shapL=='luru' and past_pos!=shapL:
                                    if past_pos=='ruru' or drawn:
                                        drawn=True
                                
                            if drawn:    
                                screen_draw("hello",HandPos[0],HandPos[1])        
                            #shapL,shapR=shapedf(data, index,LEFT_ARM),shapdef(data, index,RIGHT_ARM)'''
                            k=1
                            if(shapL=='ldrd'):
                                k=2
                                                            
                                draw_letter=True

                                #else:
                                #    draw_letter = False
                                if draw_letter and HandPos[0]!=0.0:
                                        #if (len(chara)==0):
                                        #    chara=chara+[ HandPos[0], HandPos[1]]
                                        #elif (CharRecg.ptptdist((chara[len(chara)-1],chara[len(chara)-2]),(HandPos[0],HandPos[1])))<10 :
                                        
                                        if len(chara)==0 :
                                            chara=chara+[ int(HandPos[0]), int(HandPos[1])]
                                        #elif (chara[len(chara)-2] != (int(HandPos[0]))) or ( chara[len(chara)-1]) != (int (HandPos[1])):
                                        elif (CharRecg.ptptdist((chara[len(chara)-1],chara[len(chara)-2]),((int (HandPos[0])),(int (HandPos[1]))))<700):
                                            chara=chara+[ int(HandPos[0]), int(HandPos[1])]
                                        if len(chara)>=4:
                                            for i in range(0,len(chara),2):

                                                try:pygame.draw.line(screen, (0, 0, 255),(chara[i],chara[i+1]), (chara[i+2],chara[i+3]),7)
                                                except:pass
                                        
                                        #screen_draw(CharRecg.code,ElbowPos[0],ElbowPos[1])
                            else:
                                    draw_letter=False
                                    if len(chara)>0:

                                        #LanSend.send_letter(chara)
                                        print chara
                                    chara=[]
                                    HandPos=[0.0,0.0]
                           
                            
                                
                        elif not(WriteMode):
                           
                           draw_everythingelse()
                           
                           if(shapL=='ldlu'):
                                pygame.draw.circle(screen, SKELETON_COLORS[1], (int( HandPos[0]), int( HandPos[1])), 6, 0)
                                pygame.draw.circle(screen, SKELETON_COLORS[1], (int( ElbowPos[0]), int( ElbowPos[1])), 6, 0)
                                draw_letter=True
                                if draw_letter and HandPos[0]!=0.0:
                                            
                                                chara=chara+[ HandPos[0], HandPos[1]]
                                                for i in range(0,len(chara)-4,2):
                                                    
                                                        try:pygame.draw.line(screen, (0, 0, 255),(chara[i],chara[i+1]), (chara[i+2],chara[i+3]),7)
                                                        
                                                        except:pass
                                else:
                                
                                    
                                    HandPos=[0.0,0.0]
                                    if len(chara)>0:
                                        paintlines.insert(len(paintlines),chara)
                                    chara=[]
                        else:draw_letter=False
                        
                                                
'''if past_pos=='':
                                past_pos=shapL
                                demor=shapR
                                demoL=shapL
                        #finlen =(born_len/finleng) *finleng
                            if shapR!=demor:
                                print shapR
                            drawn=False
                            if shapR == 'rulu' and shapL!='luru' :
                                if shapL=='luru' and past_pos!=shapL:
                                    if past_pos=='ruru' or drawn:
                                        drawn=True
                            if drawn:
                                screen_draw("hello",HandPos[0],HandPos[1])        '''
                            #shapL,shapR=shapedf(data, index,LEFT_ARM),shapdef(data, index,RIGHT_ARM)  
                           
                                                
                                    
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
    global Show_Video
    if not video_display :
        return
    with screen_lock:
        if Show_Video:
            address = surface_to_array(screen)
            frame.image.copy_bits(address)
            del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()


if __name__ == '__main__':
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
        with screen_lock:
                screen = pygame.display.set_mode(VIDEO_WINSIZE,0,32)    
                video_display = True
 
        def post_frame(frame):
            try:
                   
                   pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
            except:
                # event queue full
                pass
        kinect.skeleton_frame_ready += post_frame
    
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


            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    done = True
                    break