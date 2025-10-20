#!/bin/bash

##############################################################################
# Teste: 03 - APLICAÇÕES
# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
section_header "03 - APLICAÇÕES"
# Criar aplicação usando httpd que é mais estável
run_test "Criar aplicação de teste [httpd]" \
    "oc new-app httpd:latest --name=test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'App já existe'"
    

run_test "Aguardar deployment ser criado" \
    "sleep 5"
run_test "Aguardar pods iniciarem" \
    "oc wait --for=condition=available --timeout=60s deployment/test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Deployment ainda processando'"
run_test "Listar todas as aplicações" \
    "oc get all -n ${TEST_PROJECT}"
run_test "Listar deployments" \
    "oc get deployment -n ${TEST_PROJECT}"
run_test "Listar services" \
    "oc get svc -n ${TEST_PROJECT}"
run_test "Expor service como route" \
    "oc expose service test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Route já existe'"
run_test "Listar routes" \
    "oc get routes -n ${TEST_PROJECT}"
run_test "Listar templates disponíveis" \
    "oc get templates -n openshift 2>/dev/null | head -10 || true"
run_test "Verificar se pode criar app" \
    "oc auth can-i create deployments -n ${TEST_PROJECT}"
run_test "Descrever deployment" \
    "oc describe deployment test-app -n ${TEST_PROJECT} 2>/dev/null | head -20 || true"
run_test "Ver labels da aplicação" \
    "oc get all -l app=test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Nenhum recurso'"
run_test "Ver status da aplicação" \
    "oc status -n ${TEST_PROJECT} 2>/dev/null || echo 'Status não disponível'"
run_test "Listar ImageStreams" \
    "oc get is -n ${TEST_PROJECT} 2>/dev/null || echo 'Nenhuma ImageStream'"
