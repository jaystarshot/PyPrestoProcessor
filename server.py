from concurrent import futures
import grpc
import arrow_service_pb2
import arrow_service_pb2_grpc
from processor import process_presto_page

import logging

logging.basicConfig(level=logging.INFO)

# Define the service implementation
class ArrowServiceServicer(arrow_service_pb2_grpc.ArrowServiceServicer):
    def SendArrowArray(self, request, context):
        # Process the page using the function from the processor module
        processed_page = process_presto_page(request)
        return processed_page

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=[
        ('grpc.max_send_message_length', 50 * 1024 * 1024),
        ('grpc.max_receive_message_length', 50 * 1024 * 1024)
    ])

    # Add the service to the server
    arrow_service_pb2_grpc.add_ArrowServiceServicer_to_server(ArrowServiceServicer(), server)

    # Specify the port on which the server will listen
    server.add_insecure_port('[::]:50051')

    # Start the server
    server.start()
    print("gRPC server is running on port 50051...")

    # Keep the server running
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
