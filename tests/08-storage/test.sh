#!/bin/bash

##############################################################################
# Teste: 08 - STORAGE
# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
section_header "08 - STORAGE"
run_test "Listar PVCs com status" \
    "oc get pvc -A | head -10 || true"
run_test "PVCs Pending" \
    "oc get pvc -A --field-selector=status.phase=Pending | head -10 || true"
run_test "Listar StorageClasses" \
    "oc get storageclass"
run_test "Listar pv" \
    "oc get pv -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Listar persistentvolumes" \
    "oc get persistentvolumes -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Descrever pv" \
    "oc describe pv test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Criar e Gerenciar: Listar pvc" \
    "oc get pvc -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Criar e Gerenciar: Listar persistentvolumeclaims" \
    "oc get persistentvolumeclaims -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Criar e Gerenciar: Descrever pvc" \
    "oc describe pvc test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Criar e Gerenciar: Criar -f" \
    "oc create -f test-app"
run_test "Usando em Deployments: Configurar volume" \
    "oc set volume deployment/test-app \ 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
run_test "Usando em Deployments: Listar storageclass" \
    "oc get storageclass -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Usando em Deployments: Listar sc" \
    "oc get sc -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Usando em Deployments: Descrever sc" \
    "oc describe sc test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
run_test "Usando em Deployments: Patch storageclass" \
    "oc patch storageclass test-app -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}' 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
run_test "Tipos de Volumes: Descrever pod" \
    "oc describe pod test-app | grep -A 5 Volumes -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get pv -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get persistentvolumes -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc describe pv test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get pvc -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get persistentvolumeclaims -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc describe pvc test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc set volume deployment/test-app \ 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
    "oc get storageclass -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc get sc -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc describe sc test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
    "oc patch storageclass test-app -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}' 2>/dev/null || echo "Recurso não encontrado ou não aplicável"
    "oc describe pod test-app | grep -A 5 Volumes -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
