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
run_test "Listar pods com uso de recursos customizado" \
    "oc get pods -n ${TEST_PROJECT} -o json | jq -r '.items[] | .metadata.name' | head -5 || true"
run_test "Extrair imagens dos pods" \
    "oc get pods -n ${TEST_PROJECT} -o json | jq -r '.items[].spec.containers[].image' | head -5 || true"
run_test "Verificar Etcd: Listar pods" \
    "oc get pods -n openshift-etcd 2>/dev/null || echo 'Recurso não encontrado'"
run_test "Verificar Etcd: Listar clusteroperator" \
    "oc get clusteroperator etcd -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"
run_test "Backup Programado [CronJob]: Listar cronjob" \
    "oc get cronjob -n etcd-backup 2>/dev/null || echo 'Recurso não encontrado'"
run_test "Backup de Recursos do Cluster: Listar namespaces" \
    "oc get namespaces -o yaml > /tmp/cluster-resources-backup-namespaces.yaml 2>/dev/null || echo 'Recurso não encontrado'"
run_test "Backup de Recursos do Cluster: Listar clusterroles" \
    "oc get clusterroles -o yaml > /tmp/cluster-resources-backup-clusterroles.yaml 2>/dev/null || echo 'Recurso não encontrado'"
run_test "Restore do Etcd: Listar nodes" \
    "oc get nodes -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"
run_test "Ver membros do etcd" \
    "oc exec -n openshift-etcd etcd-control-plane-cluster-st22j-2 -- etcdctl member list -w table 2>/dev/null || echo 'Recurso não disponível'"
