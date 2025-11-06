# 🌍 GeoVista

GeoVista is an interactive Flask web app that lets users explore cities around the world 🌎.  
You can search for a city to view its **current weather**, see **recent searches**, and connect through a **contact form** — all in a clean, modern interface.

---

## 🚀 Live Demo
The project is live and accessible here: 
🔗 [GeoVista on Render](https://geovista-xvri.onrender.com)
---

## 🧩 Features
✅ Search any city and get real-time weather info using OpenWeather API  
✅ View recent searches stored in a local SQLite database  
✅ Interactive contact form (AJAX-style feedback without page reload)  
✅ Responsive UI with Bootstrap and Font Awesome  
✅ Modern glass-morphism design  

---

## 🛠️ Tech Stack
| Layer | Technologies Used |
|-------|--------------------|
| **Frontend** | HTML, CSS, Bootstrap, JS |
| **Backend** | Flask (Python) |
| **Database** | SQLite |
| **API** | OpenWeather API |
| **Hosting** | Render |

---

## ⚙️ Local Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/GeoVista.git

# Move into the folder
cd GeoVista

# Create a virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
