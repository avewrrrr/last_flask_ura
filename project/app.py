from flask import Flask
from flask import (
    render_template, request, redirect, url_for, session, make_response
)
from db_connect import db, connect_db
import models
from sqlalchemy import func

app = Flask(__name__)
connect_db(app)

app.config['SECRET_KEY'] = 'very_secret_key'

@app.get('/set-theme/<theme>')
def set_theme(theme):
    if theme not in ['light', 'pink']:
        return redirect(request.referrer or url_for('main_page'))
    response = make_response(redirect(request.referrer or url_for('main_page')))
    response.set_cookie('theme', theme)
    return response

@app.get('/')
def main_page():
    return render_template('main_page.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        lol_user = models.User.query.filter_by(username=username).first()
        if lol_user:
            error = 'логин занят'
            return render_template('register.html', error=error)

        user = models.User(
            username=username,
            password=password,
        )

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        return redirect(url_for('notes'))

    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = models.User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('notes'))

    return render_template('login.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        note = models.Notes(
            title=title,
            text_in_note=text,
            user_id=user_id
        )

        db.session.add(note)
        db.session.commit()

        return redirect(url_for('notes'))

    search_query = request.args.get('q', '').strip()

    if search_query:
        notes = models.Notes.query.filter(
            models.Notes.user_id == user_id,
            func.lower(models.Notes.title).like(f'%{search_query.lower()}%')).all()
    else:
        notes = models.Notes.query.filter_by(user_id=user_id).all()

    return render_template('notes.html', notes=notes, search_query=search_query, search_count=len(notes))

@app.route('/notes/<int:note_id>/edit', methods=['POST'])
def update_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    note = models.Notes.query.get(note_id)

    if note.user_id != session['user_id']:
        return redirect(url_for('notes'))

    note.title = request.form['title']
    note.text_in_note = request.form['text']

    db.session.commit()
    return redirect(url_for('notes'))

@app.route('/notes/<int:note_id>/delete')
def delete_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    note = models.Notes.query.get(note_id)

    if note.user_id != session['user_id']:
        return redirect(url_for('notes'))

    db.session.delete(note)
    db.session.commit()

    return redirect(url_for('notes'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    profile = models.Profile.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        bio = request.form.get('bio')
        ava = request.form.get('ava')

        if profile:
            profile.bio = bio
            if ava:
                profile.ava = ava
        else:
            profile = models.Profile(
                bio=bio,
                ava=ava if ava else 'ava.jpg',
                user_id=user_id
            )
            db.session.add(profile)
        db.session.commit()
        return redirect(url_for('profile'))
    notes = models.Notes.query.filter_by(user_id=user_id).all()
    return render_template('profile.html', profile=profile, notes=notes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main_page'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
