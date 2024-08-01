import pytest
import asyncio
from main import NetworkDevice, NetworkManager

@pytest.mark.asyncio
async def test_device_connection():
    """
    Test that a device can connect successfully.
    """
    device = NetworkDevice('127.0.0.1', 8888)
    await device.connect()
    assert device.reader is not None
    assert device.writer is not None
    device.disconnect()

@pytest.mark.asyncio
async def test_device_communication():
    """
    Test sending and receiving data with a device.
    """
    device = NetworkDevice('127.0.0.1', 8888)
    await device.connect()
    await device.send("Test Message")
    response = await device.receive()
    assert response == "Test Message"
    device.disconnect()

@pytest.mark.asyncio
async def test_network_manager():
    """
    Test the network manager's ability to handle multiple devices.
    """
    manager = NetworkManager()
    manager.add_device('127.0.0.1', 8888)
    manager.add_device('127.0.0.1', 9999)

    await manager.connect_all()
    await manager.send_all("Test Broadcast")
    responses = await manager.receive_all()

    for response in responses:
        assert response == "Test Broadcast"
