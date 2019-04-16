"""
Server Program, author = jbr185, 66360439
"""
import socket
import select
from sys import exit
from time import localtime
from Packet import * #packet class for packet formatting, unpacking and access
from MyUtils import getCommandLineArgument #a module i use for personal programming, i'm using the 
                                           #getCommandlineArgument function i made

MONTHS = [      #month names for each language
    ["English",
    "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
    "November", "December"],
    ["Maori",
    "Kohitatea", "Hui-tanguru", "Poutu-te-rangi", "Paenga-whawha", "Haratua", "Pipiri", "Hongongoi",
    "Here-turi-koka", "Mahuru", "Whiringa-a-nuku", "Whiringa-a-rangi", "Hakihea"],
    ["German",
    "Januar", "Februar", "Marz", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober",
    "November", "Dezember"]
]
DTTEMPLATES = [      #text responses in each languages
    ["Today's date is {0} {1}, {2}", "The current time is {0}:{1}"],
    ["Ko te ra o tenei ra ko {0} {1}, {2}", "Ko te wa o tenei wa {0}:{1}"],
    ["Heute ist der {1}. {0} {2}", "Die Uhrzeit ist {0}:{1}"]
]

def getPorts():
    """
    Gets the port number from either the commandline arguments or by prompting the user
    """
    ports = []
    for i in range(3): #for the 3 ports we are interested in
        port = getCommandLineArgument(i, int, True, 1023, 64001, False)
        #get the commanline arguement as an int, bounded between 1023 and 64001 with no correction
        if not port: #if commandline value is invalid, prompt user and close
            print("port number {} is invalid, please try again".format(i))
            exit()
        if port in ports:
            print("port numbers need to be unique")
            exit()
        ports.append(port)
    return ports

def bindPorts(ports):
    """
    bind the sockets to the given port numbers
    """
    sockets = []
    for i in range(len(ports)):
        portSocket = socket.socket(type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP) #create a socket
        portSocket.bind(("localhost", ports[i])) #bind the socket to the port on the local host
        sockets.append(portSocket)
    return sockets
    
def getSocket(fileNo, sockets):
    """
    gets the socket from from the given list that corresponds to the given fileNo, and returns its index
    """
    for index, socket in enumerate(sockets): #get the socket and index
        if socket.fileno() == fileNo:
            return socket, index
    
def getPacket(portSocket):
    """
    This function gets the packet and user from the socket that was pinged
    """
    packet, user = portSocket.recvfrom(6) #6 bytes as that is the request packet length
    print("User = {}".format(user))
    try:
        packet = RequestPacket.unpack(packet)
        print(packet)
        return packet, user
    except PacketUnpackError as err: #if the packet is invalid
        print(err)
        return False
    
def sendResponse(portSocket, requestType, socketType, user):
    """
    This function prepares and sends a packet through the given socket to the given user, as the given language index
    """
    print("Preparing response...")
    year, month, day, hour, minute, _, _, _, _ = localtime() #we don't care about the last 4 values
    if requestType == 1: #date
        text = DTTEMPLATES[socketType][0].format(MONTHS[socketType][month], day, year)
        #take the template for the language of the port and format with the correct month, day and year
    else: #else time
        text = DTTEMPLATES[socketType][1].format(hour, minute)
        #take the template for the language of the port and format with the correct hour and minute
    if len(text) > 255: #fail if over 255 bytes
        print("The formatted text for the response is too long")
        return False
    print("Sending response... ")
    portSocket.sendto(ResponsePacket(MONTHS[socketType][0][:3].lower(), year, month, day, hour, minute, 
                                     text).getBytearray(), user) #prepare a response and send it
    print("Response sent")
    return True
    
    
def main():
    """
    here we set up the ports and listen to then, sending a response if the packet is valid
    """
    try:
        ports = getPorts()
        print("Binding ports... ")
        sockets = bindPorts(ports)
        print("Ports open")
        print("Listening...")
        users = [] #list for storing users
        socketFileNo = [] #templist for socket file numbers, as the select python class needs this
        for portSocket in sockets:
            socketFileNo.append(portSocket.fileno())
        while True:
            for fileNo in select.select(socketFileNo, [], [])[0]: #for each socket that receives a packet
                #[0] as this returns a tuble of the three input lists and we only care about the first
                portSocket, portIndex = getSocket(fileNo, sockets)
                print("Request received for socket {}, retreiving packet... ".format(MONTHS[portIndex][0]))
                packet, user = getPacket(portSocket)
                users.append(user)
                if not packet: #if the packet is invaild, skip this user
                    continue
                if not sendResponse(portSocket, packet.requestType, portIndex, user): #if the text is too long
                    continue
            print("Listening...")
    except (ConnectionResetError, PacketCompileError) as err: #if critical error occurs
        print(err)
        print("Closing ports...")
        for portSocket in sockets:
            portSocket.close()
        exit()

main()