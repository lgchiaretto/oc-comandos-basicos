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
    "oc get pods -n ${TEST_PROJECT} -o wide"

run_test "Listar pods em todos os namespaces" \
    "oc get pods -A | head -20 || true"

run_test "Descrever primeiro pod" \
    "oc get pods -n ${TEST_PROJECT} -o name | head -1 | xargs -I {} oc describe {} -n ${TEST_PROJECT}"

run_test "Ver logs do pod" \
    "oc get pods -n ${TEST_PROJECT} -o name | head -1 | xargs -I {} oc logs {} -n ${TEST_PROJECT} --tail=10"

run_test "Listar pods com labels" \
    "oc get pods -n ${TEST_PROJECT} --show-labels"

run_test "Filtrar pods por label" \
    "oc get pods -n ${TEST_PROJECT} -l deployment=test-app"

run_test "Ver eventos do namespace" \
    "oc get events -n ${TEST_PROJECT} --sort-by='.lastTimestamp' | head -10 || true"

