#!/bin/bash

##############################################################################
# Teste: 29 - JOBS E CRONJOBS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "29 - JOBS E CRONJOBS"

run_test "Listar Jobs" \
    "oc get jobs -n ${TEST_PROJECT}"

run_test "Listar CronJobs" \
    "oc get cronjobs -n ${TEST_PROJECT}"

run_test "Criar Job de teste" \
    "oc create job test-job --image=busybox -n ${TEST_PROJECT} -- echo 'Hello from test job'"

run_test "Verificar Job criado" \
    "sleep 3 && oc get jobs -n ${TEST_PROJECT}"

run_test "Ver logs do Job" \
    "sleep 5 && oc logs job/test-job -n ${TEST_PROJECT}"

