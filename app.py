from flask import Flask, render_template, request, flash, send_file
import sqlite3
from form_validation import IsiAbsen as FormIsiAbsen
import csv

# Menggunakan Flask Web Development Framework
# http://flask.pocoo.org/

# Menggunakan Sqlite3
# https://docs.python.org/3/library/sqlite3.html

# Menggunakan CSV
# https://docs.python.org/3/library/csv.html

# Menggunakan wtforms untuk form validation
# https://wtforms.readthedocs.io/en/stable/

# Inisiasi Framework FLASK
app = Flask(__name__)
app.secret_key = 'secret123'


# SQLite3 config
# Membuat koneksi DB
db = sqlite3.connect('absensi.db', check_same_thread=False)

# Inisiasi Kursor
c = db.cursor()

# Cek / Membuat Table
c.execute("CREATE TABLE IF NOT EXISTS absensi(npk text, nama text)")

# Save Data perubahan
db.commit()

# Close Cursor
c.close()


@app.route('/')  # Routing Home
def home():
    return render_template('home.html')


@app.route('/isi-absen', methods=['GET', 'POST'])
def isi_absen():

    form = FormIsiAbsen(request.form)
    if request.method == 'POST' and form.validate():
        npk = form.npk.data
        nama = form.nama.data

        c = db.cursor()
        c.execute("SELECT * FROM absensi WHERE npk=?", (npk,))
        is_npk_same = c.fetchone()
        c.close()

        if is_npk_same:
            flash('Gagal absen, NPK sudah dalam list!', 'danger')
        else:
            c = db.cursor()
            c.execute("insert into absensi values (?,?)", (npk, nama))
            db.commit()
            c.close()

            flash('Sukses melakukan absen!', 'success')

        return render_template('isi_absen.html', form=form)
    return render_template('isi_absen.html', form=form)


@app.route('/list-absen')
def list_absen():
    c = db.cursor()
    c.execute("SELECT * FROM absensi")
    data = c.fetchall()
    c.close()

    return render_template('list_absen.html', listAbsen=data, deleteData=delete_absen)


@app.route('/delete-absen', methods=['GET'])
def delete_absen():
    npk = request.args.get('npk')
    c = db.cursor()
    c.execute("DELETE FROM absensi WHERE npk=?", (npk,))
    db.commit()
    c.close()
    flash('Sukses Delete absen!', 'success')

    return 'success'


@app.route('/download-csv', methods=['GET'])
def get_csv():
    c = db.cursor()
    c.execute("SELECT * FROM absensi")
    dataAbsensi = c.fetchall()

    with open('list-absensi.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(['NPK', 'Nama Lengkap'])
        for absen in dataAbsensi:
            writer.writerow(absen)

    return send_file('list-absensi.csv', mimetype='text/csv', attachment_filename='list-absensi.csv', as_attachment=True)


app.run()
