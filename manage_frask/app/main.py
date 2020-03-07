from flask import Blueprint, render_template
from flask_login import current_user
#from app.models import Event

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/admin/event')
def event_manage():
    return render_template('event.html')

@main.route('/admin/tweet')
def tweet_manage():
    return render_template('tweet.html')

