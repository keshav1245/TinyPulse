import logging
import smtplib
from email.message import EmailMessage

from app.celery_app import celery_app
from app.core.config import settings

logger = logging.getLogger(__name__)


def _send_email(subject:str, html_body: str) -> None:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] =  f"{settings.NOTIFICATION_EMAILS_FROM} <{settings.SMTP_USERNAME}>"
    message["To"] = ", ".join(settings.NOTIFICATION_EMAILS_TO)
    message.set_content("This email requires an HTML-capable client to view.")
    message.add_alternative(html_body, subtype="html")

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        smtp.send_message(message)


@celery_app.task(name="notifications.send_downtime_email")
def send_downtime_email(site_name: str, site_url: str) -> None:
    logger.info(f"Sending downtime info for {site_name} ({site_url})")
    _send_email(
        subject=f"🔴 {site_name} is down",
        html_body=f"<p><b>{site_name}</b> ({site_url}) has stopped responding.</p>"
    )

@celery_app.task(name="notifications.send_uptime_email")
def send_uptime_email(site_name: str, site_url: str, downtime_seconds: int) -> None:
    minutes = round(downtime_seconds / 60, 1)
    logger.info(f"Sending Uptime info for {site_name}, ({site_url})")
    _send_email(
        subject=f"🟢 {site_name} is back up",
        html_body=f"<p><b>{site_name}</b> ({site_url}) is back up and running. It was down for {minutes} minute(s)</p>"
    )