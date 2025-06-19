import pandas as pd
import plotly.express as px

def get_event_summary(df, code):
    if df.empty:
        return {}, None, None

    # Convert date field to datetime format
    df["date_received"] = pd.to_datetime(df["date_received"])
    # Group data by month for trend line
    trend = df.groupby(df["date_received"].dt.to_period("M")).size().reset_index()
    trend.columns = ["Month", "Reports"]
    trend["Month"] = trend["Month"].dt.strftime('%b-%Y') 

    fig = px.line(trend, x="Month", y="Reports", title="Monthly Adverse Events")


    type_counts = df["event_type"].value_counts().to_dict()


    # Get most common event type and the issue text
    most_common_type = df["event_type"].mode()[0]  # Most common event type
    most_common_pct = round((df["event_type"] == most_common_type).mean() * 100, 1)
    # top_issue = "sensor failure"  # Example, ideally pulled from 'mdr_text'

    # Count events where event_type is 'death'
    death_events = df[df["event_type"] == "Death"]
    death_reports = len(death_events)

    # Construct the narrative
    start_date = df["date_received"].min().strftime("%b-%Y")
    end_date = df["date_received"].max().strftime("%b-%Y")
    total_events = len(df)
    death_statement = f"{death_reports} death(s) were reported." if death_reports > 0 else "No deaths were reported."

    narrative = f"Between {start_date} and {end_date}, there were {total_events} adverse events associated with product code {code}, with {most_common_pct}% categorized as '{most_common_type}'. {death_statement}"

    return type_counts, fig, narrative
