# Create your views here.
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, Http404
import json, random, datetime


# файл json необходимо открывать в каждом классе, где это необходимо. Если открыть только в начале этого файла, то при
# добавлении новой статьи на странице всех новостей не будет происходить сортировка по дате. В таком случае необходим
# перезапуск сервера
# with open(settings.NEWS_JSON_PATH) as json_f:
#     news_list = json.load(json_f)
#     fresh_news = sorted(news_list, key=lambda j: j['created'], reverse=True)
#     link_list = []
#     for i in news_list:
#         link_list.append(i['link'])


class MainPageView(View):
    def get(self, request):
        return redirect('/news/')
        # return HttpResponse('<h1>Coming soon</h1>')


class AllNewsPage(View):
    def get(self, request):
        q = request.GET.get('q')
        with open(settings.NEWS_JSON_PATH) as json_f:
            news_list = json.load(json_f)
            fresh_news = sorted(news_list, key=lambda j: j['created'], reverse=True)

        news_list_without_time = []
        for i in fresh_news:
            i['created'] = i['created'][:10]
            news_list_without_time.append(i)
        if q is None:
            return render(request, 'news/allnewspage.html',
                          context={'news_list_without_time': news_list_without_time})
        else:
            news_with_q = []
            for i in news_list_without_time:
                if q in i['title']:
                    news_with_q.append(i)
            return render(request, 'news/allnewspage.html',
                          context={'news_list_without_time': news_with_q})


class NewsView(View):
    def get(self, request, link_number):

        with open(settings.NEWS_JSON_PATH) as json_f:
            news_list = json.load(json_f)

        for single_news in news_list:
            if single_news['link'] == link_number:
                return render(request, 'news/index.html', context={'single_news': single_news})
        raise Http404


class CreateNews(View):
    def get(self, request):
        return render(request, 'news/create.html')

    def post(self, request):

        with open(settings.NEWS_JSON_PATH) as json_f:
            news_list = json.load(json_f)
            link_list = []
            for i in news_list:
                link_list.append(i['link'])

        title = request.POST.get('title')
        text = request.POST.get('text')
        while True:
            link = random.randint(1, 10000)
            if link in link_list:
                continue
            else:
                break
        users_news = {'created': str(datetime.date.today()), 'text': text, 'title': title, 'link': link}
        news_list.append(users_news)
        # fresh_news.append(users_news)
        with open("news.json", "w") as json_file:
            json.dump(news_list, json_file)
            # json.dump(fresh_news, json_file)
        return redirect('/news/')
