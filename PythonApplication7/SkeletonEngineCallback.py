from pykinect import nui
import time
import thread
from pykinect.nui import JointId
with nui.Runtime() as kinect:
    screen_lock = thread.allocate()
    kinect.skeleton_engine.enabled=True
    def frame_ready(frame):
        skeltns = frame.SkeletonData
        for skelt in skeltns:
            if skelt.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                #for index,data in enumerate(skelt):
                #print skelt
                head_pos =skelt.SkeletonPositions[JointId.Head]
                print head_pos

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

def skelt_frame_ready(frame):
    for skelt in frame.SkeletonData:
            if skelt.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                print skelt
    