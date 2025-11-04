# 🌾 Project Samarth — Data-Driven Q&A System

### 🔍 Overview
**Project Samarth** is an interactive **data analytics and question-answering system** built to query and visualize insights from **Indian government datasets**, including rainfall patterns and crop production trends.  
It allows users to ask natural-language questions (like *“Compare rainfall in Maharashtra and Gujarat for the last 10 years”*) and get structured, data-backed answers with charts and tables.

---

### ⚙️ Features
- 💬 Natural-language question parsing using a lightweight intent planner  
- 🌧 Integration of **IMD rainfall** and **district-level crop production** datasets  
- 🧹 Automated **data normalization** and **state/crop mapping**  
- 🧠 SQLAlchemy-powered **SQLite database** backend for structured analysis  
- 📊 Interactive dashboard built with **Streamlit** for data visualization  
- 🔗 Extensible pipeline for adding new datasets or queries  

---

### 🧩 Tech Stack
- **Language:** Python  
- **Libraries:** Pandas, SQLAlchemy, FuzzyWuzzy, Streamlit  
- **Database:** SQLite  
- **Data Sources:** [data.gov.in](https://data.gov.in) APIs and local CSV datasets  

---

### 🏗️ Project Structure
```
project-samarth/
│
├── data/                   # Raw datasets (rainfall & crop)
├── maps/                   # Mapping files (state_map.csv, crop_map.csv)
├── scr/
│   ├── fetch_data.py       # Downloads/loads datasets
│   ├── normalize.py        # Normalizes and ingests datasets into SQLite
│   ├── db.py               # Database setup and helpers
│   ├── planner.py          # Parses natural-language queries
│   ├── analysis.py         # Performs rainfall and crop trend analysis
│   └── app.py              # Streamlit Q&A interface
│
└── project.db              # SQLite database (auto-created)
```

---

### 🚀 How to Run
#### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/project-samarth.git
cd project-samarth
```

#### 2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # on Windows
source venv/bin/activate  # on Mac/Linux
```

#### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

#### 4️⃣ Load datasets
You can either:
- Use your **local CSVs** (`data/imd_rainfall.csv`, `data/crop_district.csv`), or  
- Fetch from [data.gov.in](https://data.gov.in) using:
  ```bash
  python scr/fetch_data.py
  ```

#### 5️⃣ Normalize and ingest data
```bash
python scr/normalize.py
```

#### 6️⃣ Launch the Q&A web app
```bash
streamlit run scr/app.py
```

---

### 💡 Example Questions
Try these queries in the Streamlit app:
- *Compare rainfall in Maharashtra and Gujarat for the last 10 years*  
- *Identify the district in Tamil Nadu with the highest rice production in the most recent year*  
- *Analyze the trend of wheat production in Uttar Pradesh over the past 5 years*

---

### 🧠 Project Summary for Resume
> **Project Samarth — Data-Driven Q&A System**  
> Built an interactive data analysis platform enabling natural-language queries over government rainfall and crop production datasets.  
> **Tech:** Python, Pandas, SQLAlchemy, Streamlit, FuzzyWuzzy, SQLite

---

### 👨‍💻 Author
**[Your Name]**  
📧 [your.email@example.com]  
🌐 [https://github.com/your-username](https://github.com/your-username)
