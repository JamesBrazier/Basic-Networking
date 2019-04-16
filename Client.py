"""
Client Program, author = jbr185, 66360439
"""
import socket
from sys import argv, exit
from Packet import * #packet class for packet formatting, unpacking and access
from MyUtils import getCommandLineArgument #a module i use for personal programming, i'm using the 
                                           #getCommandlineArgument function i made

def setup():
    """
    gets the commandline arguments using the getCommandLineArgument, and returns them.
    checks them for validity including with IPv4 format, if some are invalid closes the program
    """
    try:
        rsqtType = getCommandLineArgument(0)
        if not rsqtType or not rsqtType.lower() in ["date", "time"]: #if returned false or value not date or time, exit
            print("Request type invalid, please try again")
            exit()
        IPaddr = getCommandLineArgument(1)
        if IPaddr != "localhost" and socket.getaddrinfo(IPaddr, None)[0][0] != socket.AddressFamily.AF_INET: 
            #check if given IP is vaild or not an IPv4 (or localhost)
            print("this is not a IPv4 address, please try again")
            exit()
        port = getCommandLineArgument(2, int, True, 1023, 64001) #get port value as int, ensure between 1024 and 64000 inclusive
        if not port:
            print("Port number invaild, please try again")
            exit()
    except socket.gaierror: #if the IP format is invalid, exit
        print("IP invalid, please try again")
        exit()
    return rsqtType, IPaddr, port

def main():
    """
    Connects to host, sends a requestion and prints reply, then closes
    """
    try:
        sendSocket = None #so we can check if the program never opened it
        rsqtType, IPaddr, port = setup()
        print("Opening socket... ")
        sendSocket = socket.socket(type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP) #open socket with datagram and UDP
        print("Socket open")
        print("Sending data... ")
        sendSocket.sendto(RequestPacket(rsqtType).getBytearray(), (IPaddr, port)) #send a new request packet to the address
        print("Data sent")
        print("Waiting for response... ")
        sendSocket.settimeout(1) #set the timeout to one second
        packet, _ = sendSocket.recvfrom(268) #268 bytes as header + max 255 text bytes
        print("Response received, unpacking...")
        packet = ResponsePacket.unpack(packet)
        print(packet)
        exit()
    except (ConnectionResetError, PacketCompileError, socket.gaierror, socket.timeout) as err: 
        #if critical error occurs
        print(err)
        exit()
    finally:
        if sendSocket != None: #if we actually opened the socket, close it
            print("Closing connection...")
            sendSocket.close()
    
main()