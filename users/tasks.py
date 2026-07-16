# from csv import Error

from celery import shared_task
from time import sleep
from django.conf import settings

# @shared_task
# def add(x, y):
#     print("Отчет...")
#     sleep(20)
#     print("Завершено")
#     return x + y

#HW 6
@shared_task
def login_log(email):
    print(f"Пользователь {email} успешно вошёл в систему")
    return "OK"


@shared_task
def send_email(code, email):
    from django.core.mail import send_mail
    send_mail(
        "Приветствуем на нашей платформе",
        f"Вот твой код для регистрации: {code}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return "OK"


#HW 6
@shared_task
def print_statistics():
    from users.models import CustomUser

    total_users = CustomUser.objects.count()
    print(f"Статистика: всего пользователей - {total_users}")

    return total_users


# @shared_task
# def delete_unactive_users():
#     from users.models import CustomUser
#     deleted = CustomUser.objects.filter(is_active=False).delete()
#     return f"Удалено: {deleted}"

