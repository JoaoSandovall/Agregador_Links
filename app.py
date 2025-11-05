import os 
from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from models import db, Usuario, Link
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)

db_url = os.getenv('DATABASE_URL')
if not db_url:
    raise ValueError("DATABASE_URL não está configurado no arquivo .env")

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg' }

db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login_page'
login_manager.login_message = 'Você precisa estar logado para acessar esta página.'
login_manager.login_message_category = 'danger'

def allowed_file(filename):
    return '.'in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login_page'))

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('admin_page'))
    
    if request.method == 'POST':

        username_form = request.form.get('username')
        nome_form = request.form.get('nome_de_exibicao')
        password_form = request.form.get('password')
        password_confirm_form = request.form.get('password_confirm')

        if password_form != password_confirm_form:
            flash('As senhas não conferem.', 'danger')
            return redirect(url_for('register_page'))
        
        usuario_existente = Usuario.query.filter_by(username=username_form).first()
        if usuario_existente:
            flash('Este nome de usuário já está em uso.', 'danger')
            return redirect(url_for('register_page'))

        novo_usuario = Usuario(
            username=username_form,
            nome_de_exibicao=nome_form
        )
        
        novo_usuario.set_password(password_form)

        db.session.add(novo_usuario)
        db.session.commit()

        login_user(novo_usuario)
        flash('Conta criada com sucesso! Você já está logado.', 'success')

        return redirect(url_for('admin_page'))
    return render_template('register.html')

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
    flash('Você foi desconectado.', 'success')
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

@app.route('/admin/upload', methods=['POST'])
@login_required
def upload_imagem():
    if 'imagem' not in request.files:
        flash('Nenhum arquivo enviado.', 'danger')
        return redirect(url_for('admin_page'))
    
    file = request.files['imagem']

    if file.filename == '':
        flash('Nenhum arquivo selecionado.', 'warning')
        return redirect(url_for('admin_page'))
    
    if file and allowed_file(file.filename):
        secure_name = secure_filename(file.filename)
        _ , extensao = os.path.splitext(secure_name)
        filename = str(current_user.id) + extensao

        old_pic = current_user.imagem_perfil
        if old_pic and old_pic != 'default.jpg':
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_pic))
            except FileNotFoundError:
                print(f"Arquivo antigo {old_pic} não encontrado.")

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        current_user.imagem_perfil = filename
        db.session.commit()

        flash('Foto de perfil atualizada!', 'success')
    else:
        flash('Tipo de arquivo inválido. Use apenas PNG, JPG ou JPEG.', 'danger')

    return redirect(url_for('admin_page'))

@app.route('/admin/update_profile', methods=['POST'])
@login_required
def update_profile():
    novo_nome = request.form.get('nome_de_exibicao')
    nova_bio = request.form.get('bio')

    current_user.nome_de_exibicao = novo_nome
    current_user.bio = nova_bio
    
    db.session.commit()

    flash('perfil atualizado com sucesso!', 'success')

    return redirect(url_for('admin_page'))

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

@app.route('/<string:username>')
def pagina_perfil(username):
    usuario = Usuario.query.filter_by(username=username).first()

    if not usuario:
        return "Usuario não encontrado", 404
    
    return render_template('perfil.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=False)