#!/bin/bash

##############################################################################
# Teste: 16 - SEGURANÇA E RBAC
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "16 - SEGURANÇA E RBAC"

run_test "Listar roles" \
    "oc get roles -n ${TEST_PROJECT}"

run_test "Listar rolebindings" \
    "oc get rolebindings -n ${TEST_PROJECT}"

run_test "Listar clusterroles" \
    "oc get clusterroles | head -10 || true"

run_test "Listar clusterrolebindings" \
    "oc get clusterrolebindings | head -10 || true"

run_test "Verificar permissões (can-i)" \
    "oc auth can-i create pods -n ${TEST_PROJECT}"

run_test "Listar o que posso fazer" \
    "oc auth can-i --list -n ${TEST_PROJECT} | head -20 || true"

run_test "Listar SCCs" \
    "oc get scc"

run_test "Listar service accounts" \
    "oc get sa -n ${TEST_PROJECT}"

