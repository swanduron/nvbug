
def engineerInfoGenerator(engineerList):
    stringBuffer = ''
    for engineer in engineerList:
        engineerName = engineer.name
        engineerDesc = engineer.description
        stringBuffer += f'{engineerName}\n{engineerDesc}\n--------------------\n'
    return stringBuffer

def contactInfoGenerator(contactList):
    stringBuffer = ''
    if contactList:
        parentInstance = contactList[0].customer
        stringBuffer += f'-----Customer INFO------\n' \
                        f'Name: {parentInstance.name}\n' \
                        f'{parentInstance.description}\n\n' \
                        f'-----Contact INFO-------\n'
    for contact in contactList:
        contactName = contact.name
        contactDesc = contact.description
        stringBuffer += f'Name: {contactName}\n{contactDesc}\n--------------------\n'
    return stringBuffer