import yagmail
from config import from_email, password, to_email


receiver = to_email
body = "Below you find file with actual tenders from Berezka platform"
filename = "01-10-2020_14-54.xlsx"
contents = [
    body,
    filename
]

yagmail.register(from_email, password)
yag = yagmail.SMTP(from_email)
yag.send(
    to=receiver,
    subject="Berezka Tenders",
    contents=contents,
    # attachments=filename,
)