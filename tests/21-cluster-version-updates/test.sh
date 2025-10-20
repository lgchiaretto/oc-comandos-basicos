#!/bin/bash

##############################################################################
# Teste: 21 - CLUSTER VERSION E UPDATES
##############################################################################

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
    "oc get clusterversion -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"


run_test "Status do Cluster: Admin: upgrade" \
    "oc adm upgrade 2>/dev/null || echo 'Upgrade não disponível ou sem permissões'"


run_test "Monitorar Update: Listar co" \
    "oc get co -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"


run_test "Update Stuck ou Falhando: Descrever primeiro CO com problema" \
    "oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type==\"Degraded\" and .status==\"True\")) | .metadata.name' | head -1 | xargs -I {} oc describe co {} 2>/dev/null || echo 'Nenhum CO com problema'"


run_test "Update Stuck ou Falhando: Listar events do namespace openshift-cluster-version" \
    "oc get events -n openshift-cluster-version --sort-by='.lastTimestamp' | tail -10 2>/dev/null || echo 'Recurso não encontrado'"


run_test "Update Prerequisites: Listar mcp" \
    "oc get mcp -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"


run_test "Verificar progresso de update nos nodes" \
    "oc get mcp -o custom-columns=NAME:.metadata.name,UPDATED:.status.updatedMachineCount,TOTAL:.status.machineCount 2>/dev/null || echo 'Recurso não encontrado'"
