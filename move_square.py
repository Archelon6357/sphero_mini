import asyncio
import libsphero 

address = "E7:A9:B0:C2:CD:7F"

async def main(address=None):
    sphero = libsphero.LibSphero()
    
    await sphero.init(address)

    await sphero.wait(2.0)
    await sphero.setLightColor(255, 255, 0)
    
    # Move to forward
    await sphero.move(80, 0)
    await sphero.wait(1.5)
    await sphero.move(0, 0)
    await sphero.wait(0.5)

    # Move to right
    await sphero.move(80, 90)
    await sphero.wait(1.5)
    await sphero.move(0, 0)
    await sphero.wait(0.5)

    # Move to backward
    await sphero.move(80, 180)
    await sphero.wait(1.5)
    await sphero.move(0, 0)
    await sphero.wait(0.5)

    # Move to left
    await sphero.move(80, 270)
    await sphero.wait(1.5)
    await sphero.move(0, 0)
    await sphero.wait(0.5)

    # Turn off and disconnect
    await sphero.sleep()
    await sphero.disconnect()


if __name__ == '__main__':
    asyncio.run(main(address))