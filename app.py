from flask import Flask, render_template, request, redirect, url_for, Response, make_response, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message as MailMessage
from datetime import datetime, timedelta
import io
import textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from database import db, Message
from chat_openai import generate_response
from prompts import generate_prompt



app = Flask(__name__)

# === Mail Ayarları ===
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ummu1281@gmail.com'
app.config['MAIL_PASSWORD'] = 'jgvx euoz yiky ujid'
app.config['MAIL_DEFAULT_SENDER'] = 'ummu1281@gmail.com'
mail = Mail(app)

# === Veritabanı Ayarları ===
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = "gizli_key"
app.permanent_session_lifetime = timedelta(minutes=30)



@app.route('/')
def index():
    breadcrumbs = [
        {'name': 'Homepage', 'url': '#'}
    ]
    return render_template('index.html', breadcrumbs=breadcrumbs)


@app.route('/select-artwork/<artist_name>')
def select_artwork(artist_name):
    username = session.get('username')
    session['artist'] = artist_name  # Bu satır önemli

    breadcrumbs = [
        {'name': 'Homepage', 'url': url_for('index')},
        {'name': 'Select Artist', 'url': url_for('select_artist')},
        {'name': 'Select Artwork', 'url': '#'}
    ]

    return render_template('select_artwork.html', artist=artist_name, username=username, breadcrumbs=breadcrumbs)




@app.route('/select-artist', methods=['GET', 'POST'])
def select_artist():
    if request.method == 'POST':
        username = request.form['username']
        age = request.form['age']
        session['username'] = username
        session['age'] = age
    else:
        username = session.get('username')
        age = session.get('age')

    breadcrumbs = [
        {'name': 'Homepage', 'url': url_for('index')},
        {'name': 'Select Artist', 'url': '#'}
    ]
    return render_template('select_artist.html', username=username, age=age, breadcrumbs=breadcrumbs)



@app.route('/art-and-stories')
def art_and_stories():
    return render_template('art_and_stories.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == 'museum123':
            session['admin_logged_in'] = True
            return redirect(url_for('logs'))
        else:
            error = "Incorrect password."
    return render_template('admin_login.html', error=error)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        flash("Please fill in all fields.", "error")
        return redirect(url_for('about'))

    mail_body = f"""
    New contact form submission:

    Name: {name}
    Email: {email}
    Message:
    {message}
    """

    try:
        msg = MailMessage(subject='New Contact Form Message', recipients=['ummu1281@gmail.com'], body=mail_body)
        mail.send(msg)
        flash("Your message has been sent successfully!", "success")
    except Exception:
        flash("An error occurred while sending the message.", "error")

    return redirect(url_for('about'))

@app.route('/logs')
def logs():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    username = request.args.get('username')
    artwork = request.args.get('artwork')
    query = Message.query

    if username:
        query = query.filter(Message.username.ilike(f"%{username}%"))
    if artwork:
        query = query.filter(Message.artwork.ilike(f"%{artwork}%"))

    messages = query.order_by(Message.timestamp).all()
    return render_template('logs.html', messages=messages)

@app.route('/download-logs')
def download_logs():
    all_messages = Message.query.order_by(Message.timestamp).all()
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 40
    pdf.setFont("Helvetica", 11)

    for msg in all_messages:
        line = f"[{msg.timestamp.strftime('%Y-%m-%d %H:%M')}] {msg.username} ({msg.sender}): {msg.text}"
        wrapped_lines = textwrap.wrap(line, width=100)
        for wrapped_line in wrapped_lines:
            pdf.drawString(40, y, wrapped_line)
            y -= 18
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 11)
                y = height - 40

    pdf.save()
    buffer.seek(0)
    return make_response(buffer.read(), {
        "Content-Type": "application/pdf",
        "Content-Disposition": "attachment; filename=chat_logs.pdf"
    })

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}



@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        # GET ile gelen bilgiler
        username = request.args.get('username')
        age = request.args.get('age') or session.get('age')
        artwork = request.args.get('artwork')
        artist = request.args.get('artist')

        # Bilgileri session'a kaydet
        if username:
            session['username'] = username
        if age:
            session['age'] = age
        if artwork:
            session['artwork'] = artwork
        if artist:
            session['artist'] = artist

        # Breadcrumbs için artist session'dan alınır
        artist = session.get('artist')

        # Breadcrumb dizisi
        breadcrumbs = [
            {'name': 'Homepage', 'url': url_for('index')},
            {'name': 'Select Artist', 'url': url_for('select_artist')},
            {'name': 'Select Artwork', 'url': url_for('select_artwork', artist_name=artist)},
            {'name': 'Chat', 'url': '#'}
        ]

        return render_template(
            'chat.html',
            username=session.get('username'),
            artwork=session.get('artwork'),
            breadcrumbs=breadcrumbs
        )

    # POST metodu → mesaj gönderme işlemi
    username = session.get('username')
    age = session.get('age')
    artwork = session.get('artwork')


    # Kullanıcı mesajı alınır
    user_message = request.json.get('message')

    # artwork formatlanır
    normalized_artwork = artwork.replace(" ", "_").lower()

    # Prompt seçilir
    persona_prompt = generate_prompt(normalized_artwork)

    # Kullanıcı mesajı veritabanına kaydedilir
    user_msg = Message(username=username, age=age, artwork=artwork, sender='user', text=user_message)
    db.session.add(user_msg)
    db.session.commit()

    # Bot cevabı oluşturulur
    bot_reply = generate_response(persona_prompt, user_message)
    print("DEBUG - Bot cevabı:", bot_reply)

    # Bot cevabı veritabanına kaydedilir
    if bot_reply and bot_reply.strip():
        bot_msg = Message(username=username, age=age, artwork=artwork, sender='bot', text=bot_reply.strip())
        db.session.add(bot_msg)
        db.session.commit()
    else:
        print("⚠️ Bot cevabı boş geldi.")

    return Response(bot_reply, content_type='text/plain')

