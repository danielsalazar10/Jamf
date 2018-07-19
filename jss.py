"""
jss.py
Daniel Salazar
07/18/2018

This is an example of using python with the JAMF Software Server (JSS) REST API to update a static computer group
https://bryson3gps.wordpress.com/2014/03/30/the-jss-rest-api-for-everyone/
https://bryson3gps.wordpress.com/2014/04/08/the-jss-rest-api-for-everyone-part-2/

HTTP methods and their successful response:
1) GET retrieves data from a JSS resource for us to parse.
   200: Your request was successful.
   Returns the XML of the requested resource/object.

2) POST takes input XML from a variable or a file and creates a new JSS object for a resource.
   201: Your request to create or update an object was successful.
   Return the XML containing the ID of the object.

3) PUT takes input XML from a variable or a file and updates a JSS object.
   201: Your request to create or update an object was successful.
   Returns the XML containing the ID of the object.

4) DELETE will delete a JSS object.
   200: Your request was successful.
   Returns the XML containing the ID of the object with the tag “<successful>True</successful>”

Failed responses:
1) 400: There was something wrong with your request.
You should recheck the request and/or XML and reattempt the request.

2) 401: Your authentication for the request failed.
Check your credentials or check how they are being processed/handled.

3) 403: You have made a valid request, but you lack permissions to the object you are trying to interract with.
Check the permissions of the account being used in the JSS interface

4) 404: The JSS could not find the resource you were requesting.
Check the URL to the resource you are using.

5) 409: There was a conflict when your request was processed.
Check your XML and reattempt the request.

6) 500: This is a generic internal server error.
Something has gone wrong on the server end and is unrelated to your request.
"""
import requests
import base64
import xml.etree.ElementTree as ET
# ElementTree will not include the XML declaration line, so we have to concat the results to one
xmlDeclaration = '<?xml version="1.0" encoding="UTF-8"?>'

# Gets a response from the JSS API as input
# removes the computers matching USS-Enterprise
# returns string representing the modified xml
def removeComputer(response):
    # We need to convert the XML string we received in the response into an ElementTree object that we can work with
    computergroup = ET.fromstring(response.read())
    # make another ElementTree object that is just the ‘computers’ node of the ‘computergroup’ object we just created
    computers = computergroup.find('computers')
    # if we wanted to find and delete the computer named ‘USS-Enterprise’ we could
    # use the following code on the ‘computers’ object
    for computer in computers.findall('computer'):
        if computer.find('name').text == 'USS-Enterprise':
            computers.remove(computer)
    #  it will not include any computers named ‘USS-Enterprise’
    print(computergroup)
    # we will use ElementTree to build a new XML object and then copy the computers over
    NewXML = ET.Element('computer_group')
    NewXML_computers = ET.SubElement(NewXML, 'computers')
    # print out an empty computer group
    print(NewXML)
    # iterate over each computer in the source XML and copy them over
    for computer in computers.iter('computer'):
        NewXML_computers.append(computer)
    # Now we can output this into a string and make a PUT request to the JSS.
    return(xmlDeclaration + ET.tostring(NewXML))

# Gets a response from the JSS API as input
# Adds a computer group matching the name from the input
# returns string representing the modified xml
def addComputer(response):
    # retrieve the information of the computer
    Mac = ET.fromstring(response.read())
    # Create a new group
    NewMember = ET.Element('computer')
    NewMember_id = ET.SubElement(NewMember, 'id')
    NewMember_id.text = Mac.find('general/id').text
    NewMember_name = ET.SubElement(NewMember, 'name')
    NewMember_name.text = Mac.find('general/name').text
    NewMember_macadd = ET.SubElement(NewMember, 'mac_address')
    NewMember_macadd.text = Mac.find('general/mac_address').text
    NewMember_serial = ET.SubElement(NewMember, 'serial_number')
    NewMember_serial.text = Mac.find('general/serial_number').text
    NewXML = ET.Element('computer_group')
    NewXML_computers = ET.SubElement(NewXML, 'computers')
    NewXML_computers.append(Mac)
    return(xmlDeclaration + ET.tostring(NewXML))


def call(resource, username, password, method = '', data = None):
    request = urllib2.Request(resource)
    request.add_header('Authorization', 'Basic ' + base64.b64encode(username + ':' + password))
    if method.upper() in ('POST', 'PUT', 'DELETE'):
        request.get_method = lambda: method
    
    if method.upper() in ('POST', 'PUT') and data:
        request.add_header('Content-Type', 'text/xml')
        return urllib2.urlopen(request, data)
    else:
        return urllib2.urlopen(request)

if __name__ == '__main__':
    """
    Example of HTTP Requests:
    userdata = {"username":"myAccountUsername", "password":"myAccountPassword"}
    resp = requests.get('https://myjss.com/JSSResource/', userdata)
    resp = requests.post('https://myjss.com/JSSResource/', userdata)
    resp = requests.put('https://myjss.com/JSSResource/', userdata)
    resp = requests.delete('https://myjss.com/JSSResource/', userdata)
    
    Example of what a response xml would look like:
    f = open("jss_data.xml", "r")
    if f.mode == 'r':
        response = f.read()
        print(response)
    """


