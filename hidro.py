from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

# Inisialisasi aplikasi Flask
hidro = Flask(__name__)
CORS(hidro)

# Fungsi untuk membuat database dan tabel jika belum ada
def init_db():
    conn = sqlite3.connect('data_hidro.db')
    cursor = conn.cursor()
    
    # Membuat tabel untuk data sensor
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suhu_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idx INTEGER,
            suhu INTEGER,
            humid INTEGER,
            kecerahan INTEGER,
            timestamp TEXT
        )
    ''')
    
    # Membuat tabel untuk data bulan dan tahun
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS month_year_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month_year TEXT
        )
    ''')
    
    # Memasukkan contoh data ke dalam tabel
    cursor.execute("INSERT INTO suhu_data (idx, suhu, humid, kecerahan, timestamp) VALUES (101, 36, 36, 25, '2010-09-18 07:23:48')")
    cursor.execute("INSERT INTO suhu_data (idx, suhu, humid, kecerahan, timestamp) VALUES (226, 36, 36, 27, '2011-05-02 12:29:34')")
    cursor.execute("INSERT INTO month_year_data (month_year) VALUES ('9-2010')")
    cursor.execute("INSERT INTO month_year_data (month_year) VALUES ('5-2011')")
    
    conn.commit()
    conn.close()

# Endpoint untuk mengambil data dalam format JSON
@hidro.route('/iot_api/data', methods=['GET'])
def get_suhu_data():
    conn = sqlite3.connect('data_hidro.db')
    cursor = conn.cursor()
    
    # Ambil data suhu dari database
    cursor.execute('SELECT idx, suhu, humid, kecerahan, timestamp FROM suhu_data')
    suhu_data_rows = cursor.fetchall()
    suhu_data = {str(i): {"idx": row[0], "suhu": row[1], "humid": row[2], "kecerahan": row[3], "timestamp": row[4]} for i, row in enumerate(suhu_data_rows)}

    # Ambil data bulan dan tahun
    cursor.execute('SELECT month_year FROM month_year_data')
    month_year_rows = cursor.fetchall()
    month_year_data = {str(i): {"month_year": row[0]} for i, row in enumerate(month_year_rows)}
    
    # Buat respons JSON
    response = {
        "suhumax": 36,
        "suhumin": 23,
        "suhurata": 28.35,
        "nilai_suhu_max_humid_max": suhu_data,
        "month_year_max": month_year_data
    }
    
    conn.close()

    print(response)
    return jsonify(response)

# Inisialisasi database saat aplikasi dimulai
init_db()

if __name__ == '__main__':
    hidro.run(debug=True)
