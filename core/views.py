import logging
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from telebot import TeleBot, types, logger
from .forms import ClientForm, CheckForm, EmployerForm
from .models import Client, Employer, Check
from redmonkey.settings import ADMIN_TGID, ADMIN_EMAIL, TOKEN, EMAIL_HOST_USER

logger.setLevel(logging.DEBUG)

bot = TeleBot(TOKEN)


def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return HttpResponse(status=200)


def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://redmonkeycheckmaker.herokuapp.com' + TOKEN)
    return HttpResponse(status=200)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Ваш телеграм id: " + str(message.chat.id))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


def send_check_tg(tgid):
    photo = open('client_check.jpg', 'rb')
    bot.send_photo(chat_id=tgid, photo=photo)


def send_check_email(email):
    subject = 'Чек від RedMonkey'
    message = 'Lorem ipsum'
    email_from = EMAIL_HOST_USER
    recipient_list = [email, ADMIN_EMAIL]
    msg = EmailMessage(subject, message, email_from, recipient_list)
    msg.attach_file('client_check.jpg')
    msg.send()


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
    employer = get_object_or_404(Employer, pk=pk)
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
            if check.client.tgid != 'default':
                send_check_tg(check.client.tgid)
                send_check_tg(ADMIN_TGID)
            else:
                send_check_tg(ADMIN_TGID)
                send_check_email(ADMIN_EMAIL)
            send_check_email(check.client.email)
            return redirect('index')
    else:
        form = CheckForm()
    return render(request, 'check/check_create.html', {'form': form})
