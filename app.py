import os 
from flask import Flask, render_template, redirect, url_for, request, flash
from dotenv import load_dotenv
from models import db, Usuario, Link

load_dotenv()

app = Flask(__name__)

db_url = os.getenv('DATABASE_URL')
if not db_url:
    raise ValueError("DATABASE_URL não está configurado no arquivo .env")

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

@app.route('/')
def index():
    return "Olá, mundo!"

@app.route('/admin')
def admin_page():
    usuario = Usuario.query.filter_by(username='diego').first()

    if not usuario:
        flash("Usuario 'diego' não encontrado. Crie-o no terminal", "danger")
        return redirect(url_for('index'))
    
    return render_template('admin.html', usuario=usuario)

@app.route('/admin/add', methods=['POST'])
def add_link():
    titulo_form = request.form.get('titulo')
    url_form = request.form.get('url_destino')

    usuario = Usuario.query.filter_by(username='diego').first()

    if not usuario:
        flash("Erro: Usuário 'diego' não encontrado.", 'danger')
        return redirect(url_for('admin_page'))
    
    if not titulo_form or not url_form:
        flash("Erro: Título e URL são obrigatórios.", "danger")
        return redirect(url_for('admin_page'))
    
    novo_link = Link(
        titulo=titulo_form,
        url_destino=url_form,
        usuario=usuario
    )

    db.session.add(novo_link)
    db.session.commit()

    flash("Link adicionado com sucesso!", "success")

    return redirect(url_for('admin_page'))

@app.route('/admin/delete/<int:link_id>')
def delete_link(link_id):
    link = Link.query.get(link_id)

    if link:
        db.session.delete(link)
        db.session.commit()
        flash("Link removido.", "success")
    
    else:
        flash("Link não encontrado.", "danger")

    return redirect(url_for('admin_page'))

@app.route('/<string:username>')
def pagina_perfil(username):
    usuario = Usuario.query.filter_by(username=username).first()

    if not usuario:
        return "Usuario não encontrado"
    
    return render_template('perfil.html', usuario=usuario)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)