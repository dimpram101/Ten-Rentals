import FormLogin as fl
import FormRegister as fr
import FormRentalMobil as frm
import FormPemesanan as fp
import sys, time, random, datetime, re
from PyQt5 import QtWidgets
from VarMobil import ket_mobil, harga_mobil, tipe_waktu

global mobil_skrg
global data_user
global username
global email
data_user = []

# fungsi untuk menampilkan Message Box
def message_box(text):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("Informasi")
    msg.setText("{}".format(text))
    msg.exec_()

# fungsi untuk membaca file dan mengembalikan array
def baca_file(nama_file, list_output):
    list_output.clear()
    f = open(nama_file, 'r')
    for line in f:
        list_output.append(line.strip("\n"))
    f.close()
    for i in range(len(list_output)):
        list_output[i] = list_output[i].split(",")
    return list_output

# fungsi untuk mengembalikan nilai daftar mobil yang tersisa dalam bentuk dictionary
def baca_daftar_mobil():
    f = open('daftar_mobil.txt', 'r')
    arr = []
    daftar_mobil = {}
    key = []
    value = []
    for line in f:
        line = line.strip("\n")
        arr.append(line.split())
    for i in range(len(arr)):
        key.append(arr[i][0])
    for i in range(len(arr)):
        value.append(arr[i][1])
    for i in range(len(key)):
        daftar_mobil.update({key[i]: int(value[i])})
    return daftar_mobil

# CLASS UNTUK FORM LOGIN
class FormLogin(QtWidgets.QWidget, fl.Ui_formLogin):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.tombolLogin.clicked.connect(self.push_login_button)
        self.tombolRegister.clicked.connect(self.push_register_button)

    # fungsi untuk mengecek apakah username & password ada dalam berkas data_user.txt
    def isLoginValid(self):
        global username
        global email
        logged_in = False
        baca_file('data_user.txt', data_user)
        username = self.kolom_username.text()
        password = self.kolom_password.text()
        for i in range(len(data_user)):
            if username == data_user[i][0]:
                if password == data_user[i][1]:
                    logged_in = True
                    email = data_user[i][2]
                else:
                    email = None
                    break
        return logged_in

    # fungsi untuk berpindah ke form Rental ketika login berhasil, jika tidak maka akan login ulang
    def push_login_button(self):
        if self.isLoginValid():
            message_box('Login berhasil!')
            self.close()
            rental.show()
            pemesanan.username.setText(username)
            pemesanan.email.setText(email)
        else:
            message_box('Username/Password tidak dikenali!')
            self.kolom_username.clear()
            self.kolom_password.clear()

    # fungsi untuk membuka form Register/Pendaftaran
    def push_register_button(self):
        self.register = FormRegister()
        self.register.username.setText('')
        self.register.password.setText('')
        self.register.show()
        self.hide()

class FormRegister(QtWidgets.QWidget, fr.Ui_FormRegister):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.register_btn.clicked.connect(self.register_act)
        self.back_btn.clicked.connect(self.back_to_login)

    # fungsi yang mengembalikan nilai true jika email valid
    def isEmailValid(self, email):
        if email != None:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            return True if (re.fullmatch(regex, email)) else False
        else:
            pass

    # fungsi untuk mengecek apakah username atau email yang didaftarkan sudah ada pada data_user
    def isDataExist(self):
        data_exist = False
        email_valid = False
        reg_username = self.username.text()
        reg_password = self.password.text()
        reg_email = self.email.text()
        try:
            email_valid = self.isEmailValid(reg_email)
            if reg_username == '' or reg_password == '' or reg_email == '':
                message_box('Harap isi form yang kosong')
                data_exist = None
                pass
            else:
                baca_file('data_user.txt', data_user)
                if email_valid:
                    for i in range(len(data_user)):
                        if reg_username == data_user[i][0] or reg_email == data_user[i][2]:
                            if reg_email == data_user[i][2] or reg_username == data_user[i][0]:
                                data_exist = True
                            else:
                                break
                else:
                    message_box("Email tidak valid!")
                    pass
        except:
            message_box("Error isDataExist")
            pass
        return reg_username, reg_password, reg_email, data_exist, email_valid

    # fungsi untuk menambahkan data yang didaftarkan ke dalam data_user
    def register_act(self):
        reg_username, reg_password, reg_email, data_exist, email_valid = self.isDataExist()
        if data_exist == False:
            if email_valid:
                f = open('data_user.txt', 'a+')  # --OUTPUT
                f.write("\n")
                f.write(f"{reg_username},{reg_password},{reg_email}")
                f.close()  # ---
                message_box("Username berhasil didaftarkan!")
                self.close()
                logins.show()
            else:
                pass
        elif data_exist == None:
            pass
        else:
            message_box("USERNAME ATAU EMAIL SUDAH ADA! HARAP GUNAKAN YANG LAIN")
            self.username.clear()
            self.password.clear()
            self.email.clear()

    def back_to_login(self):
        self.close()
        logins.show()

# CLASS UNTUK FORM RENTAL
class FormRental(QtWidgets.QWidget, frm.Ui_FormRental):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.listKendaraan.currentIndexChanged.connect(self.current_car)  # manggil fungsi current_car() waktu memilih
        self.btn_kembali.clicked.connect(self.back_to_login)
        self.btn_pesan.clicked.connect(self.check_car_and_go_to_pemesanan)
        self.listKendaraan.currentIndexChanged.connect(self.current_bill)
        self.listWaktu.currentIndexChanged.connect(self.current_bill)
        self.listLamaJam.currentIndexChanged.connect(self.current_bill)
        self.listLamaHari.currentIndexChanged.connect(self.current_bill)
        self.listLamaMinggu.currentIndexChanged.connect(self.current_bill)
        self.listLamaBulan.currentIndexChanged.connect(self.current_bill)

    # kembali ke form login
    def back_to_login(self):
        self.close()
        logins.kolom_username.clear()
        logins.kolom_password.clear()
        logins.show()

    # Fungsi untuk mengambil huruf pertama setiap kata di kalimat list kendaraan dan mengembalikan nilainya
    def first_each_word(self):
        kalimat = self.listKendaraan.currentText().split()
        words = []
        first = ""
        for i in range(len(kalimat)):  # memasukkan setiap kata yang ada di kalimat ke dalam words
            words.append(kalimat[i])
        for j in range(len(words)):  # menambahkan string huruf pertama dari setiap kata yang ada dalam words
            first += words[j][0]
        if first == "PA":
            return None
        return first

    # fungsi untuk mengembalikan nilai apakah mobil masih tersedia atau tidak (ya = True)
    def isThereACar(self):
        ada_mobil = False
        daftar_mobil = baca_daftar_mobil()
        mobil_skrg = self.first_each_word()
        if mobil_skrg != None:
            if daftar_mobil[mobil_skrg] != 0:
                ada_mobil = True
            else:
                message_box("Kendaraan tidak tersedia!")
                pass
        else:
            message_box("Harap pilih kendaraan!")
        return ada_mobil

    # fungsi untuk pergi ke form pemesanan jika mobil masih tersedia
    def check_car_and_go_to_pemesanan(self):
        ada_mobil = self.isThereACar()
        if ada_mobil:
            pemesanan.nama.clear()
            pemesanan.nohp.clear()
            pemesanan.alamat.clear()
            pemesanan.show()

    # menampilkan keterangan mobil yang dipilih
    def current_info(self):
        self.boxKeterangan.clear()
        mobil_skrg = self.first_each_word()
        for i in range(len(ket_mobil)):
            if mobil_skrg in ket_mobil[i]:
                self.boxKeterangan.setPlainText(ket_mobil[i][mobil_skrg])
                break

    # menampilkan gambar mobil yang dipilih dan menyambung ke fungsi current_info ^^
    def current_car(self):
        image = self.listKendaraan.currentText()
        self.gambarMobil.setStyleSheet(f"background-image : url(./Gambar/{image}.jpg);\n"
                                       "background-repeat : no-repeat;\n"
                                       "background-position : center;\n"
                                       "\n"
                                       "border-style : solid;\n"
                                       "border-width : 2px 2px;")
        self.current_info()

    # mengembalikan nilai jenis waktu (Perjam, harian, mingguna, bulanan)
    def current_jenis_waktu(self):
        kalimat = self.listWaktu.currentText()
        jenis_waktu = kalimat[0]
        return jenis_waktu

    # mengembalikan nilai sepanjang 2 huruf
    def slice_number(self, kalimat):
        new_kalimat = kalimat[0:2]
        return new_kalimat

    # fungsi untuk mengembalikan nilai waktu peminjaman yang terlihat di combobox
    def current_waktu_peminjaman(self, bool):
        jenis_waktu = self.current_jenis_waktu()
        current_time = ""
        if jenis_waktu == 'P':
            current_time = self.listLamaJam.currentText()
        elif jenis_waktu == 'H':
            current_time = self.listLamaHari.currentText()
        elif jenis_waktu == 'M':
            current_time = self.listLamaMinggu.currentText()
        elif jenis_waktu == 'B':
            current_time = self.listLamaBulan.currentText()
        if bool:  # jika bool bernilai true maka akan mengembalikan new_current_time
            new_current_time = self.slice_number(current_time)
            return new_current_time
        return current_time

    # fungsi untuk merapikan nilai biaya
    def bill_slicer(self, price):
        arr = []
        bill = ''
        for huruf in str(price):
            arr.append(huruf)
        if len(arr) == 5:
            for i in range(len(arr)):
                bill += f"{arr[i]}"
                if i == 1:
                    bill += "."
        elif len(arr) == 6:
            for i in range(len(arr)):
                bill += f"{arr[i]}"
                if i % 3 == 2 and i != len(arr) - 1:
                    bill += "."
        elif len(arr) == 7:
            for i in range(len(arr)):
                bill += f"{arr[i]}"
                if i % 3 == 0 and i != len(arr) - 1:
                    bill += "."
        elif len(arr) == 8:
            for i in range(len(arr)):
                bill += f"{arr[i]}"
                if i % 3 == 1 and i != len(arr) - 1:
                    bill += "."
        return bill

    # fungsi untuk menampilkan biaya terkini
    def current_bill(self):
        mobil_skrg = self.first_each_word()
        jenis_waktu = self.current_jenis_waktu()
        waktu = self.current_waktu_peminjaman(True)
        try:
            if jenis_waktu in tipe_waktu:
                index = tipe_waktu[jenis_waktu]
                if mobil_skrg != None:
                    current_price = harga_mobil[str(mobil_skrg)][int(index)]
                    current_price *= int(waktu)
                    bill = self.bill_slicer(current_price)
                    self.biayaRental.setText(f"Rp{str(bill)}")
                    self.form_pemesanan_act(self.listKendaraan.currentText(), self.current_waktu_peminjaman(False),
                                            bill)
                else:
                    self.biayaRental.clear()
        except:
            message_box("Terjadi error (current_bill)")

    # fungsi untuk mengedit variabel dalam class FormPemesanan
    def form_pemesanan_act(self, jenis_mobil, lama, biaya):
        pemesanan.jenis_mobil.setText(jenis_mobil)
        pemesanan.lama_peminjaman.setText(lama)
        pemesanan.biaya.setText(f"Rp{biaya}")

class FormPemesanan(QtWidgets.QWidget, fp.Ui_formPemesanan):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.yes_button.clicked.connect(self.yes_pushed)
        self.back_button.clicked.connect(self.ke_rental)

    # Fungsi untuk mengecek apakah No.HP berupa angka
    def isNoHPNumber(self, nohp):
        is_numbers = False
        try:
            if nohp != "":
                if len(nohp) < 11:
                    message_box('Harap isikan No HP yang benar! (Min 11 angka)')
                else:
                    nohp = int(nohp)
                    is_numbers = True
        except ValueError:
            message_box("Harap isikan angka pada kolom No. HP!")
            self.nohp.clear()
        return is_numbers

    # Fungsi untuk mengecek apakah data valid semua
    def isDataValid(self):
        data_valid = True
        nama = self.nama.text()
        alamat = self.alamat.text()
        nohp = self.nohp.text()
        if nama == "" or nohp == "" or alamat == "":
            message_box("Harap isi kolom yang kosong!")
            data_valid = False
        if not self.isNoHPNumber(nohp):
            data_valid = False
        return data_valid

    # Fungsi untuk kembali ke form rental
    def ke_rental(self):
        self.close()

    # Fungsi untuk memperbaharui berkas data_peminjam dengan menambahkan baris baru
    # OUTPUT
    def write_data_peminjam(self):
        f = open('data_peminjam.txt', 'a+')
        f.write(f'''Nama            : {self.nama.text()},
Username        : {self.username.text()},
E-Mail          : {self.email.text()},
Jenis Mobil     : {self.jenis_mobil.text()},
No. HP          : {self.nohp.text()},
Alamat          : {self.alamat.text()},
Lama Peminjaman : {self.lama_peminjaman.text()},
Biaya           : {self.biaya.text()}
''')
        f.write("\n")
        f.close()

    # Fungsi untuk mencetak struk
    # OUTPUT
    def write_struct(self):
        f = open('user_struct.txt', 'w')
        f.write(f'''----------------------------------------------------
    Struct Nomor    : {random.randint(1, 38757)}/{random.randint(1, 10)}
    Nama            : {self.nama.text()}
    E-Mail          : {self.email.text()}
    Jenis Mobil     : {self.jenis_mobil.text()}
    Lama Peminjaman : {self.lama_peminjaman.text()}
    No. HP          : {self.nohp.text()}
    Alamat          : {self.alamat.text()}
    Biaya           : {self.biaya.text()}

    Ten Rentals

    {datetime.date.today()}
----------------------------------------------------''')
        f.write("\n")
        f.close()

    # Fungsi untuk mengecek apakah data valid, jika iya maka akan memperbaharui berkas dan memberhentikan program
    def yes_pushed(self):
        data_valid = self.isDataValid()
        if data_valid:
            self.write_data_peminjam()
            self.write_struct()
            message_box('''
            Pesanan kamu telah diterima!
            Harap tunjukkan struk saat tiba di kasir!''')
            self.update_daftar_mobil()
            self.close()
            time.sleep(1)
            rental.close()

    # fungsi untuk memperbaharui berapa mobil yang tersisa pada berkas daftar_mobil.txt
    # OUTPUT
    def update_daftar_mobil(self):
        daftar_mobil = baca_daftar_mobil()
        mobil_skrg = rental.first_each_word()
        daftar_mobil[mobil_skrg] -= 1
        f = open('daftar_mobil.txt', 'w')
        for key, value in daftar_mobil.items():
            f.write(f"{key} {value}\n")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    logins = FormLogin()
    rental = FormRental()
    pemesanan = FormPemesanan()
    logins.show()
    sys.exit(app.exec_())
