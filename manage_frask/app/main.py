from flask import Blueprint, render_template
from flask_login import current_user
from app.models import Event

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/admin/event', methods=['GET'])
def event_manage():
    events = jsonify((Event.all()).to_dict())
    return render_template('event.html', events=events)

@main.route('/admin/event/<int:event_id>', methods=['GET'])
def get_event(event_id=None):
    # DBからフィルタリングして取得
    event = Event.query.filter_by(id=event_id).first()
    return jsonify(event.to_dict())


@main.route('/admin/event', methods=['POST'])
def post_event():
    name = request.form.get('event_name')
    event_date = request.form.get('event_date')
    adstart_date = request.form.get('adstart_date')
    end_date = request.form.get('end_date')

    event_by_name = User.query.filter_by(name=name).first()
    if name:
        flash('イベント名が重複しています')
        return redirect(url_for('main.event_manage'))

    # レコードの登録 新規作成したオブジェクトをaddしてcommit
    event = Event(name, event_date, adstart_date, end_date)
    db.session.add(event)
    db.session.commit()

    response = jsonify(event.to_dict())
    # レスポンスヘッダ設定
    response.headers['Location'] = '/api/events/%d' % event.id
    # HTTPステータスを200以外で返却したい場合
    return response, 201


@main.route('/admin/event/<event_id>', methods=['PUT'])
def put_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        abort(404, {'code': 'Not found', 'message': 'event not found'})

    event.name = request.form.get('event_name')
    event.event_date = request.form.get('event_date')
    event.adstart_date = request.form.get('adstart_date')
    event.end_date = request.form.get('end_date')
    db.session.commit()

    return jsonify(event.to_dict())


@main.route('/admin/event/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        abort(404, {'code': 'Not found', 'message': 'event not found'})

    db.session.delete(event)
    db.session.commit()

    return jsonify(None), 204

@main.route('/admin/tweet')
def tweet_manage():
    return render_template('tweet.html')

