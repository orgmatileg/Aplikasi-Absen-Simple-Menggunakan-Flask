from wtforms import Form, StringField, validators


class IsiAbsen(Form):
    nama = StringField('Nama', [validators.Required(message='Nama wajib di isi'), validators.Length(
        min=2, max=50, message='Nama minimal 2 karakter dan maksimal 50 karakter')], description='Masukkan Nama Anda')

    npk = StringField('NPK', [validators.Required(message='NPK wajib di isi'), validators.Length(
        min=15, max=16, message='NPK minimal 15 karakter dan maksimal 16 karakter'), validators.regexp('^[0-9]*$', message='Inputan Harus berupa angka saja')], description='Masukkan NPK Anda')
