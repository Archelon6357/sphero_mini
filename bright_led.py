# Sample code for emitting the main LEDs (order: red->green->blue)

import asyncio
import libsphero 

address = ""

async def main(address=None):
    sphero = libsphero.LibSphero()
    
    await sphero.init(address)

    await sphero.wait(3.0)

    await sphero.setLightColor(255, 0, 0)   # Set LED color : red
    await sphero.wait(1.0)
    await sphero.setLightColor(0, 255, 0)   # Set LED color : green
    await sphero.wait(1.0)
    await sphero.setLightColor(0, 0, 255)   # Set LED color : blue
    await sphero.wait(1.0)

    # await asyncio.sleep(2.0)
    await sphero.sleep()

    await sphero.disconnect()


if __name__ == '__main__':
    asyncio.run(main(address))