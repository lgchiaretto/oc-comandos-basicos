#!/bin/bash

##############################################################################
# Teste: 26 - TEMPLATES E MANIFESTS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "26 - TEMPLATES E MANIFESTS"
run_test "Listar templates" \
    "oc get templates -n openshift | head -10 || true"

run_test "Exportar deployment como YAML" \
    "oc get deployment test-app -n ${TEST_PROJECT} -o yaml | head -30 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Listar Templates: Listar templates" \
    "oc get templates -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"
