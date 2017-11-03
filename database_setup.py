#! usr/env/bin python

import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Menu(Base):
	__tablename__ = 'menu'

	name = Column( String(250), nullable = False)
	id = Column( Integer, primary_key = True)


class  MenuItem(Base):
	__tablename__ = 'menu_itemss'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	description = Column(String(250))
	price = Column(String(8))
	menu_id = Column(Integer, ForeignKey('menu.id'))
	menu = relationship(Menu)

engine =  create_engine('sqlite:///maverick.db')

Base.metadata.create_all(engine)

