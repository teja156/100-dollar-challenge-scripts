# This script is used to decode and decrypt the message from the encoded video

'''
Usage: 
python decode.py <path_to_encoded_video>

Example:
python decode.py video.avi
'''

from stegano import lsb
import cv2
import os
import sys
import aesutil

ENCODED_VIDEO = sys.argv[1]
temp_folder = "tmp2"
FRAMES = [156,267,78,1100,321]
decoded = {}
key = "92786491b4015404961822c6734475154ecd896215b35f3a3baf3f854b550d37"


# def test():
#     print(lsb.reveal("tmp/3-enc.png"))

def createTmp():
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

def countFrames():
    cap = cv2.VideoCapture(ENCODED_VIDEO)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return length




def decodeVideo(number_of_frames):
    # First get the frame
    cap = cv2.VideoCapture(ENCODED_VIDEO)
    frame_number = -1
    while(frame_number<=number_of_frames):
        frame_number += 1
        frame_file_name = os.path.join(temp_folder,f"{frame_number}.png")
        encoded_frame_file_name = os.path.join(temp_folder,f"{frame_number}-enc.png")
        # print(f"Frame number {frame_number}")
        ret, frame = cap.read()

        if frame_number in FRAMES:
            cv2.imwrite(encoded_frame_file_name,frame)
            # Try using stegano, comment below line to use imghide
            clear_message = lsb.reveal(encoded_frame_file_name)
            decoded[frame_number] = clear_message
            print(f"Frame {frame_number} DECODED: {clear_message}")


def arrangeAndDecrypt():
    res=""
    for fn in FRAMES:
        res = res + decoded[fn]
    print(f"Final string: {res}")
    msg = aesutil.decrypt(key=key,source=res)
    print(f"Decoded message: \n {msg}")



createTmp()
frames = countFrames()
decodeVideo(frames)
arrangeAndDecrypt()
