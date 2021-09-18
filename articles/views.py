from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from articles.models import Article, Ip


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def auth(request):
    if request.method == "POST":
        username = request.POST["login"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
        return HttpResponseRedirect("/")


def post_like(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h1>Article does not exist yet ):</h1>")

    user = request.user
    if user.is_authenticated:
        like = article.like_set.filter(user=user)
        if not like.exists():
            article.like_set.create(user=user, article=article)
        else:
            like.delete()
        return HttpResponseRedirect(f"/article/{id}")
    else:
        return HttpResponseRedirect("/")


def post_view(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h1>Article does not exist yet ):</h1>")

    ip = get_client_ip(request)

    if Ip.objects.filter(ip=ip).exists():
        article.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        article.views.add(Ip.objects.get(ip=ip))

    views = article.views.count()
    likes = article.like_set.count()

    context = {
        'article': article,
        'views': views,
        'likes': likes
    }
    return render(request, 'article.html', context)


def index(request):
    last_articles = Article.objects.order_by("-id")
    is_auth = request.user.is_authenticated
    print(is_auth)
    return render(request, "index.html", context={"articles": last_articles, "is_auth": is_auth})
