# Notion Expense Visualizer

## Motivation
I use notion to track my expenses. However, notion does not provide a built-in way to draw charts.

Some web services provide a way to visualize data from notion, such as [DataJumbo](https://www.datajumbo.co/). However, its functionality is limited and it is not free.

Meanwhile, some open-source visualization libraries, such as [plotly](https://plotly.com/python/) provide extremely powerful toolsets to visualize data, and save the result as a html file, which can be easily embedded in notion.

Therefore, I decided to combine the notion and plotly, two most powerful tools in their own field, to create a simple and free way to visualize my expenses, and share it with you.

## Features
- Visualize expenses in different forms, such as pie chart, bar chart... (TODO)
- Encrypt the chart html files by assigning random names and encrypt their content with keys, in order to protect your privacy
- Assign a unique link to each encrypted html file using Flask, so that you can easily access them from URL
- Automatically insert the link to the notion page (TODO)

## How to use
Setup the python environment
```bash
pip install -r requirements.txt
```

Set your notion token and database id in environment variables
```bash
export NOTION_TOKEN="your_notion_token"
export NOTION_DATABASE_ID="your_notion_database_id"
```

To make the chart
```bash
python make_chart.py
```

To encrypt the generated html files
```bash
python encrypt_files.py
```

To run the server
```bash
python server.py
```
