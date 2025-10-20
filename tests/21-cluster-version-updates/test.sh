#!/bin/bash

##############################################################################
# Teste: 21 - CLUSTER VERSION E UPDATES
# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
section_header "21 - CLUSTER VERSION E UPDATES"
run_test "Ver versão do cluster" \
    "oc get clusterversion"
run_test "Descrever ClusterVersion" \
    "oc describe clusterversion version"
run_test "Ver histórico de updates" \
    "oc get clusterversion version -o jsonpath='{.status.history}' | head -200 || true"
run_test "Ver Versão Atual: Listar clusterversion" \
    "oc get clusterversion -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Ver Versão Atual: Descrever clusterversion" \
    "oc describe clusterversion version -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Status do Cluster: Admin: upgrade" \
    "oc adm upgrade"
run_test "Monitorar Update: Listar co" \
    "oc get co -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Monitorar Update: Ver logs de -n" \
    "oc logs -n test-app test-app"
run_test "Ver e Mudar Channel: Patch clusterversion" \
    "oc patch clusterversion version --type merge -p '{"spec":{"channel":"stable-4.14"}}' 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
run_test "Update Stuck ou Falhando: Descrever co" \
    "oc describe co test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Update Stuck ou Falhando: Listar pods" \
    "oc get pods -n test-app 2>/dev/null || echo "Recurso não encontrado"
run_test "Update Stuck ou Falhando: Listar events" \
    "oc get events -n test-app --sort-by='.lastTimestamp' 2>/dev/null || echo "Recurso não encontrado"
run_test "Update Prerequisites: Listar nodes" \
    "oc get nodes -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Update Prerequisites: Listar mcp" \
    "oc get mcp -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get clusterversion -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc describe clusterversion version -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get co -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc patch clusterversion version --type merge -p '{"spec":{"channel":"stable-4.14"}}' 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
    "oc describe co test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get pods -n test-app 2>/dev/null || echo "Recurso não encontrado"
    "oc get events -n test-app --sort-by='.lastTimestamp' 2>/dev/null || echo "Recurso não encontrado"
    "oc get nodes -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get mcp -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
