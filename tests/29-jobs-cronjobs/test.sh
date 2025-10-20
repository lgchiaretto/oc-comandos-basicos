#!/bin/bash

##############################################################################
# Teste: 29 - JOBS E CRONJOBS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "29 - JOBS E CRONJOBS"

run_test "Listar jobs" \
    "oc get jobs -n ${TEST_PROJECT}"


run_test "Listar cronjobs" \
    "oc get cronjobs -n ${TEST_PROJECT}"


run_test "Listar Jobs: Listar jobs" \
    "oc get jobs -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"


run_test "Descrever Job: Descrever primeiro job" \
    "oc get jobs -n ${TEST_PROJECT} -o name | head -1 | xargs -I {} oc describe {} -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"


run_test "Ver Logs de Job: Listar pods de job" \
    "oc get pods -n ${TEST_PROJECT} -l job-name --show-labels 2>/dev/null | head -5 || echo 'Nenhum job encontrado'"


run_test "Listar CronJobs: Listar cronjobs" \
    "oc get cronjobs -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"


run_test "Descrever CronJob: Descrever primeiro cronjob" \
    "oc get cronjobs -n ${TEST_PROJECT} -o name | head -1 | xargs -I {} oc describe {} -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"


run_test "Ver Histórico de Execuções: Listar jobs criados por cronjob" \
    "oc get jobs -n ${TEST_PROJECT} --sort-by=.metadata.creationTimestamp 2>/dev/null || echo 'Recurso não encontrado'"
