#!/bin/sh

# run this script from the root directory of the repo, i.e.
#   scripts/generate_grpc_stubs.sh

# helps the imports work correctly
cd lib/heartsapp_service_protos/src

python -m grpc_tools.protoc -I. --python_out=../../../ --grpc_python_out=../../../ get_answer/*.proto
