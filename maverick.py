#! usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Menu, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///maverick.db')
Base.metadata.bind = engine
DBSession =  sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/maverick/')
def allMenu():
	menu_id = session.query(Menu).all()
	print(menu_id)
	return render_template('index.html', menu_id = menu_id)

@app.route('/maverick/new', methods=['GET','POST'])
def newMenu():
	if request.method == 'POST':
		addMenu = Menu(name = request.form['name'])
		session.add(addMenu)
		session.commit()
		return redirect(url_for('allMenu'))
	else:
		return render_template('newmenu.html')

@app.route('/maverick/<int:menu_id>/edit', methods =['GET','POST'])
def editMenu(menu_id):
	editedMenu = session.query(Menu).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedMenu.name = request.form['name']
		session.add(editedMenu)
		session.commit()
		return redirect(url_for('allMenu'))
	else:
		return render_template('editmenu.html', menu_id=menu_id, item=editedMenu)

@app.route('/maverick/<int:menu_id>/delete', methods = ['GET','POST'])
def deleteMenu(menu_id):
	deletedMenu = session.query(Menu).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(deletedMenu)
		session.commit()
		return redirect(url_for('allMenu'))
	else:
		return render_template('deleteMenu.html', item = deletedMenu)

@app.route('/maverick/<int:menu_id>/')
@app.route('/maverick/<int:menu_id>/menu/')
def allMenuItem(menu_id):
	menu = session.query(Menu).filter_by(id = menu_id).one()
	item = session.query(MenuItem).filter_by(menu_id = menu.id)
	return render_template('menuitem.html', menu = menu , item = item )


@app.route('/maverick/<int:menu_id>/new')
@app.route('/maverick/<int:menu_id>/menu/new', methods =['GET','POST'])
def newMenuItem(menu_id):
	if request.method == 'POST':
		addItem =  MenuItem(name = request.form['name'], price = request.form['price'], description = request.form['description'], menu_id = menu_id)
		session.add(addItem)
		session.commit()
		return redirect(url_for('allMenuItem', menu_id = menu_id))
	else:
		return render_template('newmenuitem.html', menu_id = menu_id)

@app.route('/maverick/<int:menu_id>/<int:menuItem_id>/edit', methods = ['GET','POST'])
def  editMenuItem(menu_id, menuItem_id):
	item = session.query(MenuItem).filter_by(id = menuItem_id).one()
	if request.method == 'POST':
		if request.form['name']:
			item.name = request.form['name']
		session.add(item)
		session.commit()
		return redirect(url_for('allMenuItem', menu_id = menu_id))
	else:
		return render_template('editmenuitem.html', menu_id = menu_id , menuItem_id = menuItem_id, i = item)

@app.route('/maverick/<int:menu_id>/<int:menuItem_id>/delete', methods = ['GET','POST'])
def  deleteMenuItem(menu_id, menuItem_id):
	item = session.query(MenuItem).filter_by(id = menuItem_id).one()
	if request.method == 'POST':
		session.delete(item)
		print("item has been deleted")
		return redirect(url_for('allMenuItem', menu_id = menu_id))
	else:
		return render_template('deletemenuitem.html', i = item)
	



if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)