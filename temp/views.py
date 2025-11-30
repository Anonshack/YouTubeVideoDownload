from django.shortcuts import render, redirect
from django.views import View
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
from urllib.error import HTTPError


class Home(View):
    template_name = 'download/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        url = request.POST.get('given_url')
        if request.POST.get('fetch-vid') == "1":
            try:
                yt = YouTube(
                    url,
                    use_oauth=False,
                    allow_oauth_cache=True
                )

                streams = list(yt.streams.filter(progressive=True))

                if not streams:
                    return render(request, self.template_name, {
                        "error": "Video format topilmadi!"
                    })

                context = {
                    "url": url,
                    "title": yt.title,
                    "thumb": yt.thumbnail_url,
                    "streams": streams,
                }

                return render(request, self.template_name, context)

            except (RegexMatchError, VideoUnavailable):
                return render(request, self.template_name, {
                    "error": "Noto'g'ri URL yoki video mavjud emas!"
                })

            except HTTPError as e:
                return render(request, self.template_name, {
                    "error": f"HTTP Error: {e}"
                })

            except Exception as e:
                return render(request, self.template_name, {
                    "error": f"Xatolik: {e}"
                })

        if request.POST.get('download-vid'):
            try:
                index = int(request.POST.get('download-vid')) - 1
                yt = YouTube(url)

                streams = list(yt.streams.filter(progressive=True))
                streams[index].download(output_path='Downloads')

                return redirect("home")

            except Exception as e:
                return render(request, self.template_name, {
                    "error": f"Yuklab olishda xatolik: {e}"
                })

        return render(request, self.template_name)
