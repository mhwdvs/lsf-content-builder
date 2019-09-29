# lsf-content-builder
Makes Youtube content from top videos posted to Livestreamfails.com

Pipeline:

  - Navigate to LSF via self-made API
  - Go through top posts of the day and download
    - Continue downloading until length >5 minutes
  - Use FFMPEG to stitch together, add fade in/out etc
  - Use CLI youtube uploader to automatically post
  
Note: Although somewhat 'constructive' content and is tolerated by YouTube, this definitely wouldn't hold up as fair use in court. Do not use this to create monetised videos.

This is a proof-of-concept, and could be adapted to create datasets for AI to detect 'poor' content on YouTube
