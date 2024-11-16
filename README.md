# Site Incident Analysis Tool

This is a Streamlit-based application for analyzing and processing site incident data. The tool allows users to upload an Excel file, process the data by tenant categories, and export the results into a downloadable Excel file.

---

## Features
- Upload an Excel file containing site incident data.
- Process data to group by `Tenant` and calculate aggregated metrics such as:
  - Total `Elapsed Time Count` per site.
  - Number of incidents per site.
- Display the processed data interactively.
- Download the results as a multi-sheet Excel file.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/<your-username>/site-incident-analysis.git
   cd site-incident-analysis
