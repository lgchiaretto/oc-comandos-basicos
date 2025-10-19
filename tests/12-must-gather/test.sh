#!/bin/bash

##############################################################################
# Teste: 12 - MUST-GATHER
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "12 - MUST-GATHER"

run_test "Verificar comando must-gather (sem executar)" \
    "oc adm must-gather --help | head -5 || true"

