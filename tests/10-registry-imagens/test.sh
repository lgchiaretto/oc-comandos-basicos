#!/bin/bash

##############################################################################
# Teste: 10 - REGISTRY E IMAGENS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "10 - REGISTRY E IMAGENS"

run_test "Verificar registry interno" \
    "oc get route -n openshift-image-registry 2>/dev/null || echo 'Registry route não exposta'"

run_test "Listar ImageStreams do sistema" \
    "oc get is -n openshift | head -10 || true"

run_test "Ver tags de uma ImageStream" \
    "oc get is -n openshift -o name | head -1 | xargs oc get -n openshift -o jsonpath='{.spec.tags[*].name}' 2>/dev/null || echo 'N/A'"

