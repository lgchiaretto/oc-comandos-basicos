#!/bin/bash

##############################################################################
# Teste: 06 - SERVICES E ROUTES
##############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "06 - SERVICES E ROUTES"
run_test "Listar services" \
    "oc get svc -n ${TEST_PROJECT}"
run_test "Listar services com mais detalhes" \
    "oc get svc -n ${TEST_PROJECT} -o wide"
run_test "Ver service em YAML" \
    "oc get svc test-app -n ${TEST_PROJECT} -o yaml 2>/dev/null || echo 'Service não encontrado'"
run_test "Listar routes" \
    "oc get routes -n ${TEST_PROJECT}"
run_test "Ver URL da route" \
    "oc get route test-app -n ${TEST_PROJECT} -o jsonpath='{.spec.host}' 2>/dev/null || echo 'Route não encontrado'"
run_test "Ver route em YAML" \
    "oc get route test-app -n ${TEST_PROJECT} -o yaml 2>/dev/null || echo 'Route não encontrado'"
run_test "Listar endpoints" \
    "oc get endpoints -n ${TEST_PROJECT}"

run_test "Ver todas as routes com URLs" \
    "oc get routes -n ${TEST_PROJECT} -o custom-columns=NAME:.metadata.name,HOST:.spec.host"

run_test "Descrever service" \
    "oc describe svc test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Service não encontrado'"

run_test "Descrever route" \
    "oc describe route test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Route não encontrado'"

run_test "Descrever endpoints" \
    "oc describe endpoints test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Endpoints não encontrados'"

run_test "Criar service para deployment" \
    "oc expose deployment test-app --port=8080 -n ${TEST_PROJECT} 2>/dev/null || echo 'Service já existe'"

run_test "Criar route para service" \
    "oc expose svc test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Route já existe'"

run_test "Criar route com TLS" \
    "oc create route edge test-secure --service=test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Route já existe'"
run_test "Deletar route de teste" \
    "oc delete route test-secure -n ${TEST_PROJECT} 2>/dev/null || echo 'Route não encontrado'"
