import json
import copy
elements = []
inventory = []
def get_data():
    global elements
    if(elements == []):
        with open('elements.json', 'r', encoding='utf-8') as f:
            elements = json.load(f)['elements']
    return elements

def create_inventory_item(element_foreignKey, quantity, lab, safety_information):
    global inventory
    load_inventory()
    if(element_foreignKey in [x['element'] for x in inventory]):
        return False
    inventory.append({
        'element': element_foreignKey,
        'quantity': quantity,
        'lab': lab,
        'safety_information': safety_information,
    })
    save_inventory()
    return True

def update_inventory(element_foreignKey, quantity, lab, safety_information):
    global inventory
    load_inventory()
    found = False
    for item in inventory:
        if item['element'] == element_foreignKey or item['element'] == str(element_foreignKey):
            item['quantity'] = quantity
            item['lab'] = lab
            item['safety_information'] = safety_information
            found = True
            break
    if not found:
        create_inventory_item(str(element_foreignKey), quantity, lab, safety_information)
    save_inventory()

def load_inventory():
    global inventory
    try:
        if(inventory == []):
            with open('inventory.json', 'r', encoding='utf-8') as f:
                inventory = json.load(f)['inventory']
    except Exception as e:
        print(e)
        inventory = []

def delete_inventory(element_foreignKey):
    global inventory
    load_inventory()
    inventory = [x for x in inventory if x['element'] != element_foreignKey]
    save_inventory()


def get_elements_in_lab(lab):
    return [x['element'] for x in get_inventory_joined() if x['lab'] == lab]

def get_inventory_for_element(element):
    items = [x for x in get_inventory_joined() if x['element']['number'] == element['number']]
    if len(items) == 0:
        return {
            'element': element,
            'quantity': '0',
            'lab': 'None',
            'safety_information': 'None',
            'properties': get_element_properties(element),
            'phase': element['phase']
        }
    else:
        item = items[0].copy()
        item['properties'] = get_element_properties(element)
        item['phase'] = element['phase']
        return item

def get_element_properties(element):
    props = set()
    for prop in (element['appearance'].upper().split(', ') if element['appearance'] else []) + element['category'].upper().split(', ') + element['phase'].upper().split(' '):
        if(prop.strip() == 'UNKNOWN' or prop.strip() == ''):
            continue            
        if len(prop.strip()) <= 30:
            if ' OR ' in prop:
                for sub_prop in prop.split(' OR '):
                    props.add(sub_prop.strip())
            else:
                props.add(prop.strip())
    return list(props)

def get_elements_in_inventory():
    return [x['element'] for x in get_inventory_joined()]

def get_inventory_joined():
    load_inventory()
    inventory_copy = copy.deepcopy(inventory)
    for item in inventory_copy:
        item['element'] = get_element_by_id(item['element'])
    return inventory_copy

def get_element_by_id(id):
    id = int(id)
    return [x for x in get_data() if id == int(x['number'])][0]

def save_inventory():
    with open('inventory.json', 'w') as f:
        json.dump({'inventory': inventory}, f)