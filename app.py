import streamlit as st
from utils.fetch import get_maude_data
from utils.summarize import get_event_summary
import pandas as pd
import plotly.express as px

st.title("MAUDE PMS Preview Dashboard")

# Step 1: Allow users to input multiple product codes
code_input = st.text_input("Enter FDA Product Code(s): (separate with '+')", value="LYZ")
product_codes = code_input.split("+")  # Split input by '+' for multiple codes

if product_codes:
    all_data = pd.DataFrame()
    # Flatten device-level fields like manufacturer_d_name and brand_name
    def extract_first_device_field(row, field):
        dev = row.get("device")
        if isinstance(dev, list) and len(dev) > 0:
            return dev[0].get(field)
        return None



    all_data["manufacturer_d_name"] = all_data.apply(lambda row: extract_first_device_field(row, "manufacturer_d_name"), axis=1)
    all_data["brand_name"] = all_data.apply(lambda row: extract_first_device_field(row, "brand_name"), axis=1)


    for code in product_codes:
        with st.spinner(f"Fetching data for {code}..."):
            df = get_maude_data(code.strip())  # Strip any extra spaces
        if df.empty:
            st.warning(f"No data found for product code {code}.")
        else:
            all_data = pd.concat([all_data, df], ignore_index=True)

    if not all_data.empty:
        types, trend_fig, text = get_event_summary(all_data, code_input)

        # Step 2: Show the raw data
        # st.subheader("Raw Data")
        # st.dataframe(all_data)[:30]

        # st.download_button(
        #     label="Download Raw Data as Excel",
        #     data=all_data.to_excel(index=False),
        #     file_name="maude_data.xlsx",
        #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        # )

        # Step 3: Show Adverse Event Type Breakdown (Pie Chart)
        st.subheader("Event Type Breakdown")
        event_type_counts = all_data["event_type"].value_counts()
        fig_pie = px.pie(event_type_counts, names=event_type_counts.index, values=event_type_counts.values, title="Adverse Event Types")
        st.plotly_chart(fig_pie)

        # Step 4: Show Competitor Scan (Manufacturers and Device Names)
        st.subheader("Competitor Scan")
        # competitor_data = all_data[['brand_name', 'manufacturer_d_name']].dropna().drop_duplicates()
        competitor_data = all_data['brand_name'].drop_duplicates()
        st.write(competitor_data)


        # Step 5: Show a Stacked Bar Chart of Event Counts by Manufacturer and Event Type
        st.subheader("Manufacturer Event Counts")
        # st.write("Columns available:", all_data.columns.tolist())
        manufacturer_event_count = all_data.groupby(['manufacturer_d_name', 'event_type']).size().reset_index(name="count")
        fig_bar = px.bar(manufacturer_event_count, x="manufacturer_d_name", y="count", color="event_type", title="Adverse Event Count per Manufacturer", barmode="stack")
        st.plotly_chart(fig_bar)

        # Narrative Preview
        st.subheader("Narrative Preview")
        st.write(text[:500])

        st.success("Want the full PMS-ready report?")
        st.button("Download Full Report ($10)", disabled=True)

        # st.subheader("Raw device field (first 3 rows)")
        # st.write(all_data["device"].head(3))
        # st.subheader("Device fields preview")
        # st.write(all_data[["brand_name", "manufacturer_d_name"]].dropna().head())
