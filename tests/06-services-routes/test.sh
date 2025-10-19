#!/bin/bash

##############################################################################
# Teste: 06 - SERVICES E ROUTES
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "06 - SERVICES E ROUTES"

run_test "Listar services" \
    "oc get svc -n ${TEST_PROJECT}"

run_test "Descrever service" \
    "oc describe svc test-app -n ${TEST_PROJECT}"

run_test "Ver service em YAML" \
    "oc get svc test-app -n ${TEST_PROJECT} -o yaml | head -30 || true"

run_test "Listar routes" \
    "oc get routes -n ${TEST_PROJECT}"

run_test "Descrever route" \
    "oc describe route test-app -n ${TEST_PROJECT}"

run_test "Ver URL da route" \
    "oc get route test-app -n ${TEST_PROJECT} -o jsonpath='{.spec.host}'"

run_test "Listar endpoints" \
    "oc get endpoints -n ${TEST_PROJECT}"

