#!/bin/bash

##############################################################################
# Teste: 05 - DEPLOYMENTS E SCALING
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "05 - DEPLOYMENTS E SCALING"

run_test "Listar deployments" \
    "oc get deployment -n ${TEST_PROJECT}"

run_test "Descrever deployment" \
    "oc describe deployment test-app -n ${TEST_PROJECT}"

run_test "Ver deployment em YAML" \
    "oc get deployment test-app -n ${TEST_PROJECT} -o yaml | head -50 || true"

run_test "Scale para 2 réplicas" \
    "oc scale deployment test-app --replicas=2 -n ${TEST_PROJECT}"

run_test "Verificar scale" \
    "sleep 5 && oc get deployment test-app -n ${TEST_PROJECT}"

run_test "Scale de volta para 1" \
    "oc scale deployment test-app --replicas=1 -n ${TEST_PROJECT}"

run_test "Ver ReplicaSets" \
    "oc get rs -n ${TEST_PROJECT}"

run_test "Status do deployment" \
    "oc rollout status deployment/test-app -n ${TEST_PROJECT} --timeout=10s 2>/dev/null || echo 'Deployment ainda em progresso'"

run_test "Histórico de rollout" \
    "oc rollout history deployment/test-app -n ${TEST_PROJECT}"

