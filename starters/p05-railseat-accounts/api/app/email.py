"""Sending email (P5 add-on). In development every email lands in Mailpit."""


def send_email(to: str, subject: str, body: str) -> None:
    """Send a plain-text email (task 7, step 8).

    - Build the message with the standard library's `email.message.EmailMessage`
      (From, To, Subject and the body). A From such as
      `RailSeat <no-reply@example.com>` is fine.
    - Send it with `smtplib.SMTP` on settings.SMTP_HOST and settings.SMTP_PORT.
      Locally that is Mailpit on port 1025 (not 8025, which is its web page).
    - Never log a link that holds a token.
    """
    raise NotImplementedError("TODO(task 7): send the email with smtplib")
