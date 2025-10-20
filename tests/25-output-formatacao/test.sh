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
run_test "Básico: Listar nome do primeiro pod" \
    "oc get pods -n ${TEST_PROJECT} -l app=test-app -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo 'Recurso não encontrado'"
run_test "Filtros e Condições: Listar nodes Ready" \
    "oc get nodes -o jsonpath='{.items[?(@.status.conditions[?(@.type==\"Ready\")].status==\"True\")].metadata.name}' 2>/dev/null || echo 'Recurso não encontrado'"
run_test "Exemplos Práticos com JQ: Listar CO degradados" \
    "oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type==\"Degraded\" and .status==\"True\")) | .metadata.name' 2>/dev/null || echo 'Nenhum CO degradado'"
run_test "JSONPath: Extrair IPs dos pods" \
    "oc get pods -n ${TEST_PROJECT} -o jsonpath='{.items[*].status.podIP}' 2>/dev/null || echo 'Sem pods'"
run_test "Custom Columns: Pods com status e node" \
    "oc get pods -n ${TEST_PROJECT} -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName 2>/dev/null || echo 'Sem pods'"
