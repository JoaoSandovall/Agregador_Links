from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    nome_de_exibicao = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    links = db.relationship('Link', backref='usuario', lazy=True, cascade="all, delete-orphan")

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