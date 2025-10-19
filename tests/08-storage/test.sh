#!/bin/bash

##############################################################################
# Teste: 08 - STORAGE
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "08 - STORAGE"

run_test "Listar PVCs com status" \
    "oc get pvc -A | head -10 || true"

run_test "PVCs Pending" \
    "oc get pvc -A --field-selector=status.phase=Pending | head -10 || true"

run_test "Listar StorageClasses" \
    "oc get storageclass"

