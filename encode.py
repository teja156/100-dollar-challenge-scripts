# This script is used to encode the message into the video
from hashlib import new
import cv2
import os
from stegano import lsb
from subprocess import call,STDOUT
import sys
import numpy

FRAMES = [156,267,78,1100,321]
MAIN_VIDEO = sys.argv[1]
temp_folder = "tmp"

TEXT_TO_ENCODE = "MI4NLO+eBjkp67OyUvBeVPWc+gAwHNJwSkfkfqVaSeyj1LlKUGffUah27n7iesmQ/AD1DOd2yJ80HLVh09Fglve63Oh7LDXUEUpxJGULxWhx0caVI+BpdJL9lEgDyPkHOVw0k6Q38e7mAoltD2tnZcduEJx1jH+P/q5s8lKhiW9O1feyAfoJZedRv67As6/x26mXVCujVkG5CM0bk83vYQ=="
TEXT_MAPPED_TO_FRAMES = dict()


# def extractAudio():
#     call(["ffmpeg", "-i","main1.mp4" , "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

def countFrames():
    cap = cv2.VideoCapture(MAIN_VIDEO)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return length


def PILtoOpenCV(pil_image):
    open_cv_image = numpy.array(pil_image)[:, :, ::-1]
    return open_cv_image

def addAudio():
    # Add audio to the clip
    # ffmpeg -i tmp/encoded.mp4 -i .\main1.mp4 -c copy -map 0:0 -map 1:1 -shortest out.mp4
    print("Adding audio now")
    call(["ffmpeg", "-i","tmp/encoded_no_audio.avi" , "-i",MAIN_VIDEO,"-c","copy","-map","0:0","-map","1:1","-shortest","encoded_with_audio.avi"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    print("Done adding audio")


def prepare():
    global TEXT_MAPPED_TO_FRAMES
    global TEXT_TO_ENCODE
    # Prepare the parts of text to be encoded in respective frames
    st=0
    end=45 # encode 45 chars in each frame
    length  = len(TEXT_TO_ENCODE)
    for fn in FRAMES:
        txt = TEXT_TO_ENCODE[st:end]
        TEXT_MAPPED_TO_FRAMES[fn] = txt
        print(f"[INFO] Frame {fn} has {txt}")
        st = end
        end = st + 45
        if end>length:
            end = length


def encodeVideo(number_of_frames):
    cap = cv2.VideoCapture(MAIN_VIDEO)
    fourcc = cv2.VideoWriter_fourcc(*'HFYU')
    out = cv2.VideoWriter(os.path.join(temp_folder,'encoded_no_audio.avi'),fourcc, 24.0, (1920,1080))
    frame_number = -1
    while(frame_number<=number_of_frames):
        frame_number += 1
        frame_file_name = os.path.join(temp_folder,f"{frame_number}.png")
        encoded_frame_file_name = os.path.join(temp_folder,f"{frame_number}-enc.png")
        # print(f"Frame number {frame_number}")
        ret, frame = cap.read()

        if frame_number in FRAMES:
            txt_to_encode = TEXT_MAPPED_TO_FRAMES[frame_number]
            cv2.imwrite(frame_file_name,frame)
            # Using stegano, comment out below line to use imghide
            encoded_image = lsb.hide(frame_file_name,txt_to_encode)

            new_img = PILtoOpenCV(encoded_image)
            cv2.imwrite(encoded_frame_file_name,new_img)
            new_frame = new_img
            frame = new_frame
            print(f"[INFO] Written {txt_to_encode} to frame {frame_number}")

        out.write(frame)
        try:
            # just a preview while rendering
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',gray)
        except:
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


frames = countFrames()
prepare()
encodeVideo(frames)
addAudio()

