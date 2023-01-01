# Const value for sphero mini 


device = {
    "apiProcess"    : 0x10,
    "sysInfo"       : 0x11,
    "power"         : 0x13,
    "drive"         : 0x16,
    "sensor"        : 0x18,
    "userIO"        : 0x1a,
}




packetConstants = {
    "StartOfPacket" : 0x8d,       
    "EndOfPacket"   : 0xd8
    }         

flags= {
    "isResponse"                : 0x01,                         
    "requestsResponse"          : 0x02,                   
    "requestsOnlyErrorResponse" : 0x04,          
    "resetsInactivityTimeout"   : 0x08
    }            