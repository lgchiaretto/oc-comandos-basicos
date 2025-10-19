#!/bin/bash

##############################################################################
# Teste: 28 - PATCH E EDIT
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "28 - PATCH E EDIT"

run_test "Verificar annotation" \
    "oc get deployment test-app -n ${TEST_PROJECT} -o jsonpath='{.metadata.annotations.test}'"

