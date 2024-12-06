import logging
import os
import numpy as np
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, Index, utility
from els.logging import add_logger_function

@add_logger_function
def get_or_create_collection(milvus_host="localhost", milvus_port="19530", overwrite=False):
    # Connect to Milvus
    connections.connect("default", host=milvus_host, port=milvus_port)

    # Define the collection name
    collection_name = "els"

    # Check if the collection exists
    if utility.has_collection(collection_name):
        if overwrite:
            logger.info(f"Collection '{collection_name}' already exists. Deleting...")
            utility.drop_collection(collection_name)
        else:
            logger.info(f"Collection '{collection_name}' already exists.")
            return Collection(name=collection_name)
    logger.info(f"Collection '{collection_name}' does not exist. Creating...")

    # Define the schema for the collection
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),  # Adjust `dim` as needed
        FieldSchema(name="path", dtype=DataType.VARCHAR, is_primary=False, auto_id=False, max_length=255),
    ]
    schema = CollectionSchema(fields, description="ELS collection for embeddings")

    # Create the collection
    collection = Collection(name=collection_name, schema=schema)

    # Create an index for efficient vector search
    index_params = {
        "index_type": "IVF_FLAT",  # Adjust index type based on your requirements (e.g., IVF_FLAT, HNSW)
        "metric_type": "L2",       # Adjust metric (e.g., L2, IP, COSINE) based on your embedding type
        "params": {"nlist": 384}   # Adjust nlist parameter for your dataset
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    logger.info(f"Collection '{collection_name}' created successfully.")

    # Return the collection connection
    return collection

class milvus():
    def __init__(self, host=..., port=..., clean=False):
        self.logger = logging.getLogger(f"{__class__}")
        self.logger.info("Initializing Milvus Connection")
        if host == ...:
            self.host = os.getenv("ELS_MILVUS_HOST", "localhost")
        if port == ...:
            self.port = os.getenv("ELS_MILVUS_PORT", "19530")
        self.collection = get_or_create_collection(milvus_host = self.host, milvus_port = self.port, overwrite=clean)
        self.logger.info("Connection Established")

    def embed_vector(self, vector: list, path: str):
        """
        Embeds a vector into the Milvus collection with an associated path.

        Args:
            collection (Collection): The Milvus collection object.
            vector (list): The vector to be embedded.
            path (str): The associated path string (max length 255).

        Returns:
            list: IDs of the inserted vectors.
        """
        # Validate path length
        if len(path) > 255:
            raise ValueError("The 'path' field exceeds the maximum length of 255 characters.")

        # Prepare the data for insertion
        data = [
            [vector.tolist()],  # Embedding vector
            [path],  # Path field (list because Milvus expects columnar data)
        ]

        # Insert data into the collection
        result = self.collection.insert(data)

        # Return the IDs of the inserted vectors
        return result.primary_keys

    def search_vectors_within_radius(self, query_vector, radius=1, metric_type="L2", nprobe=10):
        """
        Searches for vectors within a specified radius and returns the paths of matching records.

        Args:
            collection (Collection): The Milvus collection to search.
            query_vector (list): The vector to search for.
            radius (float): The distance radius to search within.
            metric_type (str): The metric type used for similarity ("L2", "IP", "COSINE").
            nprobe (int): Number of probe clusters for searching (affects search speed/accuracy).

        Returns:
            list: A list of paths for vectors within the specified radius.
        """
        # Define search parameters
        search_params = {"metric_type": metric_type, "params": {"nprobe": nprobe}}
        
        # Perform the search
        results = self.collection.search(
            data=[query_vector],  # Query vector (must be a list of vectors)
            anns_field="embedding",  # Field name for embeddings
            param=search_params,
            limit=10,  # Max number of results to return
            expr=None,  # Distance filter to enforce radius
            output_fields=["path"],  # Include the "path" field in the results,
            consistency_level="Strong"
        )
        
        # Extract paths from the search results
        paths = []
        for hits in results:
            for hit in hits:
                paths.append(hit.entity.get("path"))

        return paths

    def list_all_paths(self):
        """
        Retrieves all the paths stored in the collection.

        Args:
            collection (Collection): The Milvus collection to query.

        Returns:
            list: A list of all paths in the collection.
        """
        # Use a query to retrieve all paths
        self.collection.load()
        results = self.collection.query(expr="", output_fields=["path"], limit=1000)
        
        # Extract paths from the results
        paths = [result["path"] for result in results]
        return paths




if __name__ == "__main__":
    from els.logging import setup_logging
    setup_logging()
    db = milvus()
