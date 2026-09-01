import smtplib
from email.mime.text import MIMEText
from app.workers.celery_app import celery_app
from app.core.config import settings

@celery_app.task(name="send_order_confirmation")
def send_order_confirmation(order_id: int, customer_email: str):
    subject = f"Order #{order_id} Confirmed"
    body = f"Hi,\n\nYour order #{order_id} has been confirmed. Thank you for shopping with us!"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.smtp_username
    msg["To"] = customer_email

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.sendmail(settings.smtp_username, [customer_email], msg.as_string())
        print(f"[EMAIL SENT] Order {order_id} confirmation emailed to {customer_email}")
        return {"order_id": order_id, "email": customer_email, "status": "sent"}
    except Exception as e:
        print(f"[EMAIL FAILED] Order {order_id}: {e}")
        return {"order_id": order_id, "email": customer_email, "status": "failed", "error": str(e)}