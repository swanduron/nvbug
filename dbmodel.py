from sqlalchemy import *
from sqlalchemy.orm import *
from PyQt6.QtCore import QDate

engine = create_engine('sqlite:///nvbug.db', echo=True)
Base = declarative_base()

class Case(Base):

    __tablename__ = 'case'
    id = Column(Integer, primary_key=True)
    case_id = Column(String(40))
    date = Column(String(40))
    description = Column(String(400))
    nvbugs = relationship('Nvbug', backref='case')

class Nvbug(Base):

    __tablename__ = 'nvbug'
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('case.id'))
    nvbug_id = Column(String(40))
    date = Column(String(40))
    rmas = relationship('Rma', backref='nvbug')

class Rma(Base):

    __tablename__ = 'rma'
    id = Column(Integer, primary_key=True)
    nvbug_id = Column(Integer, ForeignKey('nvbug.id'))
    rma_id = Column(String(40))
    date = Column(String(40))
    engineers = relationship('Engineer', secondary='linkrmaengineer')
    contacts = relationship('Contact', secondary='linkrmacontacts')
    old_hardware = relationship('Oldcomponent', backref=backref('rma', uselist=False))
    new_hardware = relationship('Newcomponent', backref=backref('rma', uselist=False))

# Link

class Linkrmaengineer(Base):

    __tablename__ = 'linkrmaengineer'
    rma_id = Column(Integer, ForeignKey('rma.id'), primary_key=True)
    engineer_id = Column(Integer, ForeignKey('engineer.id'), primary_key=True)

class Linkrmacontacts(Base):

    __tablename__ = 'linkrmacontacts'
    rma_id = Column(Integer, ForeignKey('rma.id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('contact.id'), primary_key=True)

####Service Provider

class Engineer(Base):

    __tablename__ = 'engineer'
    id = Column(Integer, primary_key=True)
    supporter_id = Column(Integer, ForeignKey('supporter.id'))
    rma_id = Column(Integer, ForeignKey('rma.id'))
    name = Column(String(40))
    description = Column(String(500))
    date = Column(String(40))
    rmas = relationship('Rma', secondary='linkrmaengineer')

class Supporter(Base):

    __tablename__ = 'supporter'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    description = Column(String(500))
    date = Column(String(40))
    engineers = relationship('Engineer', backref='supporter')

# Customer's contact

class Contact(Base):

    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    rma_id = Column(Integer, ForeignKey('rma.id'))
    name = Column(String(40))
    description = Column(String(500))
    date = Column(String(40))
    rmas = relationship('Rma', secondary='linkrmacontacts')

class Address(Base):

    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    name = Column(String(40))
    description = Column(String(500))
    date = Column(String(40))

class Customer(Base):

    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    description = Column(String(500))
    date = Column(String(40))
    contacts = relationship('Contact', backref='customer')
    addresses = relationship('Address', backref='customer')

class Newcomponent(Base):

    __tablename__ = 'newcomponent'
    id = Column(Integer, primary_key=True)
    rma_id = Column(Integer, ForeignKey('rma.id'))
    description = Column(String(500))
    desc = Column(String(100))

class Oldcomponent(Base):

    __tablename__ = 'oldcomponent'
    id = Column(Integer, primary_key=True)
    rma_id = Column(Integer, ForeignKey('rma.id'))
    description = Column(String(500))
    desc = Column(String(100))

# add express information

if __name__ == '__main__':
    # Case.__table__.create(engine)
    # Nvbug.__table__.create(engine)
    # Rma.__table__.create(engine)
    # Linkrmaengineer.__table__.create(engine)
    # Linkrmacontacts.__table__.create(engine)
    # Engineer.__table__.create(engine)
    # Supporter.__table__.create(engine)
    # Contact.__table__.create(engine)
    # Address.__table__.create(engine)
    # Customer.__table__.create(engine)
    # Newcomponent.__table__.create(engine)
    # Oldcomponent.__table__.create(engine)

    # Data initlization
    currentDate = QDate.currentDate().toPyDate()
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    case = Case(case_id='0099842', date=currentDate, description='demo case')
    nvbug = Nvbug(nvbug_id='49032', date=currentDate)
    case.nvbugs.append(nvbug)
    rma = Rma(rma_id='24231', date=currentDate)
    nvbug.rmas.append(rma)


    session.add(case)
    session.commit()
