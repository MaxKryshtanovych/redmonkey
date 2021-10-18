from PIL import Image, ImageFont, ImageDraw
from django.db import models


class Person(models.Model):
    surname = models.CharField(max_length=128, blank=False, null=False, verbose_name="Прізвище")
    name = models.CharField(max_length=128, blank=False, null=False, verbose_name="Ім'я")
    fatname = models.CharField(max_length=128, blank=False, null=False, verbose_name="По-батькові")

    def __str__(self):
        fullname = f'{self.surname} {self.name} {self.fatname}'
        return fullname

    class Meta:
        abstract = True


class Student(Person):

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенти'


class Client(Person):
    # pass_id = models.CharField(max_length=32, blank=False, null=False, verbose_name="Серія/номер паспорту")
    # pass_detail = models.CharField(max_length=256, blank=False, null=False, verbose_name="Детально про паспорт")
    # ipn = models.PositiveIntegerField(blank=False, null=False, verbose_name="ІПН")
    phone = models.CharField(max_length=12, blank=True, null=True, verbose_name="Номер телефону")
    email = models.EmailField(max_length=128, blank=True, null=True, verbose_name="Електронна пошта")
    tgid = models.CharField(max_length=32, blank=True, null=True, default='default', verbose_name="Телеграм id")
    is_parent = models.BooleanField(default=False, verbose_name="Ця особа є платником студента")

    class Meta:
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'


class Employer(Person):
    id_code = models.PositiveIntegerField(blank=False, null=False, verbose_name="ЄДРПОУ")
    bank = models.CharField(max_length=128, blank=False, null=False, verbose_name="Назва банку/філії")
    bank_account = models.CharField(max_length=256, blank=False, null=False, verbose_name="Номер рахунку")

    class Meta:
        verbose_name = 'ФОП'
        verbose_name_plural = 'ФОПи'


class Course(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False, verbose_name="Назва курсу")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курси'


class Check(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, verbose_name="Клієнт")
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="Студент")
    employer = models.ForeignKey(Employer, on_delete=models.DO_NOTHING, verbose_name="ФОП")
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name="Напрям навчання")
    summary = models.PositiveIntegerField(verbose_name="Сума")
    text_font = ImageFont.truetype('font.ttf', 18)
    default_check_image = Image.open("default_check.jpg")
    client_check_image = ImageDraw.Draw(default_check_image)
    pub_date = models.DateField(auto_now_add=True)

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
        if self.client.is_parent:
            self.client_check_image.text((500, 220), self.student.surname, (0, 0, 0), font=self.text_font)
            self.client_check_image.text((500, 240), self.student.name, (0, 0, 0), font=self.text_font)
            self.client_check_image.text((500, 260), self.student.fatname, (0, 0, 0), font=self.text_font)
        self.default_check_image.save("client_check.jpg")
        super(Check, self).save(*args, **kwargs)

    def __str__(self):
        fullname = f'{self.client.surname} {self.client.name} {self.client.fatname} {self.summary} грн. {self.pub_date}'
        return fullname

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
