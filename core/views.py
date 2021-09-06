import logging
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from redmonkey.settings import WEBHOOK_LISTEN, WEBHOOK_PORT, WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV, WEBHOOK_URL_BASE, \
    WEBHOOK_URL_PATH
from .forms import ClientForm, CheckForm, EmployerForm
from .models import Client, Employer
from telebot import TeleBot, types, logger

logger.setLevel(logging.DEBUG)

bot = TeleBot(settings.TOKEN)


class WebHookView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"ok": "Get request processed. But nothing done"})

    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])

        return JsonResponse({"ok": "POST request processed"})


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Ваш телеграм id: " + str(message.chat.id))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


def send_check(check):
    photo = open('client_check.jpg', 'rb')
    bot.send_photo(chat_id=check.client.tgid, photo=photo)


def index(request):
    return render(request, 'index.html', {})


def client_list(request):
    clients = Client.objects.order_by('-surname')
    return render(request, 'client/client_list.html', {'clients': clients})


def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'client/client_detail.html', {'client': client})


def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm()
    return render(request, 'client/client_create.html', {'form': form})


def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    return render(request, 'client/client_edit.html', {'form': form})


def employer_list(request):
    employers = Employer.objects.order_by('-surname')
    return render(request, 'employer/employer_list.html', {'employers': employers})


def employer_detail(request, pk):
    employer = get_object_or_404(Employer, pk=pk)
    return render(request, 'employer/employer_detail.html', {'employer': employer})


def employer_create(request):
    if request.method == "POST":
        form = EmployerForm(request.POST)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.save()
            return redirect('employer_detail', pk=employer.pk)
    else:
        form = EmployerForm()
    return render(request, 'employer/employer_create.html', {'form': form})


def employer_edit(request, pk):
    employer = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        form = EmployerForm(request.POST, instance=employer)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.save()
            return redirect('employer_detail', pk=employer.pk)
    else:
        form = EmployerForm(instance=employer)
    return render(request, 'employer/employer_edit.html', {'form': form})


def check_create(request):
    if request.method == "POST":
        form = CheckForm(request.POST)
        if form.is_valid():
            check = form.save(commit=False)
            check.save()
            send_check(check)
            return redirect('index')
    else:
        form = CheckForm()
    return render(request, 'check/check_create.html', {'form': form})


bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

