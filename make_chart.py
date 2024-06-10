import os

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from notion_client import Client

from utils import read_toml, safe_get

conf = read_toml("config.toml")
PLAINTEXT_DIR = conf["directory"]["plaintext_dir"]


def plot_pie(df: pd.DataFrame, values_name: str, names_name: str):
    fig = px.pie(df, values=values_name, names=names_name)
    fig.update(layout_showlegend=False)
    # fig.update_layout(legend=dict(yanchor="top", y=1.0, xanchor="right", x=1.0))
    fig.update_traces(textinfo="label+percent")
    # fig.update_traces(textposition="outside")
    return fig


def plot_pie2(df: pd.DataFrame, values_name: str, names_name: str):
    series = df.groupby([names_name])[values_name].sum()
    labels = series.index.values.tolist()
    values = series.values.tolist()

    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            textinfo="label+percent",
            showlegend=False,
        )
    )
    return fig


def plot_bar(df, x_name, y_name, labels_name):
    fig = px.bar(df, x=x_name, y=y_name, color=labels_name)
    return fig


def plot_main(df, chart_type, chart_name, time):
    ## Filter by time
    df = df[df["Date"].str.startswith(time)]

    ## Plot
    if chart_type == "pie":
        fig = plot_pie2(df, values_name="Expense", names_name="Type")
    elif chart_type == "bar":
        fig = plot_bar(df, x_name="Date", y_name="Expense", labels_name="Type")
    else:
        raise ValueError(f"Invalid chart type: {chart_type}")

    ## No margin
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    ## Save
    variantion_num = 0
    fig.write_html(
        os.path.join(
            PLAINTEXT_DIR, f"{time}_{chart_name}_{chart_type}_v{variantion_num}.html"
        )
    )


if __name__ == "__main__":
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    db_rows = notion.databases.query(database_id=os.getenv("NOTION_DATABASE_ID"))

    lst = []
    for i, row in enumerate(db_rows["results"]):
        if i == 0:
            print(row)
        name = safe_get(row, "properties.Name.title.0.plain_text")
        date = safe_get(row, "properties.Date.date.start")
        expense = safe_get(row, "properties.Expense.number")
        item_type = safe_get(row, "properties.Type.select.name")
        item = {"Name": name, "Date": date, "Expense": expense, "Type": item_type}
        lst.append(item)
    df = pd.DataFrame(lst)
    df = df.sort_values(by=["Date"])
    print(df)

    fig = plot_pie2(df, values_name="Expense", names_name="Type")
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    plot_main(df, chart_type="pie", chart_name="expense-by-type", time="2024-05")
    plot_main(df, chart_type="bar", chart_name="expense-by-date", time="2024-05")
