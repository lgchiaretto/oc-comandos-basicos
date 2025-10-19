#!/bin/bash

##############################################################################
# Teste: 11 - MONITORAMENTO E LOGS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "11 - MONITORAMENTO E LOGS"

run_test "Ver logs do primeiro pod" \
    "oc get pods -n ${TEST_PROJECT} -o name | head -1 | xargs oc logs -n ${TEST_PROJECT} --tail=5"

run_test "Ver eventos" \
    "oc get events -n ${TEST_PROJECT} --sort-by='.lastTimestamp' | head -10 || true"

run_test "Ver top nodes" \
    "oc adm top nodes 2>/dev/null || echo 'Métricas podem não estar disponíveis'"

run_test "Ver top pods" \
    "oc adm top pods -n ${TEST_PROJECT} 2>/dev/null || echo 'Métricas podem não estar disponíveis'"

