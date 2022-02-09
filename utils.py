
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

def pickupEmailGen(rmaInstance):
    # By default design, each RMA only include one component, if a chassis need to replace multiple parts, for example
    # 1 x PDB and 1x CPU try, it will be generated 2 RMA records
    case_id = rmaInstance.case.case_id
    rmaContacts = ''
    customerInstance = rmaInstance.contacts[0].customer
    for contact in rmaInstance.contacts:
        rmaContacts += f'Name: {contact.name} \n {contact.description}'

    msgTemplate = f'''To: FSL-Support <fsl-support@nvidia.com>; 
CC: NVES-DGX <nves-dgx@nvidia.com>; DGX-RMA-SUPPORT <DGX-RMA-SUPPORT@nvidia.com>

Mail Title: Return RMA <{rmaInstance.rmaItemID}> case <{case_id}> <INFO NEED TO BE REPLACED BY REGION!>

Hi FSL team,

Please help to create a pickup delivery order for the customer to return the bad unit.

---------Components Information-------

Case: {case_id}, RMA Item Number: <{rmaInstance.rmaItemID}>, RMA Part Number: <{rmaInstance.rmaPN}>, 1x, SN: <{rmaInstance.rmaOriSN}>

----------Customer Information--------
{customerInstance.name}
{customerInstance.description}

----------Contacts Information--------
{rmaContacts}

----------End of Information----------


Regards
Haitao Sun
'''
    return msgTemplate