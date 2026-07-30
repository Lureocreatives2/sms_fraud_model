# 🛡️ Nigerian SMS Fraud Classifier 🇳🇬

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-blue)

> **An intelligent AI-powered SMS fraud detection system built to identify Nigerian-specific scam messages using Machine Learning and rule-based security techniques.**

---

# 📖 About The Project

The **Nigerian SMS Fraud Classifier** is an AI-powered web application developed to detect fraudulent SMS messages commonly circulated in Nigeria.

Traditional spam detection systems are primarily trained on global datasets and often fail to recognize localized scam patterns such as:

- 419 advance-fee fraud
- Political reward scams
- Fake bank notifications
- Work-from-home recruitment scams
- Messages deliberately written to bypass spam filters

This project addresses these challenges by combining **Machine Learning** with a **Rule-Based Fallback Engine**, producing a smarter and more reliable fraud detection system tailored for the Nigerian environment.

---

# 📊 Data Sourcing & Analysis

Creating an effective fraud classifier required combining multiple datasets to ensure both global coverage and Nigerian relevance.

## 1️⃣ UCI SMS Spam Collection Dataset

**Purpose**

Serves as the global baseline dataset for spam classification.

**Why it was used**

- Over **5,000 labeled SMS messages**
- Widely used benchmark dataset
- Teaches the model common spam language patterns
- Provides balanced examples of legitimate and spam messages

---

## 2️⃣ ExAIS SMS Spam Dataset

**Purpose**

Introduces Nigerian and region-specific spam examples.

**Why it was used**

Global datasets rarely contain:

- Nigerian phone numbers
- Local financial scams
- Regional expressions
- Nigerian banking terminology

This dataset improves the classifier's understanding of locally occurring fraud patterns.

---

## 3️⃣ Synthetic & Manually Curated Dataset

Some scam formats were missing from publicly available datasets.

To bridge this gap, additional labeled examples were manually created for:

- 🏛 Political reward scams
- 💰 419 advance-fee fraud
- 🏦 Fake bank account notifications
- 💼 Fake employment opportunities
- 📱 Work-from-home scams
- 🎁 Prize and reward messages

This significantly improved the model's ability to detect modern Nigerian fraud tactics.

---

## 🧹 Data Preprocessing

Raw SMS messages undergo several preprocessing stages before prediction.

### Text Cleaning

- Convert text to lowercase
- Remove unnecessary punctuation
- Normalize whitespace
- Preserve meaningful numeric information

### Custom Regex Processing

One major challenge is that scammers intentionally merge words together to avoid detection.

Example:

```text
salary60000NGNtoday
```

becomes

```text
salary 60000 NGN today
```

This custom Regex processor separates:

- Letters from numbers
- Numbers from currencies
- Joined keywords

without damaging useful information.

### Phone Number Preservation

Unlike many spam filters that remove numbers entirely, this project intentionally preserves Nigerian phone numbers because they often provide valuable fraud indicators.

---

# 🎯 The Problem

Many existing spam filters are designed using international datasets and fail to detect scams unique to Nigeria.

Examples include:

- Fake political empowerment schemes
- 419 advance-fee fraud
- Fake banking alerts
- BVN verification scams
- Work-from-home recruitment scams
- Reward collection scams

Scammers also deliberately disguise messages by joining words together, making them difficult for conventional machine learning models to recognize.

This project solves both problems through localized training data and intelligent preprocessing.

---

# ✨ Key Features

- 🧠 **Hybrid AI Architecture**
  - Machine Learning prediction
  - Rule-Based fallback engine

- 🇳🇬 **Nigerian Scam Detection**
  - Local fraud patterns
  - Regional scam vocabulary
  - Nigerian banking terminology

- 🔍 **Custom Regex Preprocessor**
  - Separates mashed words
  - Preserves important numerical values
  - Handles adversarial text

- 📞 **Nigerian Phone Number Detection**
  - Detects suspicious Nigerian mobile numbers
  - Adds another fraud signal

- 🏷 **Keyword Extraction**
  - Highlights suspicious keywords
  - Explains why a message was flagged

- 📊 **Confidence Score**
  - Displays model prediction confidence

- 🛡 **Safety Recommendations**
  - Advises users on appropriate actions

- 🌙 **Modern User Interface**
  - Dark-themed Streamlit application
  - Purple/Magenta gradient styling
  - Clean and responsive design

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python |
| Machine Learning | Scikit-Learn |
| Text Vectorization | TF-IDF Vectorizer |
| Classification Model | Logistic Regression |
| Web Framework | Streamlit |
| Data Processing | Pandas |
| Numerical Computing | NumPy |
| Text Processing | Regex (re) |

---

# 🏗 How It Works

The system follows a five-stage pipeline.

### 1️⃣ User Input

The user pastes an SMS message into the Streamlit interface.

⬇

### 2️⃣ Text Preprocessing

The application:

- Cleans the text
- Separates mashed words
- Preserves Nigerian phone numbers
- Normalizes formatting

⬇

### 3️⃣ Machine Learning Prediction

The cleaned text is transformed using:

- TF-IDF Vectorizer

and classified using:

- Logistic Regression

⬇

### 4️⃣ Rule-Based Fallback

If additional fraud indicators are detected, the system checks for:

- Nigerian phone numbers
- High-risk keywords
- Scam patterns

This improves robustness against adversarial SMS formatting.

⬇

### 5️⃣ Final Output

The application displays:

- Spam or Safe prediction
- Confidence score
- Triggered keywords
- Safety recommendations

---

# 🚀 Live Demo

### Streamlit App

🔗 https://smsfraudmodel-j3.streamlit.app/



---

### Project Demonstration Video

🎥 https://youtu.be/NcWMZ0O67To?si=Jf6XxdVRWO6AyM8v
---

# 💻 Local Installation

## Clone the repository

```bash
git clone https://github.com/your-username/nigerian-sms-fraud-classifier.git
```

```bash
cd nigerian-sms-fraud-classifier
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the application

```bash
streamlit run app.py
```

---

## Open your browser

```text
http://localhost:8501
```

---

# 📁 Project Structure

```text
Nigerian-SMS-Fraud-Classifier/
│
├── app.py
├── model.pkl
├── vectorizer.pkl
├── requirements.txt
├── README.md
├── datasets/
│   ├── uci_sms.csv
│   ├── exais_sms.csv
│   └── synthetic_sms.csv
│
├── notebooks/
│
└── assets/
```

---

# ✅ Project Deliverables

- [x] Data collection and preprocessing
- [x] Exploratory data analysis
- [x] Feature engineering
- [x] TF-IDF Vectorization
- [x] Logistic Regression classifier
- [x] Hybrid rule-based detection engine
- [x] Nigerian phone number detection
- [x] Keyword extraction module
- [x] Streamlit web application
- [x] User-friendly dark UI
- [x] Model evaluation
- [x] GitHub documentation
- [x] Project demonstration video

---

# 👨‍🎓 Fellow Information

| Item | Details |
|------|---------|
| **Project Name** | Nigerian SMS Fraud Classifier |
| **Built By** | Opeyemi Adeshina |
| **Cohort** | AI & Machine Learning NextGen Cohort |
| **Training Provider** | Teesas Education Ltd |
| **Email** | opeyemiolamide882@gmail.com |

---

# 📜 License

This project is released under the **MIT License**.

You are free to use, modify, and distribute this project for educational and research purposes.

---

# 🙏 Acknowledgements

Special thanks to:

- **Teesas Education Ltd**
- **AI & Machine Learning NextGen Cohort**
- **UCI Machine Learning Repository**
- **ExAIS SMS Spam Dataset Contributors**
- The open-source Python community

---

# ⭐ Support

If you found this project useful:

- ⭐ Star this repository
- 🍴 Fork the project
- 📢 Share it with others
- 💡 Contribute improvements

---

<div align="center">

### 🛡️ Nigerian SMS Fraud Classifier

**Built with ❤️ using Python, Scikit-Learn, and Streamlit**

**Developed by Opeyemi Adeshina**  
**AI & Machine Learning NextGen Cohort • Teesas Education Ltd • Lagos, Nigeria**

</div>
