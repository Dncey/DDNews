import datetime
from news.models import User
import random
def add_test_users():
    now = datetime.datetime.now()
    for num in range(0, 10000):
        try:
            user = User()
            user.username = "%011d" % num
            user.mobile = "%011d" % num
            user.password = "e10adc3949ba59abbe56e057f20f883e"
            user.last_login = now - datetime.timedelta(seconds=random.randint(0, 2678400))
            user.save()
            print(user.mobile)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    add_test_users()