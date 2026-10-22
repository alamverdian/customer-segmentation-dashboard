# 📊 LRFM Customer Segmentation Dashboard

An interactive end-to-end web dashboard engineered to transform customer transaction data into actionable business insights. This project utilizes the **LRFM (Length, Recency, Frequency, Monetary)** model and **Fuzzy C-Means (FCM) Clustering** to segment customers into 3 strategic groups: *Champions, Potential Loyalists, and Hibernating/Churn*.

🚀 **Live Demo:** [Insert your Streamlit live link here]

---

## 🛠️ Tech Stack & Libraries
- **Dashboard Framework:** Streamlit
- **Data Visualization:** Plotly Express
- **Data Preprocessing & Processing:** Pandas, OpenPyXL
- **Language:** Python 3.x

---

## ✨ Features
- **Dynamic Filtering:** Responsive sidebar selection to filter complete customer metrics instantly.
- **Real-Time KPI Metrics:** Live tracking of Total Customers, Total Revenue, and Average Purchase Frequency.
- **Interactive Visualizations:** Responsive Plotly charts (Bar Charts & Scatter Plots) equipped with hover data context.
- **Searchable Data Table:** Interactive customer breakdown view with automatic sorting and data preview capabilities.

---

## 📁 Repository Structure
```text
├── app.py                            # Main Streamlit application code
├── customer_segmentation_data.csv    # Segmented customer dataset
└── README.md                         # Project documentation
```

## ⚙️ Local Installation & Setup

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com
   ```
2. Navigate into the project folder:
   ```bash
   cd your-repo-name
   ```
3. Install the required dependencies:
   ```bash
   pip install streamlit pandas plotly openpyxl
   ```
4. Run the application:
   ```bash
   python -m streamlit run app.py
   ```
