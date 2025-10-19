#!/bin/bash

##############################################################################
# Teste: 09 - BUILDS E IMAGES
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "09 - BUILDS E IMAGES"

run_test "Listar BuildConfigs" \
    "oc get bc -n ${TEST_PROJECT}"

run_test "Listar Builds" \
    "oc get builds -n ${TEST_PROJECT}"

run_test "Listar ImageStreams" \
    "oc get is -n ${TEST_PROJECT}"

run_test "Listar ImageStreams do OpenShift" \
    "oc get is -n openshift | head -10 || true"

