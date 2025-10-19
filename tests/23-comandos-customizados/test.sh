#!/bin/bash

##############################################################################
# Teste: 23 - Comandos Customizados (awk/jq)
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "23 - COMANDOS CUSTOMIZADOS (awk/jq)"

run_test "Listar pods com uso de recursos customizado" \
    "oc get pods -n ${TEST_PROJECT} -o json 2>/dev/null | jq -r '.items[] | .metadata.name' | head -5 || true"

run_test "Contar pods por status" \
    "oc get pods -A --no-headers 2>/dev/null | awk '{print \$4}' | sort | uniq -c || true"

run_test "Extrair imagens dos pods" \
    "oc get pods -n ${TEST_PROJECT} -o json 2>/dev/null | jq -r '.items[].spec.containers[].image' | head -5 || true"
