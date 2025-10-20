#!/bin/bash

##############################################################################
# Teste: 10 - REGISTRY E IMAGENS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "10 - REGISTRY E IMAGENS"

run_test "Ver URL do registry interno" \
    "oc get route -n openshift-image-registry 2>/dev/null || echo 'Registry route não exposta'"

run_test "Listar ImageStreams do sistema" \
    "oc get is -n openshift | head -10 || true"

run_test "Ver tags de uma ImageStream" \
    "oc get is -n openshift -o name | head -1 | xargs oc get -n openshift -o jsonpath='{.spec.tags[*].name}' 2>/dev/null || echo 'N/A'"

run_test "Ver URL do registry interno" \
    "oc get route -n openshift-image-registry 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Acessar Registry: Listar clusteroperator" \
    "oc get clusteroperator image-registry -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Pull de Imagens: Listar is" \
    "oc get is -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Configurar Mirroring: Listar imagecontentsourcepolicy" \
    "oc get imagecontentsourcepolicy -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Ver configuração de pruner automático" \
    "oc get imagepruner/cluster -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Ver jobs de pruning" \
    "oc get jobs -n openshift-image-registry 2>/dev/null || echo 'Recurso não encontrado'"
