from models import Page
from faker import Faker

fake = Faker()


for _ in range(0,10):
    test = Page(url = fake.url())
    test.status = 'active'
    test.keyword = fake.word()
    test.save()
