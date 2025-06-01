# PM4_Lyrics
Analysing of this dataset: https://www.kaggle.com/datasets/carlosgdcj/genius-song-lyrics-with-language-information

# 🎶 Genius Lyrics NLP Project

This project performs natural language processing on song lyrics using a dataset from Genius. It includes sentiment analysis, data cleaning, and an interactive visualization via a web app.

---

## 🚀 How to Run This Project

Follow these steps to reproduce the full pipeline from data to interactive app:

### 1. 📥 Download the Dataset
- Go to [Kaggle](https://www.kaggle.com/) and download the Genius lyrics dataset.
- Extract or convert the file into a suitable format `.csv`.

### 2. 🗃️ Import Data into MongoDB
- Start your local MongoDB server (e.g. with `mongod`).
- Import the dataset into MongoDB using MongoDB Compass or the CLI.

#### ✅ Use the following database and collection names:
- **Database**: `data`  
- **Collection**: `Genius`

### 3. Run the sentiment.ipynb file
- Run the sentiment.ipynb file step by step which is in the "Coding" folder

### 4. Run the App
- Run the app.py file and enjoy analysing the lyrics
