#movie=Raspberry-814028145.mp4
#movie=Pi_1998_720p_trailer.mp4
movie=earth.mp4
#movie=ff.mp4

ffmpeg -re -nostdin -i "/home/ubuntu/$movie" \
    -vcodec libx264 -preset:v ultrafast \
    -acodec aac \
    -f rtsp rtsp://10.0.0.53:8554/movie
