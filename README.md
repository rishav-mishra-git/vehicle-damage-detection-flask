# 🚗 Vehicle Damage Detection and Repair Cost Estimation

## 📌 Overview

Vehicle Damage Detection and Repair Cost Estimation is an AI-powered web application that detects damages such as dents and scratches on vehicles from uploaded images and provides an estimated repair cost. The project uses a trained object detection model to automate vehicle inspection and make the damage assessment process faster and more accurate.

---

## ✨ Features

* Upload vehicle images for analysis
* Detect dents and scratches using an AI model
* Display detected damage with bounding boxes
* Estimate repair cost based on detected damage
* Simple and user-friendly web interface
* Fast inference using a cloud-hosted detection API

---

## 🛠️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### AI & Computer Vision

* Roboflow Object Detection Model
* Pillow (PIL) for image processing

### Deployment & Version Control

* GitHub
* Hugging Face Spaces (optional deployment)

---

## 📂 Project Structure

```
Vehicle-Damage-Detection/
│
├── app.py
├── requirements.txt
├── static/
│   ├── uploads/
│   └── results/
├── templates/
│   └── index.html
├── README.md
└── assets/
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Vehicle-Damage-Detection.git
```

### 2. Navigate to the project

```bash
cd Vehicle-Damage-Detection
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🚀 How It Works

1. User uploads a vehicle image.
2. Flask sends the image to the trained detection model.
3. The AI model identifies dents and scratches.
4. Bounding boxes are drawn around damaged areas.
5. Repair cost is estimated based on the detected damage.
6. The processed image and estimated cost are displayed to the user.

---

## 📷 Sample Workflow

```
Vehicle Image
      │
      ▼
Upload via Web Interface
      │
      ▼
AI Damage Detection
      │
      ▼
Bounding Box Generation
      │
      ▼
Repair Cost Estimation
      │
      ▼
Final Result Display
```

---

## 🎯 Applications

* Automobile insurance claim processing
* Vehicle inspection centers
* Car rental companies
* Used car marketplaces
* Automobile service centers

---

## 🔮 Future Enhancements

* Support for multiple damage categories
* Severity level classification
* Mobile application integration
* Real-time video damage detection
* Automatic report generation in PDF format
* Deep learning-based repair cost prediction

---

## 👨‍💻 Author

**Rishav Mishra**

* B.Tech – Computer Science & Engineering (AI & ML)
* Passionate about Artificial Intelligence, Machine Learning, and Computer Vision

---

## 📄 License

This project is developed for educational and research purposes. Feel free to fork and improve it for learning and non-commercial use.

---

## ⭐ If you found this project useful

Please consider giving the repository a **Star ⭐** and sharing your feedback.

