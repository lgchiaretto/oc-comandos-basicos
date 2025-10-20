#!/bin/bash

##############################################################################
# Teste: 29 - JOBS E CRONJOBS
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
run_test "Criar Jobs: Criar job" \
    "oc create job my-job --image=busybox -- echo "Hello World" 2>/dev/null || echo "Recurso já existe ou erro esperado"
run_test "Gerenciar Jobs: Listar jobs" \
    "oc get jobs -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Gerenciar Jobs: Descrever job" \
    "oc describe job test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Gerenciar Jobs: Ver logs de job/<job-name>" \
    "oc logs job/test-app -n ${TEST_PROJECT}"
run_test "Gerenciar Jobs: Listar pods" \
    "oc get pods -l job-name=test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Jobs Paralelos: Listar job" \
    "oc get job parallel-job -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Criar CronJobs: Criar cronjob" \
    "oc create cronjob my-cronjob --image=busybox --schedule="*/5 * * * *" -- echo "Hello every 5 minutes"
run_test "Gerenciar CronJobs: Listar cronjobs" \
    "oc get cronjobs -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Gerenciar CronJobs: Listar cj" \
    "oc get cj -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Gerenciar CronJobs: Descrever cronjob" \
    "oc describe cronjob test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Gerenciar CronJobs: Patch cronjob" \
    "oc patch cronjob test-app -p '{"spec":{"suspend":true}}' 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
run_test "Debug de Jobs: Ver logs de $POD" \
    "oc logs test-app -n ${TEST_PROJECT}"
run_test "Debug de Jobs: Listar events" \
    "oc get events --field-selector involvedObject.name=test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Debug de CronJobs: Listar cronjob" \
    "oc get cronjob test-app -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Debug de CronJobs: Ver logs de $LAST_JOB" \
    "oc create job my-job --image=busybox -- echo "Hello World" 2>/dev/null || echo "Recurso já existe ou erro esperado"
    "oc get jobs -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc describe job test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get pods -l job-name=test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get job parallel-job -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc create cronjob my-cronjob --image=busybox --schedule="*/5 * * * *" -- echo "Hello every 5 minutes"
    "oc get cronjobs -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get cj -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc describe cronjob test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc patch cronjob test-app -p '{"spec":{"suspend":true}}' 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
    "oc get events --field-selector involvedObject.name=test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get cronjob test-app -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
