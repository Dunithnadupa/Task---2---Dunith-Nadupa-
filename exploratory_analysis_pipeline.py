import os
import pandas as pd
import numpy as np

def run_exploratory_analysis(input_path):
    print("🚀 Initializing Exploratory Data Analysis (EDA) Pipeline...")
    
    # Verify dataset existence
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Source file not found at: {input_path}")
        
    # Load dataset
    df = pd.read_excel(input_path)
    print(f"📥 Dataset loaded. Total Records: {df.shape[0]}, Fields: {df.shape[1]}")
    
    # ----------------------------------------------------
    # STEP 1: Five-Number Summary & Skewness
    # ----------------------------------------------------
    print("\n📊 Step 1: Computing Core Descriptive Statistics...")
    numeric_fields = ['Quantity', 'UnitPrice', 'ItemsInCart', 'TotalPrice']
    
    summary_df = df[numeric_fields].describe()
    # Append skewness to the summary matrix
    skewness = df[numeric_fields].skew().to_frame().T
    skewness.index = ['skew']
    summary_complete = pd.concat([summary_df, skewness])
    
    print(summary_complete.round(2))
    
    # Highlight Median vs Mean for TotalPrice
    mean_tp = df['TotalPrice'].mean()
    median_tp = df['TotalPrice'].median()
    skew_tp = df['TotalPrice'].skew()
    print(f"   [Observation] TotalPrice Mean: ${mean_tp:.2f} | Median: ${median_tp:.2f} | Skewness: {skew_tp:+.2f}")
    
    # ----------------------------------------------------
    # STEP 2: Outlier Forensics (IQR vs Z-Score)
    # ----------------------------------------------------
    print("\n🔍 Step 2: Running Outlier Detection Frameworks...")
    
    # IQR Method
    Q1 = df['TotalPrice'].quantile(0.25)
    Q3 = df['TotalPrice'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + (1.5 * IQR)
    
    iqr_outliers = df[df['TotalPrice'] > upper_bound]
    print(f"   - IQR Method Upper Bound: ${upper_bound:.2f}")
    print(f"   - IQR Outliers Detected: {iqr_outliers.shape[0]} records")
    
    # Z-Score Method
    tp_mean = df['TotalPrice'].mean()
    tp_std = df['TotalPrice'].std()
    df['Z_Score'] = (df['TotalPrice'] - tp_mean) / tp_std
    z_outliers = df[df['Z_Score'].abs() > 3]
    print(f"   - Z-Score Method (|Z| > 3) Outliers Detected: {z_outliers.shape[0]} records")
    
    if not iqr_outliers.empty:
        print("   - Sample of High-Leverage VIP/Wholesale Signal Rows:")
        print(iqr_outliers[['OrderID', 'Quantity', 'UnitPrice', 'TotalPrice']].head(3).to_string(index=False))

    # ----------------------------------------------------
    # STEP 3: Operational Headline & Revenue Drain
    # ----------------------------------------------------
    print("\n🚨 Step 3: Analyzing Operational Leakage (OrderStatus)...")
    status_counts = df['OrderStatus'].value_counts()
    status_pcts = df['OrderStatus'].value_counts(normalize=True) * 100
    
    status_summary = pd.DataFrame({'Count': status_counts, 'Percentage (%)': status_pcts})
    print(status_summary.round(2))
    
    # Calculate Frozen/Unrealized Revenue
    leaked_statuses = ['Cancelled', 'Returned']
    leaked_df = df[df['OrderStatus'].isin(leaked_statuses)]
    total_gross_rev = df['TotalPrice'].sum()
    unrealized_rev = leaked_df['TotalPrice'].sum()
    drain_percentage = (unrealized_rev / total_gross_rev) * 100
    
    print(f"   - Gross Recorded Enterprise Revenue: ${total_gross_rev:,.2f}")
    print(f"   - Total Frozen/Unrealized Revenue (Cancelled + Returned): ${unrealized_rev:,.2f}")
    print(f"   - Capital Drain Rate: {drain_percentage:.1f}%")
    
    # ----------------------------------------------------
    # STEP 4: Correlation Matrix
    # ----------------------------------------------------
    print("\n🗺️ Step 4: Generating Quantitative Pearson Correlation Coefficients...")
    corr_matrix = df[numeric_fields].corr(method='pearson')
    print(corr_matrix.round(2))
    
    print("\n🎉 EDA Pipeline executed successfully.")

if __name__ == "__main__":
    # Point directly to your validated Excel data file layout path
    DATA_PATH = os.path.join("data", "Dataset for Data Analytics.xlsx")
    run_exploratory_analysis(DATA_PATH)
