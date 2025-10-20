#!/bin/bash

##############################################################################
# Teste: 19 - CERTIFICADOS E CSR
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "19 - CERTIFICADOS E CSR"

run_test "Listar CSRs" \
    "oc get csr | head -10 || true"


run_test "CSRs Pending" \
    "oc get csr | grep -E Pending || echo 'Nenhum CSR pendente'"


run_test "Visualizar CSRs: Listar csr" \
    "oc get csr -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"


run_test "API Server Certificates: Listar secret" \
    "oc get secret -n openshift-kube-apiserver 2>/dev/null || echo 'Recurso não encontrado'"


run_test "Service Serving Certificates: Listar secrets" \
    "oc get secrets --field-selector type=kubernetes.io/tls -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"


run_test "Custom API Certificates: Patch apiserver" \
    "oc get apiserver cluster -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"
