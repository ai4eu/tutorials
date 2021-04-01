# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: classifier_model.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='classifier_model.proto',
  package='know_center.openml.Classifier',
  syntax='proto3',
  serialized_options=b'B\017ClassifierProto\242\002\002KC',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16\x63lassifier_model.proto\x12\x1dknow_center.openml.Classifier\"\x15\n\x06\x44\x61taID\x12\x0b\n\x03idx\x18\x01 \x01(\x05\"%\n\x0c\x46\x65\x61tureNames\x12\x15\n\rfeature_names\x18\x01 \x01(\t\"N\n\x07Request\x12\x32\n\x03idx\x18\x01 \x01(\x0b\x32%.know_center.openml.Classifier.DataID\x12\x0f\n\x07request\x18\x02 \x01(\t\"!\n\x10\x43lassifierResult\x12\r\n\x05label\x18\x01 \x01(\t2\xdd\x01\n\nClassifier\x12\x65\n\x0fGetFeatureNames\x12%.know_center.openml.Classifier.DataID\x1a+.know_center.openml.Classifier.FeatureNames\x12h\n\rGetPrediction\x12&.know_center.openml.Classifier.Request\x1a/.know_center.openml.Classifier.ClassifierResultB\x16\x42\x0f\x43lassifierProto\xa2\x02\x02KCb\x06proto3'
)




_DATAID = _descriptor.Descriptor(
  name='DataID',
  full_name='know_center.openml.Classifier.DataID',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='idx', full_name='know_center.openml.Classifier.DataID.idx', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=57,
  serialized_end=78,
)


_FEATURENAMES = _descriptor.Descriptor(
  name='FeatureNames',
  full_name='know_center.openml.Classifier.FeatureNames',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_names', full_name='know_center.openml.Classifier.FeatureNames.feature_names', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=80,
  serialized_end=117,
)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='know_center.openml.Classifier.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='idx', full_name='know_center.openml.Classifier.Request.idx', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request', full_name='know_center.openml.Classifier.Request.request', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=119,
  serialized_end=197,
)


_CLASSIFIERRESULT = _descriptor.Descriptor(
  name='ClassifierResult',
  full_name='know_center.openml.Classifier.ClassifierResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='label', full_name='know_center.openml.Classifier.ClassifierResult.label', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=199,
  serialized_end=232,
)

_REQUEST.fields_by_name['idx'].message_type = _DATAID
DESCRIPTOR.message_types_by_name['DataID'] = _DATAID
DESCRIPTOR.message_types_by_name['FeatureNames'] = _FEATURENAMES
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['ClassifierResult'] = _CLASSIFIERRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DataID = _reflection.GeneratedProtocolMessageType('DataID', (_message.Message,), {
  'DESCRIPTOR' : _DATAID,
  '__module__' : 'classifier_model_pb2'
  # @@protoc_insertion_point(class_scope:know_center.openml.Classifier.DataID)
  })
_sym_db.RegisterMessage(DataID)

FeatureNames = _reflection.GeneratedProtocolMessageType('FeatureNames', (_message.Message,), {
  'DESCRIPTOR' : _FEATURENAMES,
  '__module__' : 'classifier_model_pb2'
  # @@protoc_insertion_point(class_scope:know_center.openml.Classifier.FeatureNames)
  })
_sym_db.RegisterMessage(FeatureNames)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'classifier_model_pb2'
  # @@protoc_insertion_point(class_scope:know_center.openml.Classifier.Request)
  })
_sym_db.RegisterMessage(Request)

ClassifierResult = _reflection.GeneratedProtocolMessageType('ClassifierResult', (_message.Message,), {
  'DESCRIPTOR' : _CLASSIFIERRESULT,
  '__module__' : 'classifier_model_pb2'
  # @@protoc_insertion_point(class_scope:know_center.openml.Classifier.ClassifierResult)
  })
_sym_db.RegisterMessage(ClassifierResult)


DESCRIPTOR._options = None

_CLASSIFIER = _descriptor.ServiceDescriptor(
  name='Classifier',
  full_name='know_center.openml.Classifier.Classifier',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=235,
  serialized_end=456,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetFeatureNames',
    full_name='know_center.openml.Classifier.Classifier.GetFeatureNames',
    index=0,
    containing_service=None,
    input_type=_DATAID,
    output_type=_FEATURENAMES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetPrediction',
    full_name='know_center.openml.Classifier.Classifier.GetPrediction',
    index=1,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_CLASSIFIERRESULT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CLASSIFIER)

DESCRIPTOR.services_by_name['Classifier'] = _CLASSIFIER

# @@protoc_insertion_point(module_scope)
