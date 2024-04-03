def send_mail(to: str, subject: str, body: str, attachments: list[str] = []) -> str:
    """
    Send an email.

    :param to: The email address to send the email to
    :param subject: The subject of the email
    :param body: The body of the email
    :param attachments: A list of file paths or URLs to attach to the email
    :return: A message indicating that the email was sent
    """
    # Send the email
    print("Sending email")
    return f"Email sent to {to} with subject {subject} and body {body} and attachments {attachments}"
