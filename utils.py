
def engineerInfoGenerator(engineerList):
    stringBuffer = ''
    for engineer in engineerList:
        engineerName = engineer.name
        engineerDesc = engineer.description
        stringBuffer += f'{engineerName}\n{engineerDesc}\n--------------------\n'
    return stringBuffer

def contactInfoGenerator(contactList):
    stringBuffer = ''
    for contact in contactList:
        contactName = contact.name
        contactDesc = contact.description
        stringBuffer += f'{contactName}\n{contactDesc}\n--------------------\n'
    return stringBuffer