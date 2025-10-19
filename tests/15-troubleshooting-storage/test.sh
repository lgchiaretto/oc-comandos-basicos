#!/bin/bash

##############################################################################
# Teste: 15 - Troubleshooting Storage
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "15 - TROUBLESHOOTING STORAGE"

run_test "Listar PVCs com status" \
    "oc get pvc -A 2>/dev/null | head -10 || true"

run_test "PVCs Pending" \
    "oc get pvc -A --field-selector=status.phase=Pending 2>/dev/null | head -10 || true"

run_test "Listar StorageClasses" \
    "oc get storageclass"
