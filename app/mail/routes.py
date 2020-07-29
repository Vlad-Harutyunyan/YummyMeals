from flask import (
    Flask,
    g,
    url_for,
    redirect,
    render_template,
    Blueprint, current_app
)
import schedule
import os
from flask_login import current_user
from flask_mail import Mail, Message
from ..users.models import User,User_Favorite_Category
from ..meals.models import Meal,Category
import datetime
from datetime import timedelta
import time

satatic_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))

class threadClass:

    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                       # Daemonize thread
        thread.start()                             # Start the execution

    def run(self):

         #
         # This might take several minutes to complete
         someHeavyFunction()



mail_bp = Blueprint(
    'mail',
    __name__,
    template_folder='templates',
    url_prefix='/mail',
    static_folder='static',
    static_url_path=satatic_path
)


@mail_bp.route('/')
def index():
    app=current_app._get_current_object()
    mail=Mail(app)
    fav=User_Favorite_Category.query.all()
    time_trigger=datetime.datetime.utcnow()- timedelta(hours=24)
    updated_list=[]
    updated=Meal.query.filter(Meal.date_posted>time_trigger).all()
    for j in updated:
        updated_list.append(j.category_id)
    updated_list=list(set(updated_list))
    for x in fav:
        if x.category_id in updated_list:
            print("ok")
            msg = Message('Hello', sender='yummymealbook@gmail.com',
                          recipients=[f'{User.query.filter(User.id==x.user_id).first().email}'])
            msg.body = f'Hello dear {User.query.filter(User.id==x.user_id).first().username}!  We have good news for you!   A new recipe for your selected category "{Category.query.filter(Category.id==x.category_id).first().name}" has arrived!'
            mail.send(msg)

    return f'mails sent {datetime.datetime.utcnow()}'


# schedule.every(60).minutes.do(index)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
