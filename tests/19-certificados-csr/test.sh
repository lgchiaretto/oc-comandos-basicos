#!/bin/bash

##############################################################################
# Teste: 19 - CERTIFICADOS E CSR
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "19 - CERTIFICADOS E CSR"

run_test "Listar CSRs" \
    "oc get csr | head -10 || true"

run_test "CSRs Pending" \
    "oc get csr | grep -E Pending || echo 'Nenhum CSR pendente'"

