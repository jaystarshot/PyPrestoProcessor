# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: arrow_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13\x61rrow_service.proto\x12\x0c\x61rrowservice\"!\n\x11\x41rrowArrayRequest\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"\"\n\x12\x41rrowArrayResponse\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x32\x63\n\x0c\x41rrowService\x12S\n\x0eSendArrowArray\x12\x1f.arrowservice.ArrowArrayRequest\x1a .arrowservice.ArrowArrayResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'arrow_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ARROWARRAYREQUEST']._serialized_start=37
  _globals['_ARROWARRAYREQUEST']._serialized_end=70
  _globals['_ARROWARRAYRESPONSE']._serialized_start=72
  _globals['_ARROWARRAYRESPONSE']._serialized_end=106
  _globals['_ARROWSERVICE']._serialized_start=108
  _globals['_ARROWSERVICE']._serialized_end=207
# @@protoc_insertion_point(module_scope)
