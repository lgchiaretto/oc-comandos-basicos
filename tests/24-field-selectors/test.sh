#!/bin/bash

##############################################################################
# Teste: 24 - FIELD SELECTORS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "24 - FIELD SELECTORS"

run_test "Pods Running" \
    "oc get pods -n ${TEST_PROJECT} --field-selector=status.phase=Running 2>/dev/null || echo 'Pods ainda não estão Running'"

run_test "Pods não Succeeded" \
    "oc get pods -A --field-selector=status.phase!=Succeeded | head -10 || true"

