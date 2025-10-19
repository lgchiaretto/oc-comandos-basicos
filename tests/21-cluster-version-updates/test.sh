#!/bin/bash

##############################################################################
# Teste: 21 - CLUSTER VERSION E UPDATES
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "21 - CLUSTER VERSION E UPDATES"

run_test "Ver versão do cluster" \
    "oc get clusterversion"

run_test "Descrever ClusterVersion" \
    "oc describe clusterversion version"

run_test "Ver histórico de updates" \
    "oc get clusterversion version -o jsonpath='{.status.history}' | head -200 || true"

