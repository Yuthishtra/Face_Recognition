# 🎯 **Gesture-Based Online Examination System**

### *Enabling paralysed & differently-abled users to write exams using head gestures*

---

## 📝 **Project Overview**

This project is an **AI-powered online MCQ examination system** where users can answer questions **without using hands, keyboard, or mouse**.

Instead, the system uses:

* **Face Mesh Tracking** (MediaPipe)
* **Nose landmark detection**
* **Head movement gestures**
* **Flask backend**
* **HTML + CSS + JavaScript UI**

This system is designed for **paralysed individuals, amputees, motor-disabled users**, or patients who cannot physically write exams.

---

## 🤖 **How It Works**

The camera tracks the user’s **nose position** using MediaPipe.

Each direction represents an answer:

| Head Movement | Detected As | Meaning  |
| ------------- | ----------- | -------- |
| Head Up       | A           | Option A |
| Head Down     | B           | Option B |
| Head Right    | C           | Option C |
| Head Left     | D           | Option D |

The user keeps the nose inside a **neutral box** and moves outside only when choosing an answer.

The gesture is sent to the Flask backend and evaluated in real-time.

---

## 🧠 **Features**

### ✨ **Accessibility Focused**

* No need for mouse, keyboard, or touch
* Ideal for paralysed patients or motor-disabled individuals
* Hands-free, hygienic, contact-less exam system

### ✨ **AI Gesture Recognition**

* Real-time face tracking (MediaPipe FaceMesh)
* Webcam-based gesture detection
* High accuracy nose landmark reading

### ✨ **Full Exam System**

* MCQ fetching from Flask
* Automatic answer recording
* Realtime scoring
* Beautiful animated UI

### ✨ **Technology Stack**

| Area              | Technology              |
| ----------------- | ----------------------- |
| Backend           | Python, Flask           |
| Gesture Detection | OpenCV, MediaPipe       |
| Frontend          | HTML, CSS, JavaScript   |
| Communication     | REST API (Flask routes) |

---

## 🗂️ **Project Structure**

```
GestureExam/
 ├── alica.py             # AI gesture detection (MediaPipe + OpenCV)
 ├── app.py               # Flask backend and API
 ├── templates/
 │     └── index.html     # Frontend UI
 └── static/
        ├── script.js     # Frontend logic
        └── style.css     # Styling
```

---

## 🧪 **How to Run the Project**

### **1️⃣ Install Dependencies**

```
pip install opencv-python mediapipe flask requests
```

### **2️⃣ Run Flask Server**

```
python app.py
```

### **3️⃣ Run Gesture System**

It will start automatically when you click **Start Test** on the webpage.
Or run manually:

```
python alica.py
```

### **4️⃣ Open Browser**

Go to:

```
http://127.0.0.1:5000
```

---

## 🎥 **Demo Video**

```


https://github.com/user-attachments/assets/3b25ea05-78d8-4ae8-acaf-9a0ed61fafd1

<img width="1535" height="830" alt="image" src="https://github.com/user-attachments/assets/e3c55f22-30cc-4ffa-8bea-917b6cbed9ac" />





## 🚀 **Future Enhancements**

* Voice feedback for visually impaired users
* Larger question banks
* Exam timer
* Cloud deployment
* Student report generation
* Blink detection for selecting answers
* Login & authentication system

---

## ❤️ **Purpose**

This project aims to support:

* Paralysed patients
* Motor disability users
* People who cannot use hands
* Bed-ridden or injured users
* Individuals needing assistive technology

Providing them the **dignity of equal education access**.

---

## 👨‍💻 **Author**

**M N Yuthishtra Bose**
Gesture-based assistive technology developer

