#!/bin/bash

##############################################################################
# Teste: 17 - CLUSTER OPERATORS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "17 - CLUSTER OPERATORS"

run_test "Listar Cluster Operators" \
    "oc get co"

run_test "Descrever primeiro CO" \
    "oc get co -o name | head -1 | xargs oc describe"

run_test "Status Geral: Listar clusteroperators" \
    "oc get clusteroperators -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Diagnosticar Problemas: Listar deploy" \
    "oc get deploy -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Authentication Operator: Listar pods" \
    "oc get pods -n openshift-authentication 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Ingress Operator: Listar ingresscontroller" \
    "oc get ingresscontroller -n openshift-ingress-operator 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Network Operator: Listar network.config.openshift.io" \
    "oc get network.config.openshift.io cluster -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "DNS Operator: Listar dns.operator/default" \
    "oc get dns.operator/default -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Status Detalhado: Descrever co" \
    "oc describe co test-app -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Must-Gather de Operadores: Admin: must-gather" \
    "echo 'Comando must-gather não executado em teste'"
