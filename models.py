from mongoengine import *
from datetime import datetime

connect('test_db')

class Page(Document):
    url = StringField()
    status = StringField()
    keyword = StringField()
    last_updated = DateTimeField(default = datetime.now)
    archived = BooleanField(default = False)
