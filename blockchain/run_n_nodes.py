from blockchain.node import Node

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run multiple blockchain nodes.")
    parser.add_argument(
        "--key_file_1",
        required=False,
        type=str,
        help="The path to the key file of the first node.",
        default="/home/mo/Documents/thesis/pos-blockchain/blockchain/keys/genesis_private_key.txt"
    )
    parser.add_argument(
        "--key_file_2",
        required=False,
        type=str,
        help="The path to the key file of the second node.",
        default="/home/mo/Documents/thesis/pos-blockchain/blockchain/keys/staker_private_key.txt"
    )
    parser.add_argument(
        "--n",
        required=True,
        type=int,
        help="The total number of nodes to run.",
    )
    args = parser.parse_args()

    if args.n < 2:
        raise ValueError("The total number of nodes must be at least 2.")

    ip = "0.0.0.0"
    node_port_start = 8010
    api_port_start = 8050

    # Create the first node with the first key file
    node1 = Node(ip, node_port_start, api_port_start, args.key_file_1)
    print(f"Started node 1 at {ip}:{node_port_start} with API port {api_port_start} and key file {args.key_file_1}")

    # Create the second node with the second key file
    node2 = Node(ip, node_port_start + 1, api_port_start + 1, args.key_file_2)
    print(f"Started node 2 at {ip}:{node_port_start + 1} with API port {api_port_start + 1} and key file {args.key_file_2}")

    # Create the remaining nodes without key files
    for i in range(2, args.n):
        node_port = node_port_start + i
        api_port = api_port_start + i
        node = Node(ip, node_port, api_port)
        print(f"Started node {i + 1} at {ip}:{node_port} with API port {api_port} without key file")
