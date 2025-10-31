from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario' 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    nome_de_exibicao = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    password_hash = db.Column(db.String(256), nullable=True)
    links = db.relationship('Link', backref='usuario', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.username}>'
    
class Link(db.Model):
    __tablename__ = 'link'

    id = db.Column(db.Integer, primary_key=True)
    titulo= db.Column(db.String(100), nullable=False,)
    url_destino = db.Column(db.String(500), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f'<Link {self.titulo} para {self.url_destino}>'