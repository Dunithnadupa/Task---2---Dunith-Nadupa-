# Exploratory Data Analysis (EDA): The Forensic Architecture of Enterprise Intelligence

## 📌 Project Overview
This repository contains **Project 2** of the **DecodeLabs Industrial Training Kit (Batch 2026)**. In enterprise data analytics, a dataset is a repository of digital evidence. The objective of this phase is to move beyond passive "simple reporting" and execute a rigorous diagnostic investigation—interrogating data structures, isolating distributions, cross-validating outliers, and revealing hidden transaction patterns.

Following the **IPO Framework** ($Input \rightarrow Process \rightarrow Output$), this project maps an incoming raw e-commerce order dataset into actionable business verdicts, utilizing an automated script-based architecture in **Python (pandas, NumPy, Matplotlib)** to decode transactional performance.

---

## 📊 Dataset Specifications
The analysis was performed on the verified file `Dataset for Data Analytics.xlsx` (compiled and audited directly from the preceding Project 1 integrity phase). The data encompasses **1,200 unique order-level records** spanning January 1, 2023, to June 30, 2025, distributed across **14 core analytical fields**:

| Field Name | Structural Type | Strategic Target |
| :--- | :--- | :--- |
| **OrderID** | Text (ID) | Primary key (1,200 unique records; 0% duplication rate) |
| **Date** | Date | Transaction timestamp (Range: Jan 1, 2023 – Jun 30, 2025) |
| **CustomerID** | Text (ID) | Buyer identifier (1,189 unique customer profiles) |
| **Product** | Categorical | Item classification (7 product spaces) |
| **Quantity** | Integer | Discrete units purchased per transaction (Scale: 1–5) |
| **UnitPrice** | Numeric (Decimal) | Cost per unit (Scale: \$11.39 – \$699.93) |
| **ShippingAddress**| Text | Destination vector (Identified as a low-value placeholder string) |
| **PaymentMethod** | Categorical | Financial settlement channel (5 balanced categories) |
| **OrderStatus** | Categorical | Operational fulfillment state (5 distinct tracking states) |
| **Tracking Number**| Text (ID) | Unique logistical shipment carrier identifier |
| **ItemsInCart** | Integer | Digital cart basket size at point of checkout (Scale: 1–10) |
| **CouponCode** | Categorical | Promotional code applied (3 active campaigns + un-coded records) |
| **Referral Source**| Categorical | Digital marketing attribution channel (5 acquisition vectors) |
| **TotalPrice** | Numeric (Decimal) | Financial gross total; cross-validated against ($Quantity \times UnitPrice$) |

---

## 📈 The Logic Skeleton: Five-Number Summary
Descriptive statistics were computed across all numeric data vectors to identify the underlying centers of gravity and variance profiles:

| Statistical Metric | Quantity | UnitPrice (\$) | ItemsInCart | TotalPrice (\$) |
| :--- | :---: | :---: | :---: | :---: |
| **Count** | 1,200 | 1,200 | 1,200 | 1,200 |
| **Mean** | 2.95 | 356.41 | 5.49 | 1,053.97 |
| **Median** | 3.00 | 364.21 | 5.00 | **823.62** |
| **Std. Deviation** | 1.41 | 197.18 | 2.28 | 819.86 |
| **Minimum** | 1.00 | 11.39 | 1.00 | 11.39 |
| **Q1 (25th Pct.)** | 2.00 | 186.06 | 4.00 | 410.52 |
| **Q3 (75th Pct.)** | 4.00 | 521.57 | 7.00 | 1,578.48 |
| **Maximum** | 5.00 | 699.93 | 10.00 | 3,456.40 |
| **Skewness** | **+0.03** *(Symmetric)* | **-0.03** *(Symmetric)* | **+0.00** *(Symmetric)* | **+0.89** *(Right-Skewed)* |

### 🧠 Geometry of Distribution: Mean vs. Median
While `Quantity` and `UnitPrice` follow an approximately uniform, symmetric distribution, their mathematical product—`TotalPrice`—exhibits a strong positive **right skew (+0.89)**. 

* **The Takeaway:** The gross mean (\$1,053.97) is artificially dragged upward by a high-value transaction tail. 
* **The Decision Rule:** In alignment with core financial modeling principles, the **Median (\$823.62)** must be reported to stakeholders as the true, representative "typical order value" to avoid overstating typical baseline performance.

---

## 🔍 Outlier Forensics: Noise vs. Signal
To unmask anomalies within the key monetary field (`TotalPrice`), two complementary analytical frameworks were deployed at the checkpoint gate:

1. **The IQR Method:** Evaluating bounds outside $[Q1 - 1.5 \times IQR]$ and $[Q3 + 1.5 \times IQR]$. With an $IQR$ of \$1,167.96, the critical upper threshold was established at **\$3,330.41**. This flag isolated **8 individual records** (0.67% of the dataset).
2. **The Z-Score Method:** Evaluating structural deviations where $|Z| > 3$. This method flagged **0 records**.

### ⚖️ The Verdict: Signal, Not Noise
The Z-score method failed to detect anomalies because it assumes a normal distribution, losing sensitivity when applied to right-skewed business matrices. The IQR method successfully captured the true variance. 

Granular review of the 8 isolated rows showed perfect arithmetic compliance ($\text{Quantity} \times \text{UnitPrice} = \text{TotalPrice}$) with no typing errors or format corruptions. Every flagged transaction represented a maximum volume order ($\text{Quantity} = 5$) matching a premium unit cost tier ($>\$660$). These are classified as **high-leverage wholesale/VIP consumer signals**, not data entry noise, and are preserved to form a dedicated enterprise segment.

---

## 🎯 High-Impact Business Diagnoses (The "So What?" Test)

### 🚨 1. The Operational Headline: Unrealized Revenue Drain
Logistical grouping of `OrderStatus` uncovered an urgent operational bottleneck: **41.4% of all orders placed fail to finalize as a closed sale**. 

* **The Leakage:** Cancelled orders (250 / 20.8%) combined with Returned orders (247 / 20.6%) account for **497 transactions**.
* **Financial Impact:** This bottleneck sequesters **\$519,673.91** in frozen capital—representing **41.1% of all gross recorded revenue (\$1,264,761.96)**. 
* **Action Item:** Prioritize operational root-cause diagnostics (e.g., payment interface dropouts, delivery lag times, or product description mismatches) before deploying further acquisition spend.

### 🛑 2. Unmasking Confounding Traps: The Temporal Illusion
A superficial interpretation of monthly aggregations suggests an aggressive transaction spike during the first half of the year (Jan–Jun) followed by a catastrophic decline in the second half. 

* **The Discovery:** This is an analytical artifact caused by a **data-coverage confounder**. The dataset records comprehensive tracking across full calendar years for 2023 and 2024, but terminates abruptly on June 30, 2025.
* **The Reality:** Isolating volumes chronologically by their respective years confirms that order velocity remains entirely flat. Annualizing the partial 2025 horizon (~462 projected orders) exposes an stable runway, completely debunking the seasonality narrative.

---

## 🗺️ Mapping Relationships: Correlation Matrix
Pearson Correlation Coefficients ($r$) were run across all quantitative matrices to isolate linear dependencies and evaluate growth levers:
