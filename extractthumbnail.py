from moviepy.editor import *
  
   
# loading video dsa gfg intro video
clip = VideoFileClip("/home/user/Desktop/dev/MoviePyPractise/final.mp4")
   
# getting only first 5 seconds
clip = clip.subclip(0, 5)
  
# saving a frame at 2 second
clip.save_frame("frame.png", t = 2)
  
# showing  clip
# clip.ipython_display(width = 360)