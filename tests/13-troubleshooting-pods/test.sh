#!/bin/bash

##############################################################################
# Teste: 13 - TROUBLESHOOTING PODS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "13 - TROUBLESHOOTING PODS"

run_test "Ver pods com problemas [todos os namespaces]" \
    "oc get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded | head -10 || true"

run_test "Ver pods em CrashLoopBackOff" \
    "oc get pods -A --field-selector=status.phase=Running | grep -E -i crash || echo 'Nenhum pod em CrashLoopBackOff'"

run_test "Descrever primeiro pod do projeto" \
    "oc get pods -n ${TEST_PROJECT} -o name | head -1 | xargs oc describe -n ${TEST_PROJECT} 2>/dev/null || echo 'Sem pods'"

run_test "Verificar Status: Listar pods" \
    "oc get pods -A -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Verificar Status: Listar events" \
    "oc get events --field-selector involvedObject.name=test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "ImagePullBackOff: Listar is" \
    "oc get is -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "ImagePullBackOff: Listar secrets" \
    "oc get secrets -n ${TEST_PROJECT} | grep docker 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Pending [Não Agendado]: Listar nodes" \
    "oc get nodes 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Volumes e Mounts: Listar pvc" \
    "oc get pvc -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "ConfigMaps e Secrets: Listar cm" \
    "oc get cm -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Pending [Não Agendado]: Descrever nodes" \
    "oc describe nodes | grep Taints 2>/dev/null || echo 'Recurso não encontrado'"
