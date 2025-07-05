from app import db

class Cafe(db.Model):
    __tablename__ = 'cafes'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    lokasi = db.Column(db.String(200), nullable=False)
    ulasan = db.relationship('Ulasan', backref='cafe', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    ulasan = db.relationship('Ulasan', backref='user', lazy=True)

class Kriteria(db.Model):
    __tablename__ = 'kriteria'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    bobot = db.Column(db.Float, nullable=False)
    tipe = db.Column(db.String(10), nullable=False)  # 'benefit' atau 'cost'
    ulasan = db.relationship('Ulasan', backref='kriteria', lazy=True)

class Ulasan(db.Model):
    __tablename__ = 'ulasan'
    id = db.Column(db.Integer, primary_key=True)
    isi = db.Column(db.Text, nullable=True)
    nilai = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cafe_id = db.Column(db.Integer, db.ForeignKey('cafes.id'), nullable=False)
    kriteria_id = db.Column(db.Integer, db.ForeignKey('kriteria.id'), nullable=False)
