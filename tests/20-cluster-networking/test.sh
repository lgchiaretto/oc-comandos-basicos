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

run_test "Listar Ingress Controllers" \
    "oc get ingresscontroller -n openshift-ingress-operator"

