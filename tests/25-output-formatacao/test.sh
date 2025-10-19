#!/bin/bash

##############################################################################
# Teste: 25 - OUTPUT E FORMATAÇÃO
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "25 - OUTPUT E FORMATAÇÃO"

run_test "Output em JSON" \
    "oc get pods -n ${TEST_PROJECT} -o json | head -50 || true"

run_test "Output em YAML" \
    "oc get pods -n ${TEST_PROJECT} -o yaml | head -50 || true"

run_test "Output com JSONPath" \
    "oc get pods -n ${TEST_PROJECT} -o jsonpath='{.items[*].metadata.name}'"

run_test "Custom columns" \
    "oc get pods -n ${TEST_PROJECT} -o custom-columns=NAME:.metadata.name,STATUS:.status.phase"

