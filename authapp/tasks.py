from scinet.celery import app


@app.task
def task_send_activation_email(user):
    # send_verify_email(user)
    print("Письмо отправлено!", user.email)


@app.task
def unlocked_user_through_two_weeks():
    pass
