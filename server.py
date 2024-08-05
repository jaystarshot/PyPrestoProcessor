from concurrent import futures
import grpc
import presto_pb2
import presto_pb2_grpc
from processor import process_presto_page

class PrestoServiceServicer(presto_pb2_grpc.PrestoServiceServicer):
    def ProcessPage(self, request, context):
        processed_page = process_presto_page(request)
        return processed_page

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    presto_pb2_grpc.add_PrestoServiceServicer_to_server(PrestoServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
