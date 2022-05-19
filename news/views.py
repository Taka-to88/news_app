from django.shortcuts import render, get_object_or_404
from .models import News
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    news = News.objects.order_by('-published')
    paginator = Paginator(news, 4)
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)
    context = {'pages': pages}

    return render(request, 'news/index.html', context)


# def news_detail(request, news_id):
#     news = News.objects.get(pk=news_id)
#     return render(request, 'news/news_detail.html', {'news': news})


# def news_detail(request, post_id):
#     news = get_object_or_404(News, pk=post_id)
#     return render(request, 'news/news_detail.html', {'news': news})
