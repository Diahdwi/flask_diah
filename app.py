from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model (yang isinya LIST berisi 2 model) dan scaler
with open('model.pkl', 'rb') as f:
    models_list = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # 1. Ambil nama model dari dropdown HTML ('Decision Tree' atau 'SVC')
            selected_model_name = request.form['model']
            
            # 2. Ambil data input dari form HTML
            pregnancies = float(request.form['Pregnancies'])
            glucose = float(request.form['Glucose'])
            blood_pressure = float(request.form['BloodPressure'])
            skin_thickness = float(request.form['SkinThickness'])
            insulin = float(request.form['Insulin'])
            bmi = float(request.form['BMI'])
            dpf = float(request.form['DiabetesPedigreeFunction'])
            age = float(request.form['Age'])

            # 3. Ubah inputan menjadi DataFrame
            # Menggunakan nama 'Pregnancy' (Tunggal) sesuai dengan cols saat training data Anda
            data = pd.DataFrame({
                'Pregnancy': [pregnancies],
                'Glucose': [glucose],
                'BloodPressure': [blood_pressure],
                'SkinThickness': [skin_thickness],
                'Insulin': [insulin],
                'BMI': [bmi],
                'DiabetesPedigreeFunction': [dpf],
                'Age': [age]
            })

            # 4. Lakukan transformasi data menggunakan scaler
            data_scaled = scaler.transform(data)

            # 5. PILIH MODEL DARI LIST BERDASARKAN INPUT DROPDOWN
            # Di kode training kamu: indeks 0 = Decision Tree, indeks 1 = SVC
            if selected_model_name == 'Decision Tree':
                chosen_model = models_list[0]
            elif selected_model_name == 'SVC':
                chosen_model = models_list[1]
            else:
                # Jaga-jaga jika ada pilihan lain (seperti Random Forest di form Anda) namun belum di-train
                chosen_model = models_list[0] 

            # 6. Lakukan prediksi menggunakan model yang sudah dipilih dari list
            prediction = chosen_model.predict(data_scaled)

            # 7. Konversi hasil prediksi ke teks
            if prediction[0] == 1:
                hasil = "Diabetic"
            else:
                hasil = "Non-Diabetic"

            # Kembalikan hasil prediksi ke halaman web
            return render_template('index.html', prediction=hasil)
            
        except Exception as e:
            # Menampilkan error agar mudah didebug jika ada kesalahan lain
            return render_template('index.html', prediction=f"Error saat komputasi: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
