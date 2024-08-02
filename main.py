import asyncio

class NetworkDevice:
    """
    A class to manage a network device connection.
    """
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        """
        Connect to the network device.
        """
        self.reader, self.writer = await asyncio.open_connection(self.address, self.port)

    async def receive(self):
        """
        Receive data from the device.
        """
        data = await self.reader.read(100)
        return data.decode()

    async def send(self, message):
        """
        Send a message to the device.
        """
        self.writer.write(message.encode())
        await self.writer.drain()

    def disconnect(self):
        """
        Close the connection to the device.
        """
        self.writer.close()

class NetworkManager:
    """
    A class to manage multiple network devices.
    """
    def __init__(self):
        self.devices = []

    def add_device(self, address, port):
        """
        Add a device to the manager.
        """
        device = NetworkDevice(address, port)
        self.devices.append(device)
        return device

    async def connect_all(self):
        """
        Connect to all managed devices.
        """
        await asyncio.gather(*(device.connect() for device in self.devices))

    async def receive_all(self):
        """
        Receive data from all managed devices.
        """
        return await asyncio.gather(*(device.receive() for device in self.devices))

    async def send_all(self, message):
        """
        Send a message to all managed devices.
        """
        await asyncio.gather(*(device.send(message) for device in self.devices))

async def run_manager():
    """
    Run the network manager to connect, send, and receive data.
    """
    manager = NetworkManager()
    manager.add_device('127.0.0.1', 8888)
    manager.add_device('127.0.0.1', 9999)

    await manager.connect_all()
    await manager.send_all("Greetings from client!")
    responses = await manager.receive_all()

    for response in responses:
        print(response)

if __name__ == "__main__":
    asyncio.run(run_manager())
