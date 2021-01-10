from moviepy.editor import *

videoclip = VideoFileClip(sys.argv[1])
bgm = AudioFileClip(sys.argv[2])
# lower the volume of the added audio clip
bgm.set_duration(videoclip.duration)
bgm = bgm.fx( afx.volumex, 0.3) 
final_audio = CompositeAudioClip([videoclip.audio, bgm])
final_clip = videoclip.set_audio(final_audio)
outfile = sys.argv[1].removesuffix(".mp4")+"_music.mp4"
final_clip.write_videofile(outfile)