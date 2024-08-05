import grpc
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import presto_pb2
import presto_pb2_grpc
import base64

app = FastAPI()

class GrpcSerializedPage(BaseModel):
    sliceBytes: str
    positionCount: int
    uncompressedSizeInBytes: int
    pageCodecMarkers: str
    checksum: int

@app.post("/process", response_model=GrpcSerializedPage)
async def process(page: GrpcSerializedPage):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = presto_pb2_grpc.PrestoServiceStub(channel)
        grpc_page = presto_pb2.GrpcSerializedPage(
            sliceBytes=base64.b64decode(page.sliceBytes),
            positionCount=page.positionCount,
            uncompressedSizeInBytes=page.uncompressedSizeInBytes,
            pageCodecMarkers=base64.b64decode(page.pageCodecMarkers),
            checksum=page.checksum
        )
        response = stub.ProcessPage(grpc_page)
        return GrpcSerializedPage(
            sliceBytes=base64.b64encode(response.sliceBytes).decode('utf-8'),
            positionCount=response.positionCount,
            uncompressedSizeInBytes=response.uncompressedSizeInBytes,
            pageCodecMarkers=base64.b64encode(response.pageCodecMarkers).decode('utf-8'),
            checksum=response.checksum
        )
