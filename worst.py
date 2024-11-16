import streamlit as st
import pandas as pd

# Streamlit app title
st.title("Site Incident Analysis")

# File upload section
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load the uploaded Excel file
    df = pd.read_excel(uploaded_file, sheet_name='Sheet1')

    # Process the data
    grouped_df = df.groupby('Site').agg({
        'Site Alias': 'first',
        'RMS Station': 'first',
        'Zone': 'first',
        'Cluster': 'first',
        'Tenant': 'first',
        'Elapsed Time Count': 'sum'
    }).reset_index()

    # Count the number of occurrences of each site
    incident_count = df['Site'].value_counts().reset_index()
    incident_count.columns = ['Site', 'Incident Count']

    # Merge grouped data with incident count
    merged_df = pd.merge(grouped_df, incident_count, on='Site')

    # Sort by total elapsed time count in descending order
    sorted_df = merged_df.sort_values(by='Elapsed Time Count', ascending=False)

    # Select relevant columns
    sorted_df = sorted_df[['Site Alias', 'RMS Station', 'Zone', 'Cluster', 'Tenant', 'Incident Count', 'Elapsed Time Count']]

    # Display the processed data
    st.subheader("Processed Data")
    st.dataframe(sorted_df)

    # Create separate sheets for each tenant and all tenants
    output_data = {}
    for tenant_category in sorted_df['Tenant'].unique():
        tenant_data = sorted_df[sorted_df['Tenant'] == tenant_category].sort_values(by='Elapsed Time Count', ascending=False)
        output_data[tenant_category] = tenant_data

    # Add "All Tenants" data
    all_tenants_data = sorted_df.sort_values(by='Elapsed Time Count', ascending=False)
    output_data['All Tenants'] = all_tenants_data

    # Provide download option
    @st.cache_data
    def generate_excel(data_dict):
        from io import BytesIO

        # Create an Excel writer in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for sheet_name, data in data_dict.items():
                data.to_excel(writer, sheet_name=sheet_name, index=False)
        output.seek(0)
        return output

    excel_data = generate_excel(output_data)
    st.download_button(
        label="Download Processed Data",
        data=excel_data,
        file_name="sorted_data_with_remarks.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
