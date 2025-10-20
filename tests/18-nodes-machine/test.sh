#!/bin/bash

##############################################################################
# Teste: 18 - NODES E MACHINE
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "18 - NODES E MACHINE"
run_test "Listar nodes" \
    "oc get nodes"

run_test "Listar nodes com detalhes" \
    "oc get nodes -o wide"

run_test "Descrever primeiro node" \
    "oc get nodes -o name | head -1 | xargs oc describe"

run_test "Listar machines" \
    "oc get machines -n openshift-machine-api"

run_test "Listar machinesets" \
    "oc get machinesets -n openshift-machine-api"

run_test "Listar e Verificar: Listar nodes" \
    "oc get nodes -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Listar e Verificar: Admin: top" \
    "oc adm top nodes 2>/dev/null || echo 'Metrics não disponíveis'"

run_test "MachineConfigs: Listar machineconfigs" \
    "oc get machineconfigs -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "MachineConfigPools: Listar machineconfigpools" \
    "oc get machineconfigpools -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado'"

run_test "Gerenciar MachineSets: Listar machinesets" \
    "oc get machinesets -n openshift-machine-api 2>/dev/null || echo 'Recurso não encontrado'"
