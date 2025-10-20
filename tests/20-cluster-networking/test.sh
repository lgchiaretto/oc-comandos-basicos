#!/bin/bash

##############################################################################
# Teste: 20 - CLUSTER NETWORKING
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "20 - CLUSTER NETWORKING"

run_test "Ver configuração de rede do cluster" \
    "oc get network.config.openshift.io cluster -o yaml | head -30 || true"

run_test "Listar Network Policies" \
    "oc get networkpolicy -n ${TEST_PROJECT}"

run_test "Listar IngressControllers" \
    "oc get ingresscontroller -n openshift-ingress-operator"

run_test "Ver configuração de rede do cluster" \
    "oc get network.config.openshift.io cluster -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Network operator config" \
    "oc get network.operator.openshift.io cluster -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Ver IPs de todos os pods" \
    "oc get pods -o wide -A -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Criar Network Policies: Listar netpol" \
    "oc get netpol -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Testar Network Policies: Listar events" \
    "oc get events -n ${TEST_PROJECT} | grep -i network 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Egress IP: Listar egressip" \
    "oc get egressip -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Egress Firewall [OVN]: Listar egressfirewall" \
    "oc get egressfirewall -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Escalar número de réplicas do IngressController" \
    "oc scale ingresscontroller -n openshift-ingress-operator --replicas=2 default 2>/dev/null || echo 'Não foi possível escalar'"
