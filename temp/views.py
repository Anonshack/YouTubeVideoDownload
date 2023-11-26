from django.shortcuts import render, redirect
from django.views import View
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable


class Home(View):
    def get(self, request):
        return render(request, 'download/index.html')

    def post(self, request):
        try:
            if request.POST.get('fetch-vid'):
                self.url = request.POST.get('given_url')
                video = YouTube(self.url)
                vidTitle, vidThumbnail = video.title, video.thumbnail_url
                qual, stream = [], []
                for vid in video.streams.filter(progressive=True):
                    qual.append(vid.resolution)
                    stream.append(vid)
                context = {'vidTitle': vidTitle, 'vidThumbnail': vidThumbnail,
                           'qual': qual, 'stream': stream,
                           'url': self.url}
                return render(request, 'download/index.html', context)

            elif request.POST.get('download-vid'):
                self.url = request.POST.get('given_url')
                video = YouTube(self.url)
                stream = [x for x in video.streams.filter(progressive=True)]
                if not stream:
                    raise ValueError("No progressive streams available for download.")

                video_qual = stream[int(request.POST.get('download-vid')) - 1]
                video_qual.download(output_path='../../Downloads')
                return redirect('home')

        except (RegexMatchError, VideoUnavailable, ValueError) as e:
            print(f"Error: {e}")

        return render(request, 'download/index.html')
