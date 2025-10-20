#!/bin/bash

##############################################################################
# Teste: 08 - STORAGE
# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_SC=$(oc get sc -o name )
source "${SCRIPT_DIR}/../lib/common.sh"
section_header "08 - STORAGE"

run_test "Listar PVCs com status" \
    "oc get pvc -A | head -10 || true"
run_test "PVCs Pending" \
    "oc get pvc -o jsonpath='{.items[?(@.status.phase=="Pending")].metadata.name}'"
run_test "Listar StorageClasses" \
    "oc get storageclass"
run_test "Listar pv" \
    "oc get pv 2>/dev/null || echo "Recurso não encontrado"
run_test "Listar persistentvolumes" \
    "oc get persistentvolumes -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Listar persistentvolumeclaims" \
    "oc get pvc -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Descrever pv" \
    "oc describe pv test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Descrever pvc" \
    "oc describe pvc test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Descrever sc" \
    "oc describe sc ocs-external-storagecluster-ceph-rbd -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Tipos de Volumes: Descrever pod" \
    "oc describe pod -l app=test-app | grep -A 5 Volumes -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Configurar volume" \
    "oc set volume deployment/test-app --add -t pvc --name=test-app --claim-name=test-app --mount-path=/test-app \
    2>/dev/null || echo "Recurso não encontrado"
run_test "Patch storageclass" \
    "oc patch storageclass ocs-external-storagecluster-ceph-rbd -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}' 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
run_test "Criar PVC usando default storageclass" \
    "oc apply -f - <<EOF
