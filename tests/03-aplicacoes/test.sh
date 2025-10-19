#!/bin/bash

##############################################################################
# Teste: 03 - APLICAÇÕES
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "03 - APLICAÇÕES"

run_test "Criar aplicação de teste (nginx)" \
    "oc new-app nginx:latest --name=test-app -n ${TEST_PROJECT}"

run_test "Aguardar deployment" \
    "sleep 10"

run_test "Listar todas as aplicações" \
    "oc get all -n ${TEST_PROJECT}"

run_test "Listar deployments" \
    "oc get deployment -n ${TEST_PROJECT}"

run_test "Listar services" \
    "oc get svc -n ${TEST_PROJECT}"

run_test "Expor service como route" \
    "oc expose service test-app -n ${TEST_PROJECT}"

run_test "Listar routes" \
    "oc get routes -n ${TEST_PROJECT}"

run_test "Listar templates disponíveis" \
    "oc get templates -n openshift | head -10 || true"

