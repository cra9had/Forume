from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponseNotFound, JsonResponse

from articles.forms import RegistrationForm
from articles.models import Article, AnonimReader
from django.views.decorators.csrf import csrf_exempt


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
def auth(request):
    if request.method == "POST" and request.is_ajax():
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember")
        if not remember_me == "true":
            request.session.set_expiry(0)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "error_text": "Логин или пароль неверны."})
    else:
        return HttpResponseNotFound("<h1>Page does not exists ):</h1>")


@csrf_exempt
def read_article(request, id: int):
    if request.method == "POST":
        device_id = request.POST.get("device_id")
        ip = get_client_ip(request)
        reader, _ = AnonimReader.objects.get_or_create(device_id=device_id)
        reader.ip = ip
        reader.save()
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return JsonResponse({"status": "error", "error_text": "Article does not exist yet...", "error_code": 404})
        article.views.add(reader)
        return JsonResponse({"status": "success"})



@csrf_exempt
def register(request):
    if request.method == "POST" and request.is_ajax():
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse(
                {'status': 'error', 'error_text': user_form.errors})


@csrf_exempt
def post_like(request, id):
    if request.is_ajax():
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return JsonResponse({"status": "error", "error_text": "Article does not exist yet...", "error_code": 404})

        user = request.user
        if user.is_authenticated:
            like = article.like_set.filter(user=user)
            if not like.exists():
                article.like_set.create(user=user, article=article)
                liked = 1
            else:
                like.delete()
                liked = -1
            return JsonResponse({"status": "success", "count": article.like_set.count(), "liked": liked})
        else:
            return JsonResponse({"status": "error", "error_text": "Auth is required", "error_code": 405})
    else:
        return HttpResponseNotFound("<h1>Page does not exists ):</h1>")


def post_view(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h1>Article does not exist yet ):</h1>")

    # ip = get_client_ip(request)
    #
    # if Ip.objects.filter(ip=ip).exists():
    #     article.views.add(Ip.objects.get(ip=ip))
    # else:
    #     Ip.objects.create(ip=ip)
    #     article.views.add(Ip.objects.get(ip=ip))
    #     article.views.add(Ip.objects.get(ip=ip))
    #
    views = article.views.count()
    likes = article.like_set.count()
    like = False

    if request.user.is_authenticated:
        if article.like_set.filter(user=request.user).exists():
            like = True

    context = {
        'article': article,
        'views': views + 1,
        'likes': likes,
        'is_auth': request.user.is_authenticated,
        'user_like': like,
        'user': request.user,
    }
    return render(request, 'article.html', context)


def index(request):
    last_articles = Article.objects.order_by("-id")
    is_auth = request.user.is_authenticated
    return render(request, "index.html", context={"articles": last_articles, "is_auth": is_auth, "user": request.user})
