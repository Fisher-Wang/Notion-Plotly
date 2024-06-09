import os

import pandas as pd
import plotly.express as px
from notion_client import Client

from utils import read_toml

conf = read_toml("config.toml")
PLAINTEXT_DIR = conf["directory"]["plaintext_dir"]


def safe_get(data, dot_chained_keys):
    """
    {'a': {'b': [{'c': 1}]}}
    safe_get(data, 'a.b.0.c') -> 1
    """
    keys = dot_chained_keys.split(".")
    for key in keys:
        try:
            if isinstance(data, list):
                data = data[int(key)]
            else:
                data = data[key]
        except (KeyError, TypeError, IndexError):
            return None
    return data


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
        type = safe_get(row, "properties.Type.select.name")
        item = {"Name": name, "Date": date, "Expense": expense, "Type": type}
        lst.append(item)
    df = pd.DataFrame(lst)
    df = df.sort_values(by=["Date"])
    print(df)

    fig = px.pie(df, values="Expense", names="Type", title="Expenses by Type")

    time = "2024-05"
    chart_name = "expense-by-type"
    chart_type = "pie"
    variantion_num = 0
    fig.write_html(
        os.path.join(
            PLAINTEXT_DIR, f"{time}_{chart_name}_{chart_type}_v{variantion_num}.html"
        )
    )
