# 📁 Simplified File-Sharing Web Application on AWS 🚀

A lightweight, user-friendly file-sharing web application built with **Flask**, hosted on **AWS EC2**, and backed by **Amazon S3** for secure file storage. Users can upload and download files through a clean web interface from anywhere in the world 🌍.

---

## 🛠️ Tech Stack & AWS Services Used

| Component         | Technology        |
|------------------|-------------------|
| Frontend         | HTML + CSS        |
| Backend          | Flask (Python)    |
| File Storage     | Amazon S3 🪣      |
| Hosting          | EC2 Instance 🖥️    |
| Permissions      | IAM Roles 🔐       |
| Networking       | VPC + Security Groups 🌐 |

---

## 🌱 Project Stages

### 1. ✅ Planning & Setup
- Defined project scope and team roles.
- Created AWS Free Tier account and configured billing alerts.

### 2. 🧱 Infrastructure Setup
- Created and configured an S3 bucket with secure permissions.
- Launched EC2 instance and attached IAM Role for S3 access.
- Set up security groups to allow HTTP and SSH traffic.

### 3. 💻 Web App Development
- Built a Flask app to handle file uploads/downloads.
- Connected the app to S3 using Boto3.
- Displayed download links after successful uploads.

### 4. 🌐 Deployment
- Installed dependencies using a User Data script on EC2.
- Auto-cloned the app from GitHub and ran it with `nohup`.
- Made the app publicly accessible via EC2 public IP.

### 5. 📸 Testing & Documentation
- Tested end-to-end uploads/downloads.
- Captured screenshots of AWS components and UI.

---

## 🧗‍♂️ Challenges Faced & How We Solved Them

| Challenge | Solution |
|----------|----------|
| ❌ IAM role creation blocked in Sandbox | Used AWS credentials directly in the Flask app via `aws configure`. |
| ❌ Flask ran on port 5000 instead of 80 | Avoided `flask run` and used `python3 app.py` with `host='0.0.0.0', port=80`. |
| ❌ Files not appearing in S3 | Verified IAM policy permissions and bucket CORS settings. |
| ❌ Flask stopped after EC2 reboot | Used `nohup` to keep the app running in background after launch. |
| ❌ Bucket name already exists | Used a random generator to create 63-character globally unique bucket names. |

---

## 📸 Screenshots

> Replace with your own images:
- ✅ EC2 Instance
- ✅ S3 Bucket
- ✅ Flask App UI
- ✅ Upload + Download demo

---

## ▶️ How to Run the App

### 🌐 Accessing the App
Visit:  
18.208.253.141


### 📥 Upload a File
- Choose a `.pdf`, `.jpg`, `.png`, `.txt`, etc.
- Get a downloadable link right after.

---

## 🌟 Bonus Features Implemented
- ✅ File list view (S3 object listing in UI)
- ✅ UI improvements with HTML/CSS

---

## 📚 License

MIT License. For educational purposes only.

---

## 🙌 Team & Acknowledgements

- Special thanks to our team members.
- Built as part of a college cloud computing project.

---
