#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Общие модели
PERSON_TYPE_CHOICES = (
    ('s', 'Студент'),
    ('a', 'Ассистент'),
    ('t', 'Старший преподаватель'),
    ('d', 'Доцент'),
    ('p', 'Профессор'),
)
ACADEMIC_STATUS_CHOICES = (
  ('x', 'Студент'),
  ('a', 'Ассистент'),
  ('s', 'Старший преподаватель'),
  ('d', 'Доцент'),
  ('p', 'Профессор'),
)

ACADEMIC_DEGREE_CHOICES = (
  ('n', 'Без степени'),
  ('t', 'Кандидат наук'),
  ('d', 'Доктор наук'),
)

#База цитирования для публикаций
CITE_BASE_CHOICES = (
    ('scp', 'Scopus'),
    ('wos', 'Web of Science'),
    ('nil', 'отсутствует')
)

# Разграничение ролей

USER_ROLES = (
    ('u', 'Сотрудник'),
    ('a', 'Руководитель')
)


class UserProfile(models.Model):
  user = models.OneToOneField(User)

  patronymic = models.CharField(max_length=30, null=True)
  birth_date = models.DateField(null=True)
  study_group = models.CharField(max_length=5, null=True)
  github_id = models.CharField(max_length=100, null=True)
  stepic_id = models.CharField(max_length=100, null=True)

  type = models.CharField(max_length=2, choices=PERSON_TYPE_CHOICES, default='s')
  typestr = ' '
  academic_degreestr=' '
  # Дата текущего избрания или зачисления на преподавательскую должность
  election_date = models.DateField(null=True)

  # Должность
  position = models.CharField(max_length=40, null=True)

  # Срок окончания трудового договора
  contract_date = models.DateField(null=True)  # Возможн поменяю

  # Ученая степень
  academic_degree = models.CharField(max_length=1, choices=ACADEMIC_DEGREE_CHOICES, null=True)

  # Год присвоения ученой степени
  year_of_academic_degree = models.DateField(null=True)

  # Учебное звание
  academic_status = models.CharField(max_length=1, choices=ACADEMIC_STATUS_CHOICES, null=True)
  year_of_academic_status = models.DateField(null=True)

  # Доступ к данным
  user_role = models.CharField(max_length=1, choices=USER_ROLES, null=True)

  @property
  def first_name(self):
    return self.user.first_name

  @property
  def last_name(self):
    return self.user.last_name

  @property
  def login(self):
    return self.user.username

  @property
  def password(self):
    return self.user.password

  @property
  def email(self):
    return self.user.email

  @property
  def privileged(self):
    return self.is_superuser

  @staticmethod
  def create(login, password, email, **params):
    user = User.objects.create_user(login, password, email)
    user.first_name = params.get('first_name')
    user.last_name = params.get('last_name')
    user.save()

    user_profile = UserProfile.objects.create(
      user=user,
      patronymic=params.get('patronymic'),
      birth_date=params.get('birth_date'),
      study_group=params.get('study_group'),
      github_id=params.get('github_id'),
      stepic_id=params.get('stepic_id'),
      type=params.get('type', 's'),
      election_date=params.get('election_date'),
      position=params.get('position'),
      contract_date=params.get('contract_date'),
      academic_degree=params.get('academic_degree'),
      year_of_academic_degree=params.get('year_of_academic_degree'),
      academic_status=params.get('academic_status'),
      year_of_academic_status=params.get('year_of_academic_status')
    )

    user_profile.save()

    return user_profile

  def __str__(self):
    return self.first_name + ' ' + self.last_name + ' ' + self.patronymic

  class Meta:
    db_table = 'userprofiles'


# Описание моделей приложения scientificWork

class Publication(models.Model):
    tpPubl = (
        ('guidelines', 'Методическое указание'),
        ('book', 'Книга'),
        ('journal', 'Статья в журнале'),
        ('compilation', 'Конспект лекции/сборник докладов'),
        ('collection ', 'Сборник трудов')
    )
    reIter = (
        ('disposable', 'одноразовый'),
        ('repeating','повторяющийся')
    )
    user = models.ForeignKey(UserProfile, default="")
    typePublication = models.CharField("Тип публикации",
                                       max_length="20",
                                       choices=tpPubl,
                                       default="book")

    publishingHouseName = models.CharField("Название издательства", max_length="100")  # название издательства
    place = models.CharField("Место издания", max_length="100")  #  место издания
    date = models.DateField("Дата издания")  #  дата издания
    volume = models.IntegerField("Объем")  #  объем
    unitVolume = models.CharField("Единицы объёма", max_length="100")  #  еденицы объема
    edition = models.IntegerField("Тираж")  #  тираж

    bookName = models.CharField("Название", max_length="300",
                            help_text="Название публикации")  #  название публикации
    type = models.CharField("Вид", max_length="100",
                            help_text="Поле заполняется, если тип вашей публикации"
                                      " \"Книга\" или \"Методическое указание\"")  #  вид методического издания / книги
    isbn = models.CharField("ISBN", max_length="100",
                            help_text="Поле заполняется, если тип вашей публткации"
                                      "\"Книга\" или \"Методическое указание\"")  #  ISBN
    number = models.IntegerField("Номер издания")  #  номер издания
    editor = models.CharField("Редактор сборника", max_length="100")  #  редакто сборника
    reiteration = models.CharField("Вид повторения сборника",
                                   choices=reIter,
                                   max_length="10",
                                   default="disposable"
                                   )  #  вид повторения сборника

    citingBase = models.CharField("База цитирования", choices=CITE_BASE_CHOICES, max_length="3", default='nil')

    def __str__(self):
        return self.bookName

class Participation(models.Model):
    tp = (
        ('conference', 'конференция'),
        ('seminar', 'семинар')
    )
    user = models.ForeignKey(UserProfile, default="")
    type = models.CharField("Тип", choices=tp, max_length="10", default="conference")  #  тип: конференция - conference, семинар - seminar
    name = models.CharField("Название", max_length="100")  # название
    date = models.DateField("Дата проведения")  # дата проведения
    place = models.CharField("Место проведения", max_length="100")  # дата проведения
    reIter = (
        ('disposable', 'одноразовый'),
        ('repeating', 'повторяющийся')
    )
    reiteration = models.CharField("Вид повторения сборника",
                                    choices=reIter,
                                    max_length="10",
                                    default="disposable"
                                   )  # вид повторения сборника

    rank = models.CharField("Ранг", max_length="100") # ранг


class Rand(models.Model):
    user = models.ForeignKey(UserProfile, default="")
    name = models.CharField("Название НИОКР", max_length="100")  # Название НИОКР
    cipher = models.CharField("Шифр", max_length="100")  #Шифр
