
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
    try:
        customerInstance = rmaInstance.contacts[0].customer
    except:
        return 'No customer information is provided, please check RMA.'
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

def pcieAddrFinder():

    pcieTree = '''00:00.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
00:00.2 IOMMU: Advanced Micro Devices, Inc. [AMD] Starship/Matisse IOMMU
00:01.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
00:01.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
00:02.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
00:03.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
00:04.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
00:05.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
00:07.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
00:07.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
00:08.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
00:08.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
00:14.0 SMBus: Advanced Micro Devices, Inc. [AMD] FCH SMBus Controller (rev 61)
00:14.3 ISA bridge: Advanced Micro Devices, Inc. [AMD] FCH LPC Bridge (rev 51)
00:18.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 0
00:18.1 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 1
00:18.2 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 2
00:18.3 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 3
00:18.4 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 4
00:18.5 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 5
00:18.6 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 6
00:18.7 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 7
00:19.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 0
00:19.1 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 1
00:19.2 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 2
00:19.3 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 3
00:19.4 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 4
00:19.5 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 5
00:19.6 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 6
00:19.7 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship Device 24; Function 7
01:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
02:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
02:04.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
02:08.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
02:1c.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
03:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
04:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
04:10.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
04:14.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
05:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
06:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
07:00.0 3D controller: NVIDIA Corporation Device 20b0 (rev a1) GPU0
09:00.0 Non-Volatile memory controller: Samsung Electronics Co Ltd NVMe SSD Controller PM173X
0a:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
0b:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
0b:10.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
0c:00.0 Infiniband controller: Mellanox Technologies MT28908 Family [ConnectX-6] IB6
0d:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
0e:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
0f:00.0 3D controller: NVIDIA Corporation Device 20b0 (rev a1) GPU1
10:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
11:10.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
12:00.0 Infiniband controller: Mellanox Technologies MT28908 Family [ConnectX-6] IB7
13:00.0 Mass storage controller: Broadcom / LSI Device c010 (rev b0)
14:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function
14:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
15:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
15:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
15:00.3 USB controller: Advanced Micro Devices, Inc. [AMD] Starship USB 3.0 Host Controller
20:00.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
20:00.2 IOMMU: Advanced Micro Devices, Inc. [AMD] Starship/Matisse IOMMU
20:01.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
20:02.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
20:03.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
20:03.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
20:03.2 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
20:03.3 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
20:04.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
20:05.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
20:07.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
20:07.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
20:08.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
20:08.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
22:00.0 Non-Volatile memory controller: Samsung Electronics Co Ltd NVMe SSD Controller SM981/PM981/PM983
23:00.0 Non-Volatile memory controller: Samsung Electronics Co Ltd NVMe SSD Controller SM981/PM981/PM983
24:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function
24:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
25:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
25:00.1 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Cryptographic Coprocessor PSPCPP
25:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
25:00.3 USB controller: Advanced Micro Devices, Inc. [AMD] Starship USB 3.0 Host Controller
40:00.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
40:00.2 IOMMU: Advanced Micro Devices, Inc. [AMD] Starship/Matisse IOMMU
40:01.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
40:01.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
40:02.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
40:03.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
40:04.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
40:05.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
40:07.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
40:07.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
40:08.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
40:08.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
41:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
42:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
42:04.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
42:08.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
42:1c.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
43:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
44:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
45:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
46:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
46:1f.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
47:00.0 3D controller: NVIDIA Corporation Device 20b0 (rev a1) GPU2
48:00.0 Serial Attached SCSI controller: Broadcom / LSI Device 00b2 (rev b0)
49:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
4a:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
4a:10.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
4b:00.0 Infiniband controller: Mellanox Technologies MT28908 Family [ConnectX-6] IB0
4c:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
4d:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
4d:1f.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
4e:00.0 3D controller: NVIDIA Corporation Device 20b0 (rev a1) GPU3
4f:00.0 Serial Attached SCSI controller: Broadcom / LSI Device 00b2 (rev b0)
50:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
51:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
51:04.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
51:10.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
52:00.0 Non-Volatile memory controller: Samsung Electronics Co Ltd NVMe SSD Controller PM173X
54:00.0 Infiniband controller: Mellanox Technologies MT28908 Family [ConnectX-6] OB1
55:00.0 Mass storage controller: Broadcom / LSI Device c010 (rev b0)
56:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function
56:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
57:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
57:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
60:00.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
60:00.2 IOMMU: Advanced Micro Devices, Inc. [AMD] Starship/Matisse IOMMU
60:01.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
60:02.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
60:03.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
60:03.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
60:04.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
60:05.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
60:05.2 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
60:07.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
60:07.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
60:08.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
60:08.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
62:00.0 PCI bridge: ASPEED Technology, Inc. AST1150 PCI-to-PCI Bridge (rev 04)
63:00.0 VGA compatible controller: ASPEED Technology, Inc. ASPEED Graphics Family (rev 41)
64:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function
64:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
65:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
65:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
80:00.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
80:00.2 IOMMU: Advanced Micro Devices, Inc. [AMD] Starship/Matisse IOMMU
80:01.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
80:01.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
80:02.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
80:03.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
80:04.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
80:05.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
80:07.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
80:07.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
80:08.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
80:08.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
81:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
82:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
82:04.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
82:08.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
82:1c.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
83:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
84:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
84:10.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
84:14.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
85:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
86:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
86:1f.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
87:00.0 3D controller: NVIDIA Corporation Device 20b0 (rev a1) GPU4
88:00.0 Serial Attached SCSI controller: Broadcom / LSI Device 00b2 (rev b0)
8a:00.0 Non-Volatile memory controller: Samsung Electronics Co Ltd NVMe SSD Controller PM173X
8b:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
8c:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
8c:10.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
8d:00.0 Infiniband controller: Mellanox Technologies MT28908 Family [ConnectX-6] IB8
8e:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
8f:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
8f:1f.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
90:00.0 3D controller: NVIDIA Corporation Device 20b0 (rev a1) GPU5
91:00.0 Serial Attached SCSI controller: Broadcom / LSI Device 00b2 (rev b0)
92:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
93:10.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
94:00.0 Infiniband controller: Mellanox Technologies MT28908 Family [ConnectX-6] IB9
95:00.0 Mass storage controller: Broadcom / LSI Device c010 (rev b0)
96:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function
96:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
97:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
97:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
97:00.3 USB controller: Advanced Micro Devices, Inc. [AMD] Starship USB 3.0 Host Controller
a0:00.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
a0:00.2 IOMMU: Advanced Micro Devices, Inc. [AMD] Starship/Matisse IOMMU
a0:01.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
a0:02.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
a0:03.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
a0:04.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
a0:05.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
a0:07.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
a0:07.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
a0:08.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
a0:08.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
a1:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function
a1:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
a2:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
a2:00.1 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Cryptographic Coprocessor PSPCPP
a2:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
b0:00.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
b0:00.2 IOMMU: Advanced Micro Devices, Inc. [AMD] Starship/Matisse IOMMU
b0:01.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
b0:01.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
b0:02.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
b0:03.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
b0:04.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
b0:05.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
b0:07.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
b0:07.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
b0:08.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
b0:08.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
b1:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
b2:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
b2:04.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
b2:08.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
b2:1c.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
b3:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
b4:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
b5:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
b6:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
b7:00.0 3D controller: NVIDIA Corporation Device 20b0 (rev a1) GPU6
b8:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
b9:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
b9:10.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
ba:00.0 Infiniband controller: Mellanox Technologies MT28908 Family [ConnectX-6] IB2
bb:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
bc:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
bd:00.0 3D controller: NVIDIA Corporation Device 20b0 (rev a1) GPU7
be:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
bf:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
bf:04.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
bf:08.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
bf:10.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
c0:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
c1:00.0 PCI bridge: Broadcom / LSI Device c010 (rev b0)
c2:00.0 PCI bridge: PLX Technology, Inc. Device 8725 (rev ca)
c3:01.0 PCI bridge: PLX Technology, Inc. Device 8725 (rev ca)
c3:02.0 PCI bridge: PLX Technology, Inc. Device 8725 (rev ca)
c3:03.0 PCI bridge: PLX Technology, Inc. Device 8725 (rev ca)
c3:04.0 PCI bridge: PLX Technology, Inc. Device 8725 (rev ca)
c3:0b.0 PCI bridge: PLX Technology, Inc. Device 8725 (rev ca)
c3:0c.0 PCI bridge: PLX Technology, Inc. Device 8725 (rev ca)
c4:00.0 Bridge: NVIDIA Corporation Device 1af1 (rev a1)
c5:00.0 Bridge: NVIDIA Corporation Device 1af1 (rev a1)
c6:00.0 Bridge: NVIDIA Corporation Device 1af1 (rev a1)
c7:00.0 Bridge: NVIDIA Corporation Device 1af1 (rev a1)
c8:00.0 Bridge: NVIDIA Corporation Device 1af1 (rev a1)
c9:00.0 Bridge: NVIDIA Corporation Device 1af1 (rev a1)
ca:00.0 Non-Volatile memory controller: Samsung Electronics Co Ltd NVMe SSD Controller PM173X NVME6
cc:00.0 Infiniband controller: Mellanox Technologies MT28908 Family [ConnectX-6] IB3
cd:00.0 Mass storage controller: Broadcom / LSI Device c010 (rev b0)
ce:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function
ce:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
cf:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
cf:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
e0:00.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Root Complex
e0:00.2 IOMMU: Advanced Micro Devices, Inc. [AMD] Starship/Matisse IOMMU
e0:01.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
e0:02.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
e0:03.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
e0:03.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
e0:04.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
e0:05.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
e0:05.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge
e0:07.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
e0:07.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
e0:08.0 Host bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge
e0:08.1 PCI bridge: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B]
e1:00.0 Infiniband controller: Mellanox Technologies MT28908 Family [ConnectX-6]
e1:00.1 Infiniband controller: Mellanox Technologies MT28908 Family [ConnectX-6]
e2:00.0 Ethernet controller: Intel Corporation I210 Gigabit Network Connection (rev 03)
e3:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function
e3:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA
e4:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP
e4:00.2 Encryption controller: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PTDMA'''