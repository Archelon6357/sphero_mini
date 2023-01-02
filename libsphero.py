import asyncio
from bleak import BleakClient

from sphero_const   import *
from sphero_uuid    import *

address = "E7:A9:B0:C2:CD:7F"

class LibSphero():

    async def init(self, address):
        # self.disconnected_event = asyncio.Event()
        self.client = BleakClient(address)

        try:
            await self.client.connect()
            model_number = await self.client.read_gatt_char(UUID_MODEL_NBR)
            print("Model Number: {0}".format("".join(map(chr, model_number))))

            # 接続を10秒後に切断する機能をOFFにする
            await self.client.write_gatt_char(UUID_SPHERO_CHARACTERISTIC_ANTI_DOS ,"usetheforce...band".encode(), response=True)
            print("Enable connection continuity")

            # Sphero mini を 起動
            await self.wait(1.0)
            await self.resume()
            print("Awake sphero robot")

        except Exception as e:
            print(e)


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

    async def wait(self, sec = 0):
        await asyncio.sleep(sec)

    async def disconnect(self):
        print("disconnect.")
        await self.client.disconnect()


    async def setLightColor(self, red=0, green=0, blue=0):
        await self._write(
            uuid  = UUID_SPHERO_CHARACTERISTIC_HANDLE_1C,
            devID = deviceID['userIO'],
            cmdID = userIOCommandIDs["allLEDs"],
            data=[0x00, 0x0e, red, green, blue])


    async def move(self, vel=0, angle=0):

        if vel < 0:
            vel = -1*vel+256

        vel_MSByte      = (vel & 0xFF00) >> 8
        vel_LSByte      = vel & 0xFF
        angle_MSByte    = (angle & 0xFF00) >> 8
        angle_LSByte    = angle & 0xFF

        await self._write(
            uuid  = UUID_SPHERO_CHARACTERISTIC_HANDLE_1C,
            devID = deviceID["driving"],
            cmdID = drivingCommands["driveWithHeading"],
            data=[vel_LSByte, angle_MSByte, angle_LSByte, vel_MSByte])


    async def _write(self, uuid=None, devID=None, cmdID=None, data=[]):
        sendBytes = [sendPacketConstants["StartOfPacket"],
            sum([flags["requestsResponse"], flags["resetsInactivityTimeout"]]), 
            devID, 
            cmdID, 1] + data

        checksum = 0
        for num in sendBytes[1:]:
            checksum = (checksum + num) & 0xFF 
        checksum = 0xff - checksum 
        sendBytes += [checksum, sendPacketConstants["EndOfPacket"]] 

        output = b"".join([x.to_bytes(1, byteorder='big') for x in sendBytes])
        print(output)         

        await self.client.write_gatt_char(UUID_SPHERO_CHARACTERISTIC_HANDLE_1C, output, response = True)


# Test code 
async def main(address=None):
    sphero = LibSphero()
    
    await sphero.init(address)
    await sphero.resume()

    await sphero.wait(3.0)

    await sphero.setLightColor(255, 0, 0)
    await sphero.wait(1.0)
    await sphero.setLightColor(0, 255, 0)
    await sphero.wait(1.0)
    await sphero.setLightColor(0, 0, 255)
    await sphero.wait(1.0)

    # await asyncio.sleep(2.0)
    await sphero.sleep()

    await sphero.disconnect()


if __name__ == '__main__':
    asyncio.run(main(address))
   