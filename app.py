import os 
from flask import Flask, render_template, redirect, url_for, request, flash
from dotenv import load_dotenv
from models import db, Usuario, Link
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

load_dotenv()

app = Flask(__name__)

db_url = os.getenv('DATABASE_URL')
if not db_url:
    raise ValueError("DATABASE_URL não está configurado no arquivo .env")

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login_page'
login_manager.login_message = 'Você precisa estr logado para acessar esta página.'
login_manager.login_message_category = 'danger'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('admin_page'))

    if request.method == 'POST':
        username_form = request.form.get('username')
        password_form = request.form.get('password')

        usuario = Usuario.query.filter_by(username=username_form).first()

        if usuario and usuario.check_password(password_form):
            login_user(usuario)
            return redirect(url_for('admin_page'))
        else:
            flash('Usuario ou senha inválidos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('Você foi desconectado.', 'sucess')
    return redirect(url_for('login_page'))

@app.route('/admin')
@login_required
def admin_page():
    usuario = current_user
    return render_template('admin.html', usuario=usuario)

@app.route('/admin/add', methods=['POST'])
@login_required
def add_link():
    titulo_form = request.form.get('titulo')
    url_form = request.form.get('url_destino')

    usuario = current_user

    if not titulo_form or not url_form:
        flash("Erro: Título e URL são obrigatórios.", "danger")
        return redirect(url_for('admin_page'))
    
    novo_link = Link(
        titulo=titulo_form,
        url_destino=url_form,
        usuario_id=usuario.id
    )

    db.session.add(novo_link)
    db.session.commit()

    flash("Link adicionado com sucesso!", "success")

    return redirect(url_for('admin_page'))

@app.route('/admin/delete/<int:link_id>')
@login_required
def delete_link(link_id):
    link = Link.query.get(link_id)

    if link and link.usuario_id == current_user.id:
        db.session.delete(link)
        db.session.commit()
        flash("Link removido.", "success")
    elif not link:
        flash("Link não encontrado.", "danger")
    else:
        flash("Acesso não autorizado", "danger")

    return redirect(url_for('admin_page'))

@app.route('/admin/edit/<int:link_id>')
@login_required
def edit_link(link_id):
    link = Link.query.get_or_404(link_id)

    if link.usuario_id != current_user.id:
        flash("Acesso não autorizado.", "danger")
        return redirect(url_for('admin_page'))
    
    return render_template('edit_link.html', link=link)

@app.route('/admin/update/<int:link_id>', methods=['POST'])
@login_required
def update_link(link_id):
    link_to_update = Link.query.get_or_404(link_id)
    
    if link_to_update.usuario_id != current_user.id:
        flash("Acesso não autorizado.", "danger")
        return redirect(url_for('admin_page'))

    novo_titulo = request.form.get('titulo')
    nova_url = request.form.get('url_destino')

    link_to_update.titulo = novo_titulo
    link_to_update.url_destino = nova_url
    db.session.commit()

    flash('Link atualizado com sucesso!', "success")
    return redirect(url_for('admin_page'))

@app.route('/')
def index():
    return "Olá, mundo"

@app.route('/<string:username>')
def pagina_perfil(username):
    usuario = Usuario.query.filter_by(username=username).first()

    if not usuario:
        return "Usuario não encontrado", 404
    
    return render_template('perfil.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)