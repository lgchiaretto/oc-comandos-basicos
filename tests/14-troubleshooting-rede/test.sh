#!/bin/bash

##############################################################################
# Teste: 14 - TROUBLESHOOTING REDE
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "14 - TROUBLESHOOTING REDE"

run_test "Listar services" \
    "oc get svc -n ${TEST_PROJECT}"

run_test "Listar endpoints" \
    "oc get endpoints -n ${TEST_PROJECT}"

run_test "Listar routes" \
    "oc get routes -n ${TEST_PROJECT}"

run_test "Verificar DNS (pods dns)" \
    "oc get pods -n openshift-dns | head -5 || true"

