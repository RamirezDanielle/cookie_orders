from flask import Flask, request, render_template, redirect, session
from flask_app import app

from flask_app.models.cookie import Cookie

@app.route('/')
def index():
    orders = Cookie.get_all()
    return render_template('cookie_orders.html', orders = orders)

@app.route('/add/order')
def new_order():
    return render_template('new_order.html')

@app.route('/cookies/new', methods=['POST'])
def save():
    print(request.form)
    data = {
        'name' : request.form['name'],
        'cookie_type' : request.form['cookie_type'],
        'num_boxes' : request.form['num_boxes'],
    }
    valid = Cookie.validate_order(data)
    if valid:
        Cookie.save(request.form)
        return redirect('/')
    return redirect('/add/order')

#edit order
@app.route('/cookie/edit/<int:order_id>')
def edit(order_id):
    order=Cookie.get_one(order_id)
    return render_template('change_order.html', order = order)


@app.route('/cookie/update', methods=['POST'])
def update_order():
    print(request.form)
    Cookie.update(request.form)