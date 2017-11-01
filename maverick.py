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

@app.route('/maverick/<int:menu_id>/delete')
def deleteMenu(menu_id):
	return ("page that delete the menu %s" %menu_id)

@app.route('/maverick/<int:menu_id>/')
@app.route('/maverick/<int:menu_id>/menu/')
def allMenuItem(menu_id):
	return ("page that displays menu items of Menu %s" %menu_id)

@app.route('/maverick/<int:menu_id>/new')
@app.route('/maverick/<int:menu_id>/menu/new')
def newMenuItem(menu_id):
	return ("page that allows user to add new item to menu %s" %menu_id)

@app.route('/maverick/<int:menu_id>/<int:menuItem_id>')
def menuItem(menu_id,menuItem_id):
	return ("page that shows detail description of item %s of menu %s" % (menuItem_id, menu_id))

@app.route('/maverick/<int:menu_id>/<int:menuItem_id>/edit')
def  editMenuItem(menu_id, menuItem_id):
	return ("page that allows user to edit item item %s of menu %s" % (menuItem_id, menu_id))

@app.route('/maverick/<int:menu_id>/<int:menuItem_id>/delete')
def  deleteMenuItem(menu_id, menuItem_id):
	return ("page that allows user to delete item %s of menu %s" % (menuItem_id, menu_id))



if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)