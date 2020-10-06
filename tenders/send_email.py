import yagmail
from config import from_email, password, to_emails, cc, bcc


receiver = to_emails
body = "Below you find file with actual tenders from Berezka platform"
filename = "out\\05-10-2020_09-31.xlsx"
contents = [
    body,
    filename
]

yagmail.register(from_email, password)
yag = yagmail.SMTP(from_email)
yag.send(
    to=receiver,
    # cc=cc,
    # bcc=bcc,
    subject="Berezka Tenders",
    contents=contents,
    # attachments=filename,
)