#!/bin/bash

##############################################################################
# Teste: 22 - ETCD BACKUP
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "22 - ETCD BACKUP"

run_test "Verificar pods do etcd" \
    "oc get pods -n openshift-etcd | grep -E etcd"

run_test "Ver membros do etcd" \
    "oc exec -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[1].metadata.name}') -- etcdctl member list -w table"

run_test "Listar pods com uso de recursos customizado" \
    "oc get pods -n ${TEST_PROJECT} -o json | jq -r '.items[] | .metadata.name' | head -5 || true"

run_test "Extrair imagens dos pods" \
    "oc get pods -n ${TEST_PROJECT} -o json | jq -r '.items[].spec.containers[].image' | head -5 || true"

