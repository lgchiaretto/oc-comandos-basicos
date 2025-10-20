#!/bin/bash

##############################################################################
# Teste: 25 - OUTPUT E FORMATAÇÃO
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "25 - OUTPUT E FORMATAÇÃO"

run_test "Output em JSON" \
    "oc get pods -n ${TEST_PROJECT} -o json | head -50 || true"

run_test "Output em YAML" \
    "oc get pods -n ${TEST_PROJECT} -o yaml | head -50 || true"

run_test "Output com JSONPath" \
    "oc get pods -n ${TEST_PROJECT} -o jsonpath='{.items[*].metadata.name}' 2>/dev/null || echo 'Sem pods'"

run_test "Custom columns" \
    "oc get pods -n ${TEST_PROJECT} -o custom-columns=NAME:.metadata.name,STATUS:.status.phase 2>/dev/null || echo 'Sem pods'"

run_test "Básico: Listar pod" \
    "oc get pod test-app -o jsonpath='{.metadata.name}' -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Filtros e Condições: Listar nodes" \
    "oc get nodes -o jsonpath='{.items[?(@.status.conditions[?(@.type==\"Ready\")].status==\"True\")].metadata.name}' 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Exemplos Práticos com JQ: Listar co" \
    "oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type==\"Degraded\" and .status==\"True\")) | .metadata.name' 2>/dev/null || echo 'Recurso não encontrado'"
