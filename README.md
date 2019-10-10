# lsf-content-builder
Makes a compilation video from top videos posted to Livestreamfails.com

Pipeline:

  - Navigate LSF to farm top clips of the day and extract mp4 links
  - curl download all links extracted
  - Use FFMPEG to preprocess files (resolution, frame rate, etc) 
  - Overlay the streamers name over the clip
  - Use FFMPEG + FFPROBE to add fade in/out to each clip downloaded
  - Use FFMPEG to concat all the clips together
  - Use thumbnail of top clip as thumbnail of compilation
  - Use CLI youtube uploader to automatically post
  
