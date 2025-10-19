#!/bin/bash

##############################################################################
# Teste: 18 - NODES E MACHINE
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "18 - NODES E MACHINE"

run_test "Listar nodes" \
    "oc get nodes"

run_test "Listar nodes com detalhes" \
    "oc get nodes -o wide"

run_test "Descrever primeiro node" \
    "oc get nodes -o name | head -1 | xargs oc describe"

run_test "Listar machines" \
    "oc get machines -n openshift-machine-api"

run_test "Listar machinesets" \
    "oc get machinesets -n openshift-machine-api"

