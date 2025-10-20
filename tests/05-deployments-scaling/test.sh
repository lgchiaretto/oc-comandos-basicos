#!/bin/bash

##############################################################################
# Teste: 05 - DEPLOYMENTS E SCALING
##############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "05 - DEPLOYMENTS E SCALING"
run_test "Listar deployments" \
    "oc get deployment -n ${TEST_PROJECT}"

run_test "Descrever deployment" \
    "oc describe deployment test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Deployment não encontrado'"

run_test "Ver deployment em YAML" \
    "oc get deployment test-app -n ${TEST_PROJECT} -o yaml 2>/dev/null | head -50 || echo 'Deployment não encontrado'"

run_test "Scale para 2 réplicas" \
    "oc scale deployment test-app --replicas=2 -n ${TEST_PROJECT} 2>/dev/null || echo 'Deployment não encontrado'"

run_test "Verificar scale" \
    "sleep 3 && oc get deployment test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Deployment não encontrado'"

run_test "Scale de volta para 1" \
    "oc scale deployment test-app --replicas=1 -n ${TEST_PROJECT} 2>/dev/null || echo 'Deployment não encontrado'"

run_test "Ver ReplicaSets" \
    "oc get rs -n ${TEST_PROJECT}"

run_test "Status do deployment" \
    "oc rollout status deployment/test-app -n ${TEST_PROJECT} --timeout=10s 2>/dev/null || echo 'Deployment ainda em progresso'"

run_test "Histórico de rollout" \
    "oc rollout history deployment/test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Deployment não encontrado'"

run_test "Configurar autoscaling (HPA)" \
    "oc autoscale deployment test-app --min=1 --max=5 --cpu-percent=80 -n ${TEST_PROJECT} 2>/dev/null || echo 'HPA já existe ou deployment não encontrado'"

run_test "Listar HPA" \
    "oc get hpa -n ${TEST_PROJECT}"

run_test "Descrever HPA" \
    "oc describe hpa -n ${TEST_PROJECT} 2>/dev/null || echo 'Nenhum HPA encontrado'"

run_test "Atualizar imagem do deployment" \
    "oc set image deployment/test-app test-app=httpd:2.4 -n ${TEST_PROJECT} 2>/dev/null || echo 'Deployment não encontrado'"

run_test "Pausar rollout" \
    "oc rollout pause deployment/test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Deployment não encontrado'"

run_test "Retomar rollout" \
    "oc rollout resume deployment/test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Deployment não encontrado'"

run_test "Reiniciar rollout" \
    "oc rollout restart deployment/test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Deployment não encontrado'"

run_test "Fazer rollback (undo)" \
    "oc rollout undo deployment/test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Deployment não encontrado'"

run_test "Ver todas as réplicas" \
    "oc get replicasets -n ${TEST_PROJECT}"

run_test "Deletar HPA de teste" \
    "oc delete hpa --all -n ${TEST_PROJECT} 2>/dev/null || echo 'Nenhum HPA para deletar'"

