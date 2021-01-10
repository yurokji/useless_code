import os 
import sys

os.system("ffmpeg -i "+ sys.argv[2] + " -c copy -map 0 -f segment -segment_time " + sys.argv[1] + " -reset_timestamps 1 -segment_format_options movflags=+faststart  ./movs/" + sys.argv[3]+ "%04d.mp4")