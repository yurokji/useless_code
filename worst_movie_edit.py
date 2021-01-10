#!/usr/bin/env python3
# Tite: Worst of the Worst Video Editor
# Download: https://github.com/yurokji/useless_code

# I have implemented a couple of python scripts.
# to automatically find and collect all the audio intervals 
# each of which correspond to useless "so" words 
# dectected by the speech recognition module from my video.   
# Before going into,
# These python scripts have some requirements as below:

# 1. install Vosk speech recognition toolkit
# pip install vosk

# 2. download vosk model for specific language
# Here I used vosk-model-en-us-aspire-0.2

# 3. Extract the zip file and rename the folder as "model"
# Move "model" folder itself into this folder   

# 4. install moviepy
# pip install moviepy

# 5. Go edit your file!
# python worst_movie_edit.py original.mp4 --> orignal_edited.mp4 

# 6. Add some cool background audio
# python add_music.py original_edited.mp4 --> original_edited_music.mp4


from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import subprocess
import json
import random 
from moviepy.editor import *
import sys
import numpy as np 

# Load the input video file from the terminal
clip = VideoFileClip(sys.argv[1])
fps = clip.reader.fps

# recognize the speech from the input video file
sample_rate=16000
model = Model("model")
rec = KaldiRecognizer(model, sample_rate)
process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                            sys.argv[1],
                            '-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                            stdout=subprocess.PIPE)

# recognized results are stored in the json format
# convert them all into a list to check if a string found in a specific time interval is "so" 
# if yes, then further check if its confidence is above some threshold,# and time interval is long enough
# if all yes, then put such information in to time_list variable
time_list = []
start_sec = 0
end_sec = 0
while True:
    data = process.stdout.read(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        recElem = rec.Result()
        res = json.loads(recElem)
        if 'result' in res:
            for i in range(len(res['result'])):
                confidence = res['result'][i]['conf']
                start_sec = res['result'][i]['start']
                end_sec = res['result'][i]['end']
                word = res['result'][i]['word'].lower().strip()
                if word == "so":
                    print("confidence: ", confidence)
                    print("start_time: ", start_sec)
                    print("end_time", end_sec)
                    print("word: ", word)
                    if confidence > 0.8 and end_sec - start_sec  > 0.2:
                        time_list.append([start_sec, end_sec, word])

# using time list, begin editing
# 1. rendering text "so" for time intervals containing in the time_list  on the clip  
# with its count
# 2. also rendering saw meme image, applying some image transformation,
# such as resize, translation, rotations  

edited_clips = []
count_so = 0
word_to_print = "so: {:4d} times".format(count_so)
btxtClip = TextClip(word_to_print,color='yellow', bg_color='black', font="Ubuntu-B", fontsize=30)
btxtClip = btxtClip.set_position((600, 600))
for mtime in time_list:
    mt1 = mtime[0]
    mt2 = mtime[1]
    word = mtime[2]
    duration = mt2 - mt1
    count_so += 1
    word_to_print = "so: "+str(count_so) 
    meme_name = "./imgs/saw.png"
    minv = 0.4
    maxv = 0.7
    memeClip = ImageClip(meme_name)
    memeClip = memeClip.set_duration(duration)
    # resize
    f = minv + (maxv - minv) *random.random() 
    meme_width = memeClip.size[0]
    meme_height = memeClip.size[1]
    meme_width = int(f * meme_width)
    memeClip = memeClip.fx( vfx.resize, width=meme_width)
    meme_width = memeClip.size[0]
    meme_height = memeClip.size[1]
    # rotation
    img_center = (meme_width // 2, meme_height // 2)
    corner = random.randint(0,3)
    saw_degree = 90 * corner
    memeClip = memeClip.rotate(saw_degree, expand=False)
    emboss = 1
    if corner == 0:
        pos = random.randint(10, clip.w - 10)
        memeClip = memeClip.set_position((pos - img_center[0], clip.h - img_center[1] - 10 * emboss))
    elif corner == 1:
        pos = random.randint(10, clip.h - 10)
        memeClip = memeClip.set_position((clip.w - img_center[0] - 10* emboss , pos - img_center[1]))  
    elif corner == 2:
        pos = random.randint(10, clip.w - 10)
        memeClip = memeClip.set_position((pos - img_center[0] , - img_center[0] + 10* emboss ))  
    else:
        pos = random.randint(10, clip.h - 10)
        memeClip = memeClip.set_position((-img_center[0] + 10* emboss, pos  - img_center[1]))   

# composite all the layers (video, meme image, text) for a clip 
    word_to_print = "so: {:4d} times".format(count_so)
    btxtClip = TextClip(word_to_print,color='yellow', bg_color='black', font="Ubuntu-B", fontsize=30)
    btxtClip = btxtClip.set_position((600, 600))
    btxtClip = btxtClip.set_duration(duration)
    cvc = CompositeVideoClip([clip.subclip(mt1,mt2), memeClip, btxtClip])       
    edited_clips.append(cvc)
# concatenate all the composited clips together into one clip
print("count_so: ", count_so) 
edited_clips = np.array(edited_clips)
final_clip = concatenate_videoclips(edited_clips)
# write the final clip to a file
outfile = sys.argv[1].removesuffix(".mp4")
final_clip.write_videofile(outfile +"_edited.mp4")