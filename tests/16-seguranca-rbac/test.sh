#!/bin/bash

##############################################################################
# Teste: 16 - SEGURANÇA E RBAC
##############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "16 - SEGURANÇA E RBAC"
run_test "Listar roles" \
    "oc get roles -n ${TEST_PROJECT}"

run_test "Listar rolebindings" \
    "oc get rolebindings -n ${TEST_PROJECT}"

run_test "Listar clusterroles" \
    "oc get clusterroles | head -20"

run_test "Listar clusterrolebindings" \
    "oc get clusterrolebindings | head -20"

run_test "Ver permissões do usuário atual" \
    "oc auth can-i --list -n ${TEST_PROJECT} | head -20"

run_test "Verificar se pode criar pods" \
    "oc auth can-i create pods -n ${TEST_PROJECT}"

run_test "Verificar se pode deletar deployments" \
    "oc auth can-i delete deployments -n ${TEST_PROJECT}"

run_test "Criar role de teste" \
    "oc create role test-role --verb=get,list --resource=pods -n ${TEST_PROJECT} 2>/dev/null || echo 'Role já existe'"

run_test "Descrever role" \
    "oc describe role test-role -n ${TEST_PROJECT} 2>/dev/null || echo 'Role não encontrado'"

run_test "Listar service accounts" \
    "oc get sa -n ${TEST_PROJECT}"

run_test "Criar service account de teste" \
    "oc create sa test-sa -n ${TEST_PROJECT} 2>/dev/null || echo 'SA já existe'"

run_test "Dar permissão view para SA" \
    "oc adm policy add-role-to-user view system:serviceaccount:${TEST_PROJECT}:test-sa -n ${TEST_PROJECT} 2>/dev/null || echo 'Permissão já existe'"

run_test "Listar SCC (Security Context Constraints)" \
    "oc get scc | head -15"

run_test "Descrever SCC restricted" \
    "oc describe scc restricted | head -30"

run_test "Ver quem pode usar SCC anyuid" \
    "oc get scc anyuid -o jsonpath='{.users}' 2>/dev/null || echo 'SCC não encontrado'"

run_test "Deletar role de teste" \
    "oc delete role test-role -n ${TEST_PROJECT} 2>/dev/null || echo 'Role não encontrado'"

run_test "Deletar service account de teste" \
    "oc delete sa test-sa -n ${TEST_PROJECT} 2>/dev/null || echo 'SA não encontrado'"

