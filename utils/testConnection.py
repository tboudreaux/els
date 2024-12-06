from pymilvus import connections, utility

# Update with your Milvus instance details
MILVUS_HOST = "10.17.1.164"  # Replace with your host, e.g., "127.0.0.1"
MILVUS_PORT = "19530"      # Replace with your port, default is 19530

def test_milvus_connection():
    try:
        # Connect to Milvus
        connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
        print(f"Connected to Milvus at {MILVUS_HOST}:{MILVUS_PORT}")

        # Check if the server is healthy
        if utility.has_collection("_default"):
            print("Milvus server is healthy.")
        else:
            print("Milvus is running, but the default collection is missing (this is fine for a new server).")
        
    except Exception as e:
        print(f"Failed to connect to Milvus: {e}")
    finally:
        # Disconnect from Milvus
        connections.disconnect("default")

if __name__ == "__main__":
    test_milvus_connection()

