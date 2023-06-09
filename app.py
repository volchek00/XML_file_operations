from flask import Flask, render_template, request
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
import os

app = Flask(__name__)

def process_xml_file(zip_file_path):
    items = []
    parts_and_spare_parts = []

    # Extracting the file
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall()
        xml_file = zip_ref.namelist()[0]

    # Loading XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find all item elements
    item_elements = root.findall('.//item')

    # Count the items and print their names
    count = 0
    for item in item_elements:
        name = item.get('name')
        if name:
            count += 1
            items.append(name)

    all_items_df = pd.DataFrame(items, columns=['All_items'])

    # Searching for categories with specific attributes
    for category in root.iter('category'):
        if category.attrib.get('type') == 'partType' and category.attrib.get('name') == 'Náhradní díly':
            for part in category.iter('part'):
                item_name = part.attrib.get('itemName')
                items = part.findall('item')
                names = [item.attrib.get('name') for item in items]
                parts_and_spare_parts.append({'Items': item_name, 'Spare parts': ', '.join(names)})

    # Creating a spare_parts_df from the parts_and_spare_parts
    spare_parts_df = pd.DataFrame(parts_and_spare_parts)

    return count, all_items_df, spare_parts_df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['choice']

    if user_input == "1":
        count, _, _ = process_xml_file("astra_export_xml.zip")
        result = f"Total number of items: {count} items"

    elif user_input == "2":
        _, all_items_df, _ = process_xml_file("astra_export_xml.zip")
        result = all_items_df.to_html(index=False)

    elif user_input == "3":
        _, _, spare_parts_df = process_xml_file("astra_export_xml.zip")
        result = spare_parts_df.to_html(index=False)

    elif user_input == "q":
        result = "Exiting..."

    else:
        result = "Invalid input. Please try again."

    return render_template('index.html', result=result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
