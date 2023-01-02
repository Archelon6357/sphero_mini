import asyncio
from bleak import BleakClient

from sphero_const   import *
from sphero_uuid    import *

address = "E7:A9:B0:C2:CD:7F"

class LibSphero():

    async def init(self, address):
        self.client = None
        self.disconnected_event = asyncio.Event()

        async with BleakClient(address, disconnected_callback = self.disconnected_callback) as self.client:
            
            # 接続を10秒後に切断する機能をOFFにする
            await self.client.write_gatt_char(UUID_SPHERO_CHARACTERISTIC_ANTI_DOS ,"usetheforce...band".encode(), response=True)


    def disconnected_callback(self, client):
        print("Disconnected callback called!")
        self.disconnected_event.set()

    async def resume(self):         # sphero mini を 起こす．

        await self._write(
            uuid  = UUID_SPHERO_CHARACTERISTIC_HANDLE_1C,
            devID = deviceID["powerInfo"],
            cmdID = powerCommandIDs["wake"],
            data=[])

    async def sleep(self):

        await self._write(
            uuid  = UUID_SPHERO_CHARACTERISTIC_HANDLE_1C,
            devID = deviceID["powerInfo"],
            cmdID = powerCommandIDs["sleep"],
            data=[])

    async def _write(self, uuid=None, devID=None, cmdID=None, data=[]):
        sendBytes = [sendPacketConstants["StartOfPacket"],
            sum([flags["requestsResponse"], flags["resetsInactivityTimeout"]]), 
            devID, 
            cmdID, 1]

        checksum = 0
        for num in sendBytes[1:]:
            checksum = (checksum + num) & 0xFF 
        checksum = 0xff - checksum 
        sendBytes += [checksum, sendPacketConstants["EndOfPacket"]] 

        output = b"".join([x.to_bytes(1, byteorder='big') for x in sendBytes])
        print(output)         

        await self.client.write_gatt_char(UUID_SPHERO_CHARACTERISTIC_HANDLE_1C, output, response = True)

async def main(address=None):
    sphero = LibSphero()
    
    await sphero.init(address)
    await sphero.resume()

    await asyncio.sleep(2.0)
    await sphero.sleep()


if __name__ == '__main__':
    asyncio.run(main(address))
   