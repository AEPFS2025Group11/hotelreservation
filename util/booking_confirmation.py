import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def send_booking_confirmation(to_email: str, guest_name: str, hotel_name: str,
                              check_in: str, check_out: str, room_type: str, booking_id: str):
    from_email = "denisvoegeli80@gmail.com"
    password = os.environ.get("EMAIL_PASSWORD")

    if not password:
        logging.error("❌ Kein Passwort in Umgebungsvariable EMAIL_PASSWORD gefunden.")
        return

    subject = f"Buchungsbestätigung – {hotel_name}"

    plain_body = f"""
    Hallo {guest_name},

    vielen Dank für Ihre Buchung im Hotel {hotel_name}!

    Zimmer: {room_type}
    Check-in: {check_in}
    Check-out: {check_out}
    Buchungsnummer: {booking_id}

    Bitte bringen Sie diese Bestätigung zur Anreise mit.

    Herzliche Grüße
    Ihr {hotel_name}-Team
    """

    html_body = f"""
    <html>
    <body>
        <p>Hallo {guest_name},</p>
        <p>vielen Dank für Ihre Buchung im Hotel <strong>{hotel_name}</strong>!</p>
        <ul>
            <li>🛏️ <strong>Zimmer</strong>: {room_type}</li>
            <li>📅 <strong>Check-in</strong>: {check_in}</li>
            <li>📅 <strong>Check-out</strong>: {check_out}</li>
            <li>📄 <strong>Buchungsnummer</strong>: {booking_id}</li>
        </ul>
        <p>Bitte bringen Sie diese Bestätigung zur Anreise mit.</p>
        <p>Herzliche Grüße<br>Ihr {hotel_name}-Team</p>
    </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(plain_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, password)
            server.send_message(message)
        logging.info("✅ Buchungsbestätigung erfolgreich gesendet.")
    except smtplib.SMTPAuthenticationError:
        logging.error("❌ Authentifizierungsfehler – bitte Zugangsdaten prüfen.")
    except smtplib.SMTPException as e:
        logging.error(f"❌ SMTP-Fehler: {e}")
    except Exception as e:
        logging.error(f"❌ Unbekannter Fehler beim E-Mail-Versand: {e}")
