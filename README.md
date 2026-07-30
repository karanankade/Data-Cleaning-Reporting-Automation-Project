# 🧹 Data Cleaning & Reporting Automation Project

An automated **ETL (Extract, Transform, Load)** pipeline built with Python and Pandas that ingests messy sales data, cleans and standardizes it, computes Key Performance Indicators (KPIs), generates visual analytics, and produces multi-sheet Excel reports.

---

## 📌 Features

- **Messy Data Generator (`generate_data.py`)**:
  - Generates realistic raw datasets containing intentional data quality defects:
    - Missing values (quantity, price, city).
    - Inconsistent text formatting (mixed casing, leading/trailing whitespace).
    - Corrupted or non-standard date strings (`YYYY-MM-DD`, `DD/MM/YYYY`, invalid strings).
    - Duplicate rows.
- **Automated Data Cleaning Pipeline (`data_pipeline.py`)**:
  - **Imputation**: Fills missing numerical values with medians and categorical missing values with modes.
  - **Deduplication**: Automatically identifies and removes duplicate records.
  - **Text Normalization**: Strips extra whitespace and standardizes city/product text formatting to Title Case.
  - **Date Parsing & Filtering**: Coerces dates to consistent datetime formats and drops unparseable records.
  - **Feature Engineering**: Calculates total `Revenue` (`Quantity` * `Price`) and extract period `Month`.
- **Automated Reporting & Visualization**:
  - Computes core KPIs: Total Revenue, Total Order Count, and Top Performing Product.
  - Exports a monthly revenue trend bar chart (`monthly_sales.png`).
  - Generates an Excel workbook (`Automated_Report.xlsx`) with separate formatted sheets for **Cleaned Data** and **Monthly Summary**.

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Data Wrangling**: `pandas`, `numpy`
- **Visualization**: `matplotlib`
- **Excel Automation**: `xlsxwriter` / `openpyxl`

---

## 📁 Directory Structure

```text
Data Cleaning & Reporting Automation Project/
├── generate_data.py        # Script to create raw_sales_data.csv with data quality issues
├── data_pipeline.py        # Full ETL pipeline (Load, Clean, Analyze, Export)
├── raw_sales_data.csv      # Generated raw/messy input dataset
├── requirements.txt        # Python dependency list
├── Automated_Report.xlsx   # Output multi-sheet Excel report
├── monthly_sales.png       # Generated monthly revenue bar chart
└── README.md               # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Messy Dataset
```bash
python generate_data.py
```
*Output*: Creates `raw_sales_data.csv` with simulated data noise.

### 3. Execute the Automation Pipeline
```bash
python data_pipeline.py
```

*Pipeline Execution Steps*:
1. Loads `raw_sales_data.csv`.
2. Cleans missing values, removes duplicates, normalizes strings, and fixes dates.
3. Prints KPI summary to console:
   ```text
   --- KPI Insights ---
   Total Revenue: $XXX,XXX.XX
   Total Orders: XX
   Top Performing Product: <Product Name>
   ```
4. Saves `monthly_sales.png` chart and `Automated_Report.xlsx` workbook.

---

## 📊 Sample Pipeline Output

| Artifact | Description |
| :--- | :--- |
| **`monthly_sales.png`** | Bar graph illustrating revenue aggregated by monthly periods. |
| **`Automated_Report.xlsx`** | Sheet 1 (`Cleaned Data`): Full standardized dataset.<br>Sheet 2 (`Monthly Summary`): Aggregated monthly sales figures. |

---
