from PIL import Image, ImageFont, ImageDraw
from django.db import models


class Client(models.Model):
    surname = models.CharField(max_length=128, blank=False, null=False, verbose_name="Прізвище")
    name = models.CharField(max_length=128, blank=False, null=False, verbose_name="Ім'я")
    fatname = models.CharField(max_length=128, blank=False, null=False, verbose_name="По-батькові")
    phone = models.PositiveIntegerField(blank=True, null=True, verbose_name="Номер телефону")
    email = models.EmailField(max_length=128, blank=True, null=True, verbose_name="Електронна пошта")
    tgid = models.CharField(max_length=32, blank=True, null=True, verbose_name="Телеграм id")

    def __str__(self):
        fullname = self.surname + ' ' + self.name + ' ' + self.surname
        return fullname


class Employer(models.Model):
    surname = models.CharField(max_length=128, blank=False, null=False, verbose_name="Прізвище")
    name = models.CharField(max_length=128, blank=False, null=False, verbose_name="Ім'я")
    fatname = models.CharField(max_length=128, blank=False, null=False, verbose_name="По-батькові")
    id_code = models.PositiveIntegerField(blank=False, null=False, verbose_name="ЄДРПОУ")
    bank = models.CharField(max_length=128, blank=False, null=False, verbose_name="Назва банку/філії")
    bank_account = models.CharField(max_length=256, blank=False, null=False, verbose_name="Номер рахунку")

    def __str__(self):
        fullname = self.surname + ' ' + self.name + ' ' + self.surname
        return fullname


class Course(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False, verbose_name="Назва курсу")

    def __str__(self):
        return self.name


class Check(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клієнт")
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, verbose_name="ФОП")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Напрям навчання")
    summary = models.PositiveIntegerField(verbose_name="Сума")
    text_font = ImageFont.truetype('font.ttf', 18)
    default_check_image = Image.open("default_check.jpg")
    client_check_image = ImageDraw.Draw(default_check_image)

    def save(self, *args, **kwargs):
        self.client_check_image.text((500, 20), str(self.summary), (0, 0, 0), font=self.text_font)
        self.client_check_image.text((500, 40), str(self.course), (0, 0, 0), font=self.text_font)
        self.client_check_image.text((500, 60), self.employer.surname, (0, 0, 0), font=self.text_font)
        self.client_check_image.text((500, 80), self.employer.name, (0, 0, 0), font=self.text_font)
        self.client_check_image.text((500, 100), self.employer.fatname, (0, 0, 0), font=self.text_font)
        self.client_check_image.text((500, 120), self.employer.bank, (0, 0, 0), font=self.text_font)
        self.client_check_image.text((500, 140), self.employer.bank_account, (0, 0, 0), font=self.text_font)
        self.client_check_image.text((500, 160), self.client.surname, (0, 0, 0), font=self.text_font)
        self.client_check_image.text((500, 180), self.client.name, (0, 0, 0), font=self.text_font)
        self.client_check_image.text((500, 200), self.client.fatname, (0, 0, 0), font=self.text_font)
        self.default_check_image.save("client_check.jpg")
        super(Check, self).save(*args, **kwargs)
