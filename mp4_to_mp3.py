from moviepy import VideoFileClip
video = VideoFileClip("C:\\Users\\PC\\AppData\\Roaming\\Wondershare\\Wondershare Filmora\\Output\\HTML Playlist\\HTML PLAYLIST-1.mp4")
video.audio.write_audiofile("output.mp3")
