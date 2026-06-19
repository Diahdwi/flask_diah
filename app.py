from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model dan scaler yang sudah ditraining
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Mengambil input data dari form HTML
        pregnancies = float(request.form['Pregnancies'])
        glucose = float(request.form['Glucose'])
        blood_pressure = float(request.form['BloodPressure'])
        skin_thickness = float(request.form['SkinThickness'])
        insulin = float(request.form['Insulin'])
        bmi = float(request.form['BMI'])
        dpf = float(request.form['DiabetesPedigreeFunction'])
        age = float(request.form['Age'])
        
        # Mengubah data menjadi bentuk DataFrame
        data = pd.DataFrame({
            'Pregnancies': [pregnancies],
            'Glucose': [glucose],
            'BloodPressure': [blood_pressure],
            'SkinThickness': [skin_thickness],
            'Insulin': [insulin],
            'BMI': [bmi],
            'DiabetesPedigreeFunction': [dpf],
            'Age': [age]
        })
        
        # PENTING: Jika menggunakan scaler pada saat training, 
        # maka data baru juga harus ditransformasi menggunakan scaler
        data_scaled = scaler.transform(data)
        
        # Memprediksi hasil (1 = Diabetic, 0 = Non-Diabetic)
        prediction = model.predict(data_scaled)
        
        # Mengubah format hasil array numerik menjadi teks
        if prediction[0] == 1:
            hasil = "Diabetic"
        else:
            hasil = "Non-Diabetic"
            
        return render_template('index.html', prediction=hasil)

if __name__ == '__main__':
    app.run(debug=True)