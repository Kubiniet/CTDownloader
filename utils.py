from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable


url = "https://www.youtube.com/watch?v=rGB3KodPfpY"
url_playlist = "https://www.youtube.com/watch?v=aMHDVsHFxN0&list=RDaMHDVsHFxN0"

yt = YouTube(url)
pl = Playlist(url_playlist)

# if len(pl) > 0:
#     for index, url in enumerate(pl.video_urls):
#         try:
#             yt = YouTube(url)
#             print("ffdffd")
#         except VideoUnavailable:
#             print(f"Video {url} is unavaialable, skipping.")
#         else:
#             print(f"Downloading video: {url}")
# else:
#     print("is empty")

try:
    yt = YouTube(url)
    print(yt.check_availability())
except VideoUnavailable:
    print(f"Video {url} is unavaialable, skipping.")
else:
    print(f"Downloading video: {url}")
