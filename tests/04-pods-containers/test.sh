#!/bin/bash

##############################################################################
# Teste: 04 - PODS E CONTAINERS
# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
section_header "04 - PODS E CONTAINERS"
run_test "Listar todos os pods" \
    "oc get pods"
run_test "Listar pods com mais informações" \
    "oc get pods -o wide"
run_test "Listar pods em todos os namespaces" \
    "oc get pods -A | head -20 || true"
run_test "Descrever primeiro pod" \
    "oc get pods -o name | head -1 | xargs -I {} oc describe {}"
run_test "Ver logs do pod" \
    "oc get pods -o name | head -1 | xargs -I {} oc logs {} --tail=10"
run_test "Listar pods com labels" \
    "oc get pods --show-labels"
run_test "Filtrar pods por label" \
    "oc get pods -l deployment=test-app"
run_test "Ver eventos do namespace" \
    "oc get events --sort-by='.lastTimestamp' | head -10 || true"
run_test "Listar Pods: Listar pods" \
    "oc get pods -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Descrever Pods: Descrever pod" \
    "oc describe pod test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Descrever Pods: Listar pod" \
    "oc get pod test-app -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Acessar Shell: rsh <nome-do-pod>" \
    "oc rsh test-app"
run_test "Acessar Shell: Executar comando em <nome-do-pod>" \
    "oc exec test-app -- test-app -n ${TEST_PROJECT}"
run_test "Acessar Shell: Executar comando em -it" \
    "oc exec -it test-app -- /bin/bash -n ${TEST_PROJECT}"
run_test "Copiar Arquivos: cp <arquivo-local>" \
    "oc cp test-app test-app:test-app"
run_test "Copiar Arquivos: cp <nome-do-pod>:<caminho-no-pod>" \
    "oc cp test-app:test-app test-app"
run_test "Copiar Arquivos: cp /local/dir" \
    "oc cp /local/dir test-app:/container/dir"
run_test "Copiar Arquivos: cp ./config.json" \
    "oc cp ./config.json mypod:/etc/config/config.json"
run_test "Criar e Deletar: Criar -f" \
    "oc create -f pod.yaml"
run_test "Criar e Deletar: Aplicar -f" \
    "oc apply -f pod.yaml"
run_test "Reiniciar Pods: Rollout restart" \
    "oc rollout restart deployment/test-app 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
run_test "Reiniciar Pods: Escalar deployment" \
    "oc scale deployment test-app --replicas=0 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
run_test "Debug Interativo: debug pod/<nome-do-pod>" \
    "oc debug pod/test-app"
    "oc get pods -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc describe pod test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get pod test-app -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc rollout restart deployment/test-app 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
    "oc scale deployment test-app --replicas=0 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
run_test "Ver Logs: Ver logs de <nome-do-pod>" \
    "oc logs test-app -n ${TEST_PROJECT}"
run_test "Ver Logs: Ver logs de -f" \
    "oc logs -f test-app -n ${TEST_PROJECT}"
run_test "Ver Logs: Ver logs de -l" \
    "oc logs -l app=test-app -n ${TEST_PROJECT}"
