__author__ = 'allanpedroni'

import email
import glob, urllib
import mimetypes

simple_message = """\
From: allan
Content-Type: text/plain

Hello!
"""

# msg = email.message_from_string(simple_message)
# msg = email.message_from_file(open("RESPR1779.msg"))
# email.message_from_file(open())

for file in glob.glob("*"):
    url = urllib.pathname2url(file)
    print(file, mimetypes.guess_type(url))

#print("head", msg.items())
#print("content_type", msg.get_content_type())
#print("body", msg.get_payload())



multipart_message = """\
From: allan
Content-Type: multipart/alternative; boundary="BOUNDARY"

--BOUNDARY
Content-Type: text/plain
Content-Transfer-Encoding: 7bit

Hello!

--BOUNDARY
Content-Type: text/html
Content-Transfer-Encoding: quoted-printable

<p>Hello!</p>
--BOUNDARY--
"""

# msg = email.message_from_string(multipart_message)

# for part in msg.walk():
#    print("type", repr(part.get_content_type()))
#    print("body", repr(part.get_payload()))