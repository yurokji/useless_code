from moviepy.editor import *
import moviepy
import sys

final_video_name = "movs/"+sys.argv[2]
total_edited_clips = []
for i in range(17):
    print(i)
    edited_video_name = "movs/"+sys.argv[1]+"{:04d}.mp4".format(i)
    clip = VideoFileClip(edited_video_name)
    total_edited_clips.append(clip)

final_clip = concatenate_videoclips(total_edited_clips)
final_clip.write_videofile(final_video_name)
