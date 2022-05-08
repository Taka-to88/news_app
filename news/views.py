from django.shortcuts import render, get_object_or_404
from prometheus_client import Summary
from .models import News


def index(request):
    news = News.objects.order_by('-published')
    return render(request, 'news/index.html', {'news': news})


def news_detail(request, news_id):
    news = News.objects.get(pk=news_id)
    return render(request, 'news/news_detail.html', {'news': news})


def news_detail(request, post_id):
    news = get_object_or_404(News, pk=post_id)
    return render(request, 'news/news_detail.html', {'news': news})
