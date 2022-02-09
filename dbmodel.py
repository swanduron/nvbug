from sqlalchemy import *
from sqlalchemy.orm import *
from PyQt6.QtCore import QDate


Base = declarative_base()

class Case(Base):

    __tablename__ = 'case'
    id = Column(Integer, primary_key=True)
    case_id = Column(String(40))
    date = Column(String(40))
    description = Column(String(400))
    rmas = relationship('Rma', backref='case')
    logs = relationship('logInfo', backref='case')
    caseCompFlag = Column(Boolean, default=False)


class Rma(Base):

    __tablename__ = 'rma'
    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey('case.id'))
    rma_id = Column(String(40))
    date = Column(String(40))
    rmaETD = Column(String(40))
    rmaSrvDate = Column(String(40))
    description = Column(String(400))
    rmaItemID = Column(String(40))
    rmaPN = Column(String(40))
    rmaOriSN = Column(String(40))
    # Add 4 flags to mark the progress during provide service
    componentsSendFlag = Column(Boolean, default=False)
    componentsRecvFlag = Column(Boolean, default=False)
    rmaCompFlag = Column(Boolean, default=False)
    rmaReturnFlag = Column(Boolean, default=False)
    rmaCompleteFlag = Column(Boolean, default=False)
    engineers = relationship('Engineer', secondary='linkrmaengineer')
    contacts = relationship('Contact', secondary='linkrmacontacts')
    old_hardware = relationship('Oldcomponent', backref=backref('rma', uselist=False))
    new_hardware = relationship('Newcomponent', backref=backref('rma', uselist=False))
    logs = relationship('logInfo', backref='rma')

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
class logInfo(Base):

    __tablename__ = 'loginfo'
    id = Column(Integer, primary_key=True)
    date = Column(String(40))
    content = Column(String(2000))
    rma_id = Column(Integer, ForeignKey('rma.id'))
    case_id = Column(Integer, ForeignKey('case.id'))


if __name__ == '__main__':
    engine = create_engine('sqlite:///nvbug.db', echo=True)
    #
    # Case.__table__.create(engine)
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
    # logInfo.__table__.create(engine)

    # Data initlization
    # currentDate = QDate.currentDate().toPyDate()
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
    # case = Case(case_id='0099842', date=currentDate, description='demo case')
    # rma = Rma(rma_id='24231', date=currentDate)
    # case.rmas.append(rma)
    #
    #
    # session.add(case)
    # session.commit()

    # query data test
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
    # res = session.query(Case).filter_by(case_id='0099842').one()
    # for i in res.rmas:
    #     print(i.rma_id)