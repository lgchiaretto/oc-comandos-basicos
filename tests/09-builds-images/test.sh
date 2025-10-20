#!/bin/bash

##############################################################################
# Teste: 09 - BUILDS E IMAGES
##############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "09 - BUILDS E IMAGES"

run_test "Listar buildconfigs" \
    "oc get bc -n ${TEST_PROJECT}"

run_test "Listar builds" \
    "oc get builds -n ${TEST_PROJECT}"

run_test "Ver status de builds" \
    "oc get builds -n ${TEST_PROJECT} --sort-by=.metadata.creationTimestamp 2>/dev/null || echo 'Nenhum build'"

run_test "Listar imagestreams" \
    "oc get is -n ${TEST_PROJECT}"

run_test "Ver tags de imagestream" \
    "oc get is -n ${TEST_PROJECT} -o jsonpath='{range .items[*]}{.metadata.name}{\"\\n\"}{end}' 2>/dev/null || echo 'Sem imagestreams'"

run_test "Ver histórico de builds" \
    "oc get builds -n ${TEST_PROJECT} --sort-by=.status.completionTimestamp 2>/dev/null || echo 'Nenhum build'"

run_test "Descrever buildconfig" \
    "oc describe bc -n ${TEST_PROJECT} 2>/dev/null || echo 'Nenhum buildconfig encontrado'"

run_test "Descrever imagestream" \
    "oc describe is -n ${TEST_PROJECT} 2>/dev/null || echo 'Nenhum imagestream encontrado'"

run_test "Criar buildconfig de teste (do zero)" \
    "oc new-build --name=test-build --binary -n ${TEST_PROJECT} 2>/dev/null || echo 'Buildconfig já existe'"

run_test "Deletar buildconfig de teste" \
    "oc delete bc test-build -n ${TEST_PROJECT} 2>/dev/null || echo 'Buildconfig não encontrado'"

run_test "Ver logs de build" \
    "oc logs -n ${TEST_PROJECT} -l buildconfig=test-app --tail=20 2>/dev/null || echo 'Nenhum build encontrado'"

run_test "Iniciar novo build" \
    "oc start-build test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Buildconfig não encontrado'"

run_test "Cancelar build (se houver)" \
    "oc cancel-build test-app-1 -n ${TEST_PROJECT} 2>/dev/null || echo 'Build não encontrado ou já finalizado'"
