#!/bin/bash

##############################################################################
# Teste: 13 - TROUBLESHOOTING PODS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "13 - TROUBLESHOOTING PODS"

run_test "Ver pods com problemas (todos os namespaces)" \
    "oc get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded | head -10 || true"

run_test "Ver pods em CrashLoopBackOff" \
    "oc get pods -A --field-selector=status.phase=Running | grep -E -i crash || echo 'Nenhum pod em CrashLoopBackOff'"

run_test "Descrever primeiro pod do projeto" \
    "oc get pods -n ${TEST_PROJECT} -o name | head -1 | xargs oc describe -n ${TEST_PROJECT}"

