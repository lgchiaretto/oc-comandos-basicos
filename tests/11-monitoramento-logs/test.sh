#!/bin/bash

##############################################################################
# Teste: 11 - MONITORAMENTO E LOGS
##############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "11 - MONITORAMENTO E LOGS"

run_test "Ver logs de um pod" \
    "oc logs -n ${TEST_PROJECT} -l app=test-app --tail=20 2>/dev/null || echo 'Nenhum pod disponível'"

run_test "Ver logs em tempo real" \
    "timeout 2 oc logs -f -n ${TEST_PROJECT} -l app=test-app 2>/dev/null || echo 'Timeout ou sem pods'"

run_test "Ver logs de container específico" \
    "oc logs -n ${TEST_PROJECT} -l app=test-app -c test-app --tail=10 2>/dev/null || echo 'Container não encontrado'"

run_test "Ver logs anteriores (de container que crashou)" \
    "oc logs --previous -n ${TEST_PROJECT} -l app=test-app 2>/dev/null || echo 'Sem histórico anterior'"

run_test "Ver logs com timestamp" \
    "oc logs --timestamps -n ${TEST_PROJECT} -l app=test-app --tail=10 2>/dev/null || echo 'Sem pods'"

run_test "Ver eventos do namespace" \
    "oc get events -n ${TEST_PROJECT} --sort-by='.lastTimestamp' | tail -10"

run_test "Ver eventos de um pod específico" \
    "oc get events -n ${TEST_PROJECT} --field-selector involvedObject.kind=Pod | head -10"

run_test "Monitorar uso de recursos dos pods" \
    "oc adm top pods -n ${TEST_PROJECT} 2>/dev/null || echo 'Metrics não disponíveis'"

run_test "Monitorar uso de recursos dos nodes" \
    "oc adm top nodes | head -5 2>/dev/null || echo 'Metrics não disponíveis'"

run_test "Ver status geral do projeto" \
    "oc status -n ${TEST_PROJECT}"

run_test "Verificar pods com problemas" \
    "oc get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded | head -10"

run_test "Listar todos os eventos do cluster (últimos)" \
    "oc get events -A --sort-by='.lastTimestamp' | tail -20"

run_test "Ver logs do sistema (audit)" \
    "oc adm node-logs --role=master --path=audit/audit.log 2>/dev/null | tail -10 || echo 'Sem permissão ou audit não disponível'"

run_test "Ver logs de kubelet" \
    "oc adm node-logs --role=master --path=kubelet/kubelet.log 2>/dev/null | tail -10 || echo 'Sem permissão'"

run_test "Verificar prometheus" \
    "oc get pods -n openshift-monitoring | grep prometheus"

