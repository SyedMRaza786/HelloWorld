from flask import Flask, redirect, jsonify
from flask import render_template
from flask import request
from db import delete_inventory, get_data, create_inventory_item, get_elements_in_inventory, get_elements_in_lab, get_inventory_for_element, update_inventory
app = Flask(__name__)


# ROUTES
@app.route('/')
def get_welcome():
    return render_template('welcome.jinja')

@app.route('/view')
def element():
    try:
        id = int(request.args.get('id'))
        element = get_inventory_for_element([x for x in get_data() if id == int(x['number'])][0])
        unit = 'Grams'
        if 'GAS' in element['phase'].upper():
            unit = 'Bar'
        elif 'LIQUID' in element['phase'].upper():
            unit = 'Milliliters'
        return render_template("view.jinja", element=element['element'], properties=element['properties'], unit=unit, note=element['safety_information'], lab=element['lab'], quantity=element['quantity'])
    except Exception as e:
        print(e)
        return render_template("search_results.jinja", elements={'elements' : []})

@app.route('/add', methods=['GET', 'POST'])
def elements():
    if(request.method == 'GET'):
        return render_template("add.jinja", elements={'elements' : get_data()}, error="")
    elif(request.method == 'POST'):
        data = request.get_json()
        element = data['element']
        quantity = data['quantity']
        lab = data['lab']
        safety_information = data['notes']
        if(create_inventory_item(element, quantity, lab, safety_information)):
            return jsonify({'id' : element})
        else:
            # Return a json with error or the id of the element
            return jsonify({'error' : 'Element already in inventory'})
        

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    try:
        if(request.method == 'GET'):
            id = int(request.args.get('id'))

            element = get_inventory_for_element([x for x in get_data() if id == int(x['number'])][0])
            unit = 'Grams'
            if 'GAS' in element['phase'].upper():
                unit = 'Bar'
            elif 'LIQUID' in element['phase'].upper():
                unit = 'Milliliters'
            return render_template("edit.jinja", element=element['element'], properties=element['properties'], unit=unit, note=element['safety_information'], lab=element['lab'], quantity=element['quantity'])
        elif(request.method == 'POST'):
            data = request.form
            element = int(request.args.get('id'))
            quantity = data['quantity']
            lab = data['lab']
            safety_information = data['notes']
            update_inventory(element, quantity, lab, safety_information)
            return redirect(f'/view?id={element}')
            
    except:
        return redirect('/')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if(request.method == 'GET'):
        return render_template("delete.jinja", elements={'elements' : get_elements_in_inventory()})
    elif(request.method == 'POST'):
        element = request.form['element']
        delete_inventory(element)
        return render_template("delete.jinja", elements={'elements' : get_elements_in_inventory()})

@app.route('/search', methods=['POST', 'GET'])
def search():
    try:
        if(request.method == 'GET'):
            data = request.args.get('q')
        else:
            data = request.form['q']
        query = data

        elements = get_data()
        filtered_elements = []
        for term in ['name', 'appearance', 'phase', 'category', 'discovered_by']:
            cur_elements = [x for x in elements if x[term] and query.lower() in x[term].lower()]
            for x in cur_elements:
                if x not in filtered_elements:
                    filtered_elements.append(x)
        elements = filtered_elements + get_elements_in_lab(query)
        elements = sorted(elements, key=lambda x: x['name'].lower().find(query.lower()) if query.lower() in x['name'].lower() else 10000)
        return render_template("search_results.jinja", elements={'elements' : elements})
    except Exception as e:
        print(e)
        return render_template("search_results.jinja", elements={'elements' : []})

if __name__ == '__main__':
    app.run(debug=True)
