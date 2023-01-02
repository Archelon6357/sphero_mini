import asyncio
import libsphero 

address = "E7:A9:B0:C2:CD:7F"

async def main(address=None):
    sphero = libsphero.LibSphero()
    
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