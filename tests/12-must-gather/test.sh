#!/bin/bash

##############################################################################
# Teste: 12 - MUST-GATHER
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "12 - MUST-GATHER"
run_test "Verificar comando must-gather (sem executar)" \
    "oc adm must-gather --help | head -5 || true"
run_test "Inspecionar Recursos: Admin: inspect" \
    "oc adm inspect ns/test-app --dest-dir=/tmp/inspect"
run_test "Coletar Dados do Cluster: Listar pods" \
    "oc get pods -n openshift-must-gather-* 2>/dev/null || echo "Recurso não encontrado"
run_test "Verificações Básicas: Listar clusteroperators" \
    "oc get clusteroperators -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Verificações Básicas: Listar nodes" \
    "oc get nodes -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Verificações Básicas: Listar clusterversion" \
    "oc get clusterversion -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Verificações Básicas: Listar events" \
    "oc get events -A --field-selector type=Warning --sort-by='.lastTimestamp' | tail -20 -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Coleta Rápida: Listar co" \
    "oc get co -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
