import asyncio
from bleak import BleakClient

from const import *

address = "E7:A9:B0:C2:CD:7F"

MODEL_NBR_UUID = "00002a00-0000-1000-8000-00805f9b34fb"

UUID_SPHERO_CHARACTERISTIC_HANDLE_1C = "00010002-574f-4f20-5370-6865726f2121"
UUID_SPHERO_CHARACTERISTIC_ANTI_DOS = "00020005-574f-4f20-5370-6865726f2121"

# async def main(address):
#     async with BleakClient(address) as client:
#         model_number = await client.read_gatt_char(MODEL_NBR_UUID)
#         print("Model Number: {0}".format("".join(map(chr, model_number))))


async def main(address):
    async with BleakClient(address) as client:
        
        await client.write_gatt_char(UUID_SPHERO_CHARACTERISTIC_ANTI_DOS ,"usetheforce...band".encode(), response=True)

        sendBytes = [0x8d, sum([0x02, 0x08]), 0x13, 0x0D, 1]

        checksum = 0
        for num in sendBytes[1:]:
            checksum = (checksum + num) & 0xFF # bitwise "and to get modulo 256 sum of appropriate bytes
        checksum = 0xff - checksum # bitwise 'not' to invert checksum bits
        sendBytes += [checksum, 0xd8] # concatenate

        output = b"".join([x.to_bytes(1, byteorder='big') for x in sendBytes])
        print(output)         

        await client.write_gatt_char(UUID_SPHERO_CHARACTERISTIC_HANDLE_1C, output, response = True)


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

