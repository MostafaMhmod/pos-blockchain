import json
import socket

from p2pnetwork.node import Node

from ..utils.helpers import BlockchainUtils
from ..utils.logger import logger

from typing import Dict, List, Any
import os
import threading
import time

class SocketConnector:
    """Handles socket connections between nodes."""

    def __init__(self, ip: str, port: int) -> None:
        """
        Initialize a socket connector.
        
        """
        self.ip = ip
        self.port = port
        self.use_docker = os.environ.get("USE_DOCKER", False)
        if self.use_docker:
            self.docker_ip = self.docker_node_mapping()[self.port]

    def get_docker_node_ports(self) -> List[int]:
        """
        Get the Docker node ports from environment variables.
        
        """
        return [int(i) for i in os.environ.get("DOCKER_NODE_PORTS", "").split(",") if i]

    def get_docker_node_container_names(self) -> List[str]:
        """
        Get the Docker node container names from environment variables.
        
        Returns:
            List of Docker node container names
        """
        return os.environ.get("DOCKER_NODE_CONTAINER_NAMES", "").split(",") if os.environ.get("DOCKER_NODE_CONTAINER_NAMES") else []

    def first_node_config(self) -> Dict[str, Any]:
        """
        Get the configuration for the first node.
        
        """
        if self.use_docker:
            ports = self.get_docker_node_ports()
            names = self.get_docker_node_container_names()
            if ports and names:
                return {
                    "port": ports[0],
                    "ip": names[0],
                }
        return {"port": int(os.environ.get("FIRST_NODE_PORT", 9010)), "ip": "localhost"}

    def docker_node_mapping(self) -> Dict[int, str]:
        """
        Create a mapping of Docker node ports to container names.
        
        """
        docker_node_ports = self.get_docker_node_ports()
        docker_node_container_names = self.get_docker_node_container_names()
        return {
            int(port): name
            for port, name in zip(docker_node_ports, docker_node_container_names)
        }

    def equals(self, connector: 'SocketConnector') -> bool:
        """
        Check if this connector equals another connector.
        
        """
        if connector.ip == self.ip and connector.port == self.port:
            return True
        return False

class Message:
    """Represents a message in the P2P network."""

    def __init__(self, sender_connector: SocketConnector, message_type: str, data: Any) -> None:
        """
        Initialize a message.
        
        Args:
            sender_connector: Connector of the sender
            message_type: Type of the message
            data: Data contained in the message
        """
        self.sender_connector = sender_connector
        self.message_type = message_type
        self.data = data

class PeerDiscoveryHandler:
    """Handles peer discovery in the P2P network."""

    def __init__(self, node) -> None:
        """
        Initialize the peer discovery handler.
        
        """
        self.socket_communication = node
        self.use_docker = os.environ.get("USE_DOCKER", False)

    def start(self) -> None:
        """Start the peer discovery process."""
        status_thread = threading.Thread(target=self.status, args=())
        status_thread.start()
        discovery_thread = threading.Thread(target=self.discovery, args=())
        discovery_thread.start()

    def status(self) -> None:
        """Report the status of node connections."""
        count = 1
        while True:
            current_connections = []
            self.socket_communication.node.blockchain.peers = [self.socket_communication.socket_connector] + self.socket_communication.peers 
            for peer in self.socket_communication.peers:
                current_connections.append(f"{peer.ip}: {peer.port}")
            if not self.socket_communication.peers:
                logger.info({"message": "No nodes connected"})
            else:
                logger.info(
                    {
                        "message": "Node connection status",
                        "connections": f"Current connections: {current_connections}",
                        "whoami": self.socket_communication,
                    }
                )
            count += 1
            sleep_time = 15 if count < 10 else 600  # prevent excessive logging
            time.sleep(sleep_time)

    def discovery(self) -> None:
        """Discover new peers in the network."""
        while True:
            handshake_message = self.handshake_message()
            self.socket_communication.broadcast(handshake_message)
            time.sleep(10)

    def handshake(self, connected_node) -> None:
        """
        Perform a handshake with a connected node.
        
        """
        handshake_message = self.handshake_message()
        self.socket_communication.send(connected_node, handshake_message)

    def handshake_message(self) -> Any:
        """
        Create a handshake message.

        """
        connector_self = self.socket_communication.socket_connector
        peers_self = self.socket_communication.peers
        data = peers_self
        message_type = "DISCOVERY"
        message = Message(connector_self, message_type, data)
        encoded_message = BlockchainUtils.encode(message)
        return encoded_message

    def handle_message(self, message: Message) -> None:
        """
        Handle a peer discovery message.
        
        """
        peers_socket_connector = message.sender_connector
        peers_peer_list = message.data

        if not any(
            peer.equals(peers_socket_connector)
            for peer in self.socket_communication.peers
        ):
            self.socket_communication.peers.append(peers_socket_connector)

        for peers_peer in peers_peer_list:
            peer_known = False

            for peer in self.socket_communication.peers:
                if peer.equals(peers_peer):
                    peer_known = True

            if not peer_known and not peers_peer.equals(
                self.socket_communication.socket_connector
            ):
                ip = peers_peer.ip
                if self.use_docker:
                    ip = peers_peer.docker_ip
                self.socket_communication.connect_with_node(ip, peers_peer.port)

class SocketCommunication(Node):
    """Handles socket communication between nodes."""

    def __init__(self, ip: str, port: int) -> None:
        """
        Initialize socket communication.
        
        """
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []
        self.peer_discovery_handler = PeerDiscoveryHandler(self)
        self.socket_connector = SocketConnector(ip, port)

    def init_server(self) -> None:
        """Initialize the server socket."""
        logger.info(
            {
                "message": f"Node initialisation on port: {self.port}",
                "node": {"id": self.id, "ip": self.host, "port": self.port},
            }
        )
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(10.0)
        self.sock.listen(1)

    def connect_to_first_node(self) -> None:
        """Connect to the first node in the network."""
        port = self.socket_connector.first_node_config()["port"]
        ip = self.socket_connector.first_node_config()["ip"]
        if self.socket_connector.port != port:
            self.connect_with_node(ip, port)

    def start_socket_communication(self, node) -> None:
        """
        Start socket communication.
        """
        self.node = node
        self.start()
        self.peer_discovery_handler.start()
        self.connect_to_first_node()

    def inbound_node_connected(self, connected_node) -> None:
        """
        Handle an inbound node connection.
        """
        self.peer_discovery_handler.handshake(connected_node)

    def outbound_node_connected(self, connected_node) -> None:
        """
        Handle an outbound node connection.
        
        """
        self.peer_discovery_handler.handshake(connected_node)

    def node_message(self, connected_node, message: Any) -> None:
        """
        Handle a message from a node.
        
        """
        message = BlockchainUtils.decode(json.dumps(message))
        if message.message_type == "DISCOVERY":
            self.peer_discovery_handler.handle_message(message)
        elif message.message_type == "TRANSACTION":
            transaction = message.data
            self.node.handle_transaction(transaction)
        elif message.message_type == "BLOCK":
            block = message.data
            self.node.handle_block(block)
        elif message.message_type == "BLOCKCHAINREQUEST":
            self.node.handle_blockchain_request(connected_node)
        elif message.message_type == "BLOCKCHAIN":
            blockchain = message.data
            self.node.handle_blockchain(blockchain)

    def send(self, receiver, message: Any) -> None:
        """
        Send a message to a receiver.
        
        """
        self.send_to_node(receiver, message)

    def broadcast(self, message: Any) -> None:
        """
        Broadcast a message to all connected nodes.

        """
        self.send_to_nodes(message)