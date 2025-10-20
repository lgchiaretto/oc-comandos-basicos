#!/bin/bash

##############################################################################
# Teste: 04 - PODS E CONTAINERS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "04 - PODS E CONTAINERS"

run_test "Listar todos os pods" \
    "oc get pods -n ${TEST_PROJECT}"

run_test "Listar pods com mais informações" \
    "oc get pods -o wide -n ${TEST_PROJECT}"

run_test "Listar pods em todos os namespaces" \
    "oc get pods -A | head -20 || true"

run_test "Descrever primeiro pod" \
    "oc get pods -n ${TEST_PROJECT} -o name | head -1 | xargs -I {} oc describe {} -n ${TEST_PROJECT} 2>/dev/null || echo 'Sem pods'"

run_test "Ver logs do pod" \
    "oc get pods -n ${TEST_PROJECT} -o name | head -1 | xargs -I {} oc logs {} -n ${TEST_PROJECT} --tail=10 2>/dev/null || echo 'Sem pods'"

run_test "Listar pods com labels" \
    "oc get pods --show-labels -n ${TEST_PROJECT}"

run_test "Filtrar pods por label" \
    "oc get pods -l app=test-app -n ${TEST_PROJECT}"

run_test "Ver eventos do namespace" \
    "oc get events -n ${TEST_PROJECT} --sort-by='.lastTimestamp' | head -10 || true"

run_test "Listar Pods: Listar pods" \
    "oc get pods -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Descrever Pods: Descrever pod (primeiro disponível)" \
    "oc get pods -n ${TEST_PROJECT} -l app=test-app -o name | head -1 | xargs -I {} oc describe {} -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Descrever Pods: Listar pod em YAML (primeiro disponível)" \
    "oc get pods -n ${TEST_PROJECT} -l app=test-app -o name | head -1 | xargs -I {} oc get {} -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Reiniciar Pods: Rollout restart" \
    "oc rollout restart deployment/test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado ou não aplicável'"

run_test "Ver Logs: Ver logs de pod (por label)" \
    "oc logs -l app=test-app -n ${TEST_PROJECT} --tail=10 2>/dev/null || echo 'Sem pods'"

run_test "Ver Logs: Ver logs do primeiro pod" \
    "oc get pods -n ${TEST_PROJECT} -l app=test-app -o name | head -1 | xargs -I {} oc logs {} -n ${TEST_PROJECT} --tail=10 2>/dev/null || echo 'Sem pods'"
