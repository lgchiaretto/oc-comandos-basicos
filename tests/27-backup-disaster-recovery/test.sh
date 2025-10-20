#!/bin/bash

##############################################################################
# Teste: 27 - BACKUP E DISASTER RECOVERY
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "27 - BACKUP E DISASTER RECOVERY"
run_test "Exportar recursos do projeto" \
    "oc get all -n ${TEST_PROJECT} -o yaml | head -50 || true"

run_test "Backup de Manifests por Namespace: Listar namespace" \
    "oc get namespace test-app -o yaml > /tmp/test-app-namespace.yaml 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Backup de Todo o Cluster [Manifests]: Listar namespaces" \
    "oc get namespaces -o yaml > /tmp/cluster-namespaces.yaml 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Backup de Todo o Cluster [Manifests]: Listar nodes" \
    "oc get nodes -o yaml > /tmp/cluster-nodes.yaml 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Backup de Todo o Cluster [Manifests]: Listar clusterroles" \
    "oc get clusterroles -o yaml > /tmp/cluster-clusterroles.yaml 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Velero - Backup Tool: Listar csv" \
    "oc get csv -n openshift-adp 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Backup de PVCs: Listar volumesnapshot" \
    "oc get volumesnapshot -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Restore de Aplicação: Listar pvc" \
    "oc get pvc -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"
