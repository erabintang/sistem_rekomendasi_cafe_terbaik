from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Cafe, User, Ulasan, Kriteria
from flask import request, render_template, redirect, url_for, flash
@app.route('/')
def home():
    cafes = Cafe.query.all()
    hasil = []

    for cafe in cafes:
        ulasan_list = cafe.ulasan
        total_nilai = sum([u.nilai for u in ulasan_list])
        skor = total_nilai / len(ulasan_list) if ulasan_list else 0

        hasil.append({
            'id': cafe.id,
            'nama': cafe.nama,
            'lokasi': cafe.lokasi,
            'skor': skor
        })

    hasil = sorted(hasil, key=lambda x: x['skor'], reverse=True)

    return render_template('home.html', cafes=hasil)

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query or query.strip() == "":
        flash("Masukkan kata kunci pencarian.")
        return redirect(url_for('cafes'))

    cafes = Cafe.query.all()
    hasil = [cafe for cafe in cafes if query.lower() in cafe.nama.lower()]

    if not hasil:
        flash(f'Tidak ditemukan cafe dengan nama "{query}".')

    return render_template('search_result.html', cafes=hasil, query=query)


@app.route('/cafes')
def cafes():
    cafes = Cafe.query.all()
    return render_template('cafes.html', cafes=cafes)

@app.route('/cafes/tambah', methods=['POST'])
def tambah_cafe():
    nama = request.form['nama']
    lokasi = request.form['lokasi']
    cafe = Cafe(nama=nama, lokasi=lokasi)
    db.session.add(cafe)
    db.session.commit()
    return redirect(url_for('cafes'))

@app.route('/cafes/edit/<int:id>', methods=['POST'])
def edit_cafe(id):
    cafe = Cafe.query.get_or_404(id)
    cafe.nama = request.form['nama']
    cafe.lokasi = request.form['lokasi']
    db.session.commit()
    return redirect(url_for('cafes'))

@app.route('/cafes/hapus/<int:id>')
def hapus_cafe(id):
    cafe = Cafe.query.get_or_404(id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('cafes'))

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/tambah', methods=['POST'])
def tambah_user():
    nama = request.form['nama']
    user = User(nama=nama)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users'))

@app.route('/users/edit/<int:id>', methods=['POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    user.nama = request.form['nama']
    db.session.commit()
    return redirect(url_for('users'))

@app.route('/users/hapus/<int:id>')
def hapus_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))

@app.route('/reviews')
def reviews():
    all_reviews = Ulasan.query.all()
    users = User.query.all()
    cafes = Cafe.query.all()
    kriteria = Kriteria.query.all()
    return render_template('reviews.html', reviews=all_reviews, users=users, cafes=cafes, kriteria=kriteria)


@app.route('/reviews/tambah', methods=['POST'])
def tambah_ulasan():
    isi = request.form['isi']
    nilai = float(request.form['nilai'])
    cafe_id = int(request.form['cafe_id'])
    user_id = int(request.form['user_id'])
    kriteria_id = int(request.form['kriteria_id'])  # ✅ ambil dari form

    ulasan = Ulasan(isi=isi, nilai=nilai, cafe_id=cafe_id, user_id=user_id, kriteria_id=kriteria_id)
    db.session.add(ulasan)
    db.session.commit()
    return redirect(url_for('reviews'))


@app.route('/reviews/edit/<int:id>', methods=['POST'])
def edit_ulasan(id):
    ulasan = Ulasan.query.get_or_404(id)
    ulasan.isi = request.form['isi']
    ulasan.nilai = float(request.form['nilai'])
    ulasan.cafe_id = int(request.form['cafe_id'])
    ulasan.user_id = int(request.form['user_id'])
    db.session.commit()
    return redirect(url_for('reviews'))

@app.route('/reviews/hapus/<int:id>')
def hapus_ulasan(id):
    ulasan = Ulasan.query.get_or_404(id)
    db.session.delete(ulasan)
    db.session.commit()
    return redirect(url_for('reviews'))

@app.route('/kriteria')
def kriteria():
    kriteria = Kriteria.query.all()
    return render_template('kriteria.html', kriteria=kriteria)

@app.route('/kriteria/tambah', methods=['POST'])
def tambah_kriteria():
    nama = request.form['nama']
    bobot = float(request.form['bobot'])
    tipe = request.form['tipe']
    kriteria = Kriteria(nama=nama, bobot=bobot, tipe=tipe)
    db.session.add(kriteria)
    db.session.commit()
    return redirect(url_for('kriteria'))

@app.route('/kriteria/edit/<int:id>', methods=['POST'])
def edit_kriteria(id):
    kriteria = Kriteria.query.get_or_404(id)
    kriteria.nama = request.form['nama']
    kriteria.bobot = float(request.form['bobot'])
    kriteria.tipe = request.form['tipe']
    db.session.commit()
    return redirect(url_for('kriteria'))

@app.route('/kriteria/hapus/<int:id>')
def hapus_kriteria(id):
    kriteria = Kriteria.query.get_or_404(id)
    db.session.delete(kriteria)
    db.session.commit()
    return redirect(url_for('kriteria'))

@app.route('/saw', methods=['GET', 'POST'])
def saw():
    cafes = Cafe.query.all()
    kriteria = Kriteria.query.all()

    if request.method == 'POST':
        # ambil nilai dari form dan proses SAW
        # simpan ke variabel hasil_saw
        hasil_saw = []  # nanti diisi hasil ranking

        return render_template('saw.html', cafes=cafes, kriteria=kriteria, hasil=hasil_saw)

    return render_template('saw.html', cafes=cafes, kriteria=kriteria)

@app.route('/hasil')
def hasil():
    cafes = Cafe.query.all()
    kriteria = Kriteria.query.all()
    
    # Ambil nilai ulasan per cafe per kriteria
    matrix = {}  # { cafe.id: {kriteria.id: nilai} }
    for c in cafes:
        matrix[c.id] = {}
        for k in kriteria:
            ulasan = Ulasan.query.filter_by(cafe_id=c.id, kriteria_id=k.id).first()
            matrix[c.id][k.id] = ulasan.nilai if ulasan else 0

    # Normalisasi dan hitung skor
    hasil_saw = []
    for c in cafes:
        norm = []
        skor = 0
        for k in kriteria:
            kolom = [matrix[x.id][k.id] for x in cafes]
            nilai = matrix[c.id][k.id]
            if k.tipe == 'benefit':
                normal = nilai / max(kolom) if max(kolom) != 0 else 0
            else:
                normal = min(kolom) / nilai if nilai != 0 else 0
            norm.append(normal)
            skor += normal * k.bobot
        hasil_saw.append({
            'nama': c.nama,
            'normalisasi': norm,
            'skor': skor
        })

    hasil_saw = sorted(hasil_saw, key=lambda x: x['skor'], reverse=True)

    return render_template('hasil.html', hasil=hasil_saw, kriteria=kriteria)
