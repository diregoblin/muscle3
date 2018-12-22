from typing import cast

from ymmsl import Reference

from libmuscle.mcp.message import Message
from libmuscle.mcp.client import Client
from libmuscle.mcp.direct_server import DirectServer, registered_servers


class DirectClient(Client):
    """A client that connects to an MCP server.

    This is a base class for MCP Clients. An MCP Client connects to
    an MCP Server over some lower-level communication protocol, and
    requests messages from it.
    """
    @staticmethod
    def can_connect_to(location: str) -> bool:
        """Whether DirectClient can connect to the given location.

        Args:
            location: The location to potentially connect to.

        Returns:
            True iff a DirectClient can connect to this location.
        """
        if not location.startswith('direct:'):
            return False
        server_id = location[7:]
        return server_id in registered_servers

    def __init__(self, location: str) -> None:
        """Create a DirectClient for a given location.

        The client will connect to this location and be able to request
        messages from any compute element and port represented by it.

        Args:
            location: A location string.
        """
        super().__init__(location)
        server_id = location[7:]
        self.__server = cast(DirectServer, registered_servers[server_id])

    def receive(self, receiver: Reference) -> Message:
        """Receive a message from a port this client connects to.

        Args:
            receiver: The receiving (local) port.

        Returns:
            The received message.
        """
        return self.__server.request(receiver)