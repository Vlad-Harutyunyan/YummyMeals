import os
from flask import (
    Blueprint, current_app
)
from flask_mail import Mail, Message
from ..users.models import User, UserFavoriteCategory
from ..meals.models import Meal, Category
import datetime
from datetime import timedelta

satatic_path = os.path.abspath(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static'))

mail_bp = Blueprint(
    'mail',
    __name__,
    template_folder='templates',
    url_prefix='/mail',
    static_folder='static',
    static_url_path=satatic_path
)


def mail_send():
    app = current_app._get_current_object()
    mail = Mail(app)
    fav = UserFavoriteCategory.query.all()
    time_trigger = datetime.datetime.utcnow() - timedelta(hours=24)
    updated_list = []
    updated = Meal.query.filter(Meal.date_posted > time_trigger).all()
    for j in updated:
        updated_list.append(j.category_id)
    updated_list = list(set(updated_list))
    for x in fav:
        if x.category_id in updated_list:
            print("ok")
            msg = Message(
                'New Recipe', sender='yummymealbook@gmail.com', recipients=[
                    f'{User.query.filter(User.id == x.user_id).first().email}'])
            msg.body = f'Hello dear' \
                f' {User.query.filter(User.id == x.user_id).first().username}! ' \
                f' We have good news for you!   A new recipe for your' \
                f' selected category ' \
                f'{Category.query.filter(Category.id == x.category_id).first().name}' \
                f' has arrived!'
            mail.send(msg)

    return f'mails sent {datetime.datetime.utcnow()}'

# schedule.every(60).minutes.do(index)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
