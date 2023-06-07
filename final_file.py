import zipfile
import xml.etree.ElementTree as ET
import pandas as pd

def main():
    items = []
    parts_and_spare_parts = []

    # Extracting the file
    with zipfile.ZipFile("astra_export_xml.zip", "r") as zip_ref:
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
                parts_and_spare_parts.append({'Item Name': item_name, 'Names': ', '.join(names)})

    # Creating a spare_parts_df from the parts_and_spare_parts
    spare_parts_df = pd.DataFrame(parts_and_spare_parts)

    while True:
        user_input = input("Enter your choice (1, 2, 3, or q to quit): ")

        if user_input == "1":
            print(f"Total number of items: {count} items")

        elif user_input == "2":
            print(all_items_df['All_items'])

        elif user_input == "3":
            print(spare_parts_df)

        elif user_input == "q":
            break
        
        else:
            print("Invalid input. Please try again.")

if __name__ == '__main__':
    main()
