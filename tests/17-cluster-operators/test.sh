#!/bin/bash

##############################################################################
# Teste: 17 - CLUSTER OPERATORS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "17 - CLUSTER OPERATORS"

run_test "Listar Cluster Operators" \
    "oc get co"

run_test "Descrever primeiro CO" \
    "oc get co -o name | head -1 | xargs oc describe"

