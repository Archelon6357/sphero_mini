import asyncio
from bleak import BleakClient

from sphero_const   import *
from sphero_uuid    import *

address = "E7:A9:B0:C2:CD:7F"

# async def main(address):
#     async with BleakClient(address) as client:
#         model_number = await client.read_gatt_char(MODEL_NBR_UUID)
#         print("Model Number: {0}".format("".join(map(chr, model_number))))

async def main(address):

    # disconnected_event = asyncio.Event()

    def disconnected_callback(client):
        print("Disconnected callback called!")
        disconnected_event.set()

    async with BleakClient(address, disconnected_callback = disconnected_callback) as client:
        
        # 接続を10秒後に切断する機能をOFFにする
        await client.write_gatt_char(UUID_SPHERO_CHARACTERISTIC_ANTI_DOS ,"usetheforce...band".encode(), response=True)


        # sphero mini を 起こす．
        sendBytes = [sendPacketConstants["StartOfPacket"],
            sum([flags["requestsResponse"], flags["resetsInactivityTimeout"]]), 
            deviceID["powerInfo"], 
            powerCommandIDs["wake"], 1]

        checksum = 0
        for num in sendBytes[1:]:
            checksum = (checksum + num) & 0xFF # bitwise "and to get modulo 256 sum of appropriate bytes
        checksum = 0xff - checksum # bitwise 'not' to invert checksum bits
        sendBytes += [checksum, 0xd8] # concatenate

        output = b"".join([x.to_bytes(1, byteorder='big') for x in sendBytes])
        print(output)         

        await client.write_gatt_char(UUID_SPHERO_CHARACTERISTIC_HANDLE_1C, output, response = True)

        # 2秒待機
        await asyncio.sleep(2.0)

        # sphero mini を DeepSleep mode にする．
        sendBytes = [sendPacketConstants["StartOfPacket"],
                    sum([flags["requestsResponse"], flags["resetsInactivityTimeout"]]), 
                    deviceID["powerInfo"], 
                    powerCommandIDs["sleep"], 1]

        checksum = 0
        for num in sendBytes[1:]:
            checksum = (checksum + num) & 0xFF # bitwise "and to get modulo 256 sum of appropriate bytes
        checksum = 0xff - checksum # bitwise 'not' to invert checksum bits
        sendBytes += [checksum, 0xd8] # concatenate

        output = b"".join([x.to_bytes(1, byteorder='big') for x in sendBytes])
        print(output)         

        await client.write_gatt_char(UUID_SPHERO_CHARACTERISTIC_HANDLE_1C, output, response = True)        

        # sendBytes = [sendPacketConstants["StartOfPacket"],
        #      sum([flags["requestsResponse"], flags["resetsInactivityTimeout"]]), 
        #      deviceID["powerInfo"], 
        #      powerCommandIDs["wake"], 1]

        # self._send(characteristic=self.API_V2_characteristic,
        #     devID=deviceID['powerInfo'],
        #     commID=powerCommandIDs["wake"],
        #     payload=[]) # empty payload        
        # await 

# async def main(address):
#     async with BleakClient(address) as client:
#         red =   255
#         green = 255
#         blue = 0

#         sendBytes = [0x8d, 0x0a, 0x1a, 0x0e, 1] + [0x00, 0x0e, red, green, blue]

#         checksum = 0
#         for num in sendBytes[1:]:
#             checksum = (checksum + num) & 0xFF # bitwise "and to get modulo 256 sum of appropriate bytes
#         checksum = 0xff - checksum # bitwise 'not' to invert checksum bits
#         sendBytes += [checksum, 0xd8] # concatenate

#         output = b"".join([x.to_bytes(1, byteorder='big') for x in sendBytes])

#         print(output)

#         await client.write_gatt_char(UUID_SPHERO_CHARACTERISTIC_HANDLE_1C, output, response = True)


asyncio.run(main(address))


