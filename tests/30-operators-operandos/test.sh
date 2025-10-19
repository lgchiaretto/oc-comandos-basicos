#!/bin/bash

##############################################################################
# Teste: 30 - OPERATORS E OPERANDOS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "30 - OPERATORS E OPERANDOS"

run_test "Verificar OLM" \
    "oc get pods -n openshift-operator-lifecycle-manager | head -5 || true"

run_test "Listar Catalog Sources" \
    "oc get catalogsources -n openshift-marketplace"

run_test "Listar PackageManifests" \
    "oc get packagemanifests -n openshift-marketplace | head -10 || true"

run_test "Listar Subscriptions" \
    "oc get subscriptions -A | head -10 || true"

run_test "Listar CSVs" \
    "oc get csv -A | head -10 || true"

run_test "Listar InstallPlans" \
    "oc get installplan -A | head -10 || true"

run_test "Listar OperatorGroups" \
    "oc get operatorgroups -A | head -10 || true"

run_test "Listar CRDs" \
    "oc get crd | head -10 || true"

