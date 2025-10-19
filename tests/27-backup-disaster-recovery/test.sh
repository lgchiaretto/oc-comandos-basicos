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

