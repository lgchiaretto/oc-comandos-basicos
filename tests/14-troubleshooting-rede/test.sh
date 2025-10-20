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

run_test "Pods do CoreDNS/DNS" \
    "oc get pods -n openshift-dns | head -5 || true"

run_test "Verificar Services: Listar svc" \
    "oc get svc -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Endpoints: Listar endpoints" \
    "oc get endpoints -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Troubleshoot Routes: Listar routes" \
    "oc get routes -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Troubleshoot Routes: Listar route" \
    "oc get route test-app -o jsonpath='{.spec.host}' -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "IngressController config" \
    "oc get ingresscontroller -n openshift-ingress-operator 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Descrever IngressController" \
    "oc describe ingresscontroller default -n openshift-ingress-operator 2>/dev/null || echo 'Recurso não encontrado'"
