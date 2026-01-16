from core.celery import APP


@APP.task()
def send_otp_email(email, otp):
    print(f'sending otp - {otp} to email - {email}')