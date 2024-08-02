import asyncio

async def handle_connection(reader, writer):
    """
    Handle incoming client connections.
    """
    data = await reader.read(100)
    message = data.decode()
    client_address = writer.get_extra_info('peername')

    print(f"Received '{message}' from {client_address}")

    writer.write(data)
    await writer.drain()

    print("Connection closed")
    writer.close()

async def start_servers():
    """
    Start the TCP servers for testing.
    """
    server1 = await asyncio.start_server(handle_connection, '127.0.0.1', 8888)
    server2 = await asyncio.start_server(handle_connection, '127.0.0.1', 9999)

    print(f'Serving on {server1.sockets[0].getsockname()}')
    print(f'Serving on {server2.sockets[0].getsockname()}')

    async with server1, server2:
        await asyncio.gather(server1.serve_forever(), server2.serve_forever())

if __name__ == "__main__":
    asyncio.run(start_servers())
