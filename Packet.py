"""
Packet Module author = jbr185, 66360439
"""
class RequestPacket():
    """
    The RequestPacket class, used for packing and unpacking request packets
    """
    def __init__(self, requestType):
        self.magicNo = 0x497E
        self.packetType = 1 #this is a request packet     
        if type(requestType) == int and requestType > 0 and requestType <= 2: #if the type is a valid int
            self.requestType = requestType
        elif type(requestType) == str: #if the type is a valid string
            if requestType.lower() == "date":
                self.requestType = 1
            elif requestType.lower() == "time":
                self.requestType = 2
        else: #if not raise a compile error
            raise PacketCompileError("[PacketCompileError] Invaild requestType given")
        
    def __str__(self):
        """
        turn the field values for this packet into a string
        """
        return "Packet field values = {}, {}, {}".format(self.magicNo, self.packetType, self.requestType)
        
    def getBytearray(self):
        """
        turn this packet into a bytearray for sending
        """
        return bytearray([0x49, 0x7E, 0, 1, 0, self.requestType])
    
    def unpack(packet):
        """
        unpacks a given bytearray into request packet form whilst checking for invalid fields
        """
        if len(packet) != 6: #if the packet is too long
            raise PacketUnpackError("[PacketUnpackError] Packet size invalid")
        if (packet[0] * 256) + packet[1] != 0x497E: #if the magic number is incorrect
            #the first byte * 256 + the second gets the original value
            raise PacketUnpackError("[PacketUnpackError] Invaild magic number")
        if (packet[2] * 256) + packet[3] != 1: #if the type is not request type
            raise PacketUnpackError("[PacketUnpackError] Invalid packet type; not of type RequestPacket")
        if (packet[4] * 256) + packet[5] < 0 or (packet[4] * 256) + packet[5] > 2: #if the request type is invalid
            raise PacketUnpackError("[PacketUnpackError] Invalid requestType ({})".format((packet[4] * 256) + packet[5]))
        return RequestPacket((packet[4] * 256) + packet[5]) #return a RequestPacket object with the values
    
    
class ResponsePacket():
    """
    The ResponsePacket class, used for packing and unpacking response packets
    """    
    def __init__(self, languageCode, year, month, day, hour, minute, text):
        self.magicNo = 0x497E
        self.packetType = 2 #this is a response packet
        if type(languageCode) == int and languageCode > 0 and languageCode <= 3: #if the language code is a valid int
            self.languageCode = languageCode
        elif type(languageCode) == str: #if the language code is a valid string
            if languageCode.lower()[:3] == "eng":
                self.languageCode = 1
            elif languageCode.lower()[:3] == "mao":
                self.languageCode = 2
            elif languageCode.lower()[:3] == "ger":
                self.languageCode = 3
        else: #if not throw a compile error
            raise PacketCompileError("[PacketCompileError] Invalid language code given")
        if year > 0 and year.bit_length() <= 16: #if the year is a valid byte size
            self.year = year
        else:
            raise PacketCompileError("[PacketCompileError] Invalid year given")
        if month > 0 and month < 12: #if the month is valid
            self.month = month
        else:
            raise PacketCompileError("[PacketCompileError] Invalid month given")        
        if day > 0 and day <= 31: #if the day is valid
            self.day = day
        else:
            raise PacketCompileError("[PacketCompileError] Invalid day given")        
        if hour >= 0 and hour <= 23: #if the hour is valid
            self.hour = hour
        else:
            raise PacketCompileError("[PacketCompileError] Invalid hour given")        
        if minute >= 0 and minute <= 59: #if the minute is valid
            self.minute = minute
        else:
            raise PacketCompileError("[PacketCompileError] Invalid minute given")        
        self.payload = text
        self.length = len(self.payload) #get the length of the payload
        
    def __str__(self):
        """
        turn the packet into a string of its field values
        """
        return "Packet field values = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(self.magicNo, self.packetType, 
                    self.languageCode, self.year, self.month, self.day, self.hour, self.minute, self.length, self.payload)
        
    def getBytearray(self):
        """
        turn the packet into a byte array
        """
        yearByte1 = self.year // 256 #as the year can take two bytes, we split the value
        yearByte2 = self.year % 256
        return bytearray([0x49, 0x7E, 0, 2, 0, self.languageCode, yearByte1, yearByte2, self.month, 
                          self.day, self.hour, self.minute, self.length]) + self.payload.encode()
        
    def unpack(packet):
        """
        unpacks a given bytearray into response packet form whilst checking for invalid fields
        """
        if len(packet) < 13: #if the packet isn't even long enough for our header
            raise PacketUnpackError("[PacketUnpackError] Packet size invalid")
        if (packet[0] * 256) + packet[1] != 0x497E:
            raise PacketUnpackError("[PacketUnpackError] Packet magic number")
        if (packet[2] * 256) + packet[3] != 2: #if is isn't a response packet
            raise PacketUnpackError("[PacketUnpackError] Invalid packet type; not of type ResponsePacket")
        if (packet[4] * 256) + packet[5] < 0 or (packet[4] * 256) + packet[5] > 3: #if the language code is invalid
            raise PacketUnpackError("[PacketUnpackError] Invalid languageCode ({})".format((packet[4] * 256) + packet[5]))
        if (packet[6] * 256) + packet[7] >= 2100: #if the year is too far in the future (we don't want those damn time travellers!)
            raise PacketUnpackError("[PacketUnpackError] Invalid year ({})".format((packet[6] * 256) + packet[7]))
        if packet[8] < 1 or packet[8] > 12: #if the month is invalid
            raise PacketUnpackError("[PacketUnpackError] Invalid month ({})".format(packet[8]))  
        if packet[9] < 1 or packet[9] > 31: #if the day is invalid
            raise PacketUnpackError("[PacketUnpackError] Invalid day ({})".format(packet[9]))
        if packet[10] < 0 or packet[10] > 23: #if the hour is invalid
            raise PacketUnpackError("[PacketUnpackError] Invalid hour ({})".format(packet[10]))
        if packet[11] < 0 or packet[11] > 59: #if the minute is invalid
            raise PacketUnpackError("[PacketUnpackError] Invalid minute ({})".format(packet[11]))
        if len(packet) != packet[12] + 13: #if the size is incorrect
            raise PacketUnpackError("[PacketUnpackError] Incorrect length field: {} != {}".format(len(packet) - 13, packet[12]))
        return ResponsePacket((packet[4] * 256) + packet[5], (packet[6] * 256) + packet[7], packet[8], packet[9], packet[10], 
                    packet[11], packet[13:].decode()) #create a new response packet based on the values
        
        
class PacketUnpackError(ValueError):
    """
    class for packet unpacking errors
    """
    def __init__(self, text):
        super()
        
        
class PacketCompileError(ValueError):
    """
    calss for packet creation errors
    """
    def __init__(self, text):
        super()
        
        