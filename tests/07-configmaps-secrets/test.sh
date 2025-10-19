#!/bin/bash

##############################################################################
# Teste: 07 - CONFIGMAPS E SECRETS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "07 - CONFIGMAPS E SECRETS"

run_test "Criar ConfigMap" \
    "oc create configmap test-config --from-literal=key1=value1 --from-literal=key2=value2 -n ${TEST_PROJECT}"

run_test "Listar ConfigMaps" \
    "oc get configmap -n ${TEST_PROJECT}"

run_test "Descrever ConfigMap" \
    "oc describe configmap test-config -n ${TEST_PROJECT}"

run_test "Ver ConfigMap em YAML" \
    "oc get configmap test-config -n ${TEST_PROJECT} -o yaml"

run_test "Criar Secret" \
    "oc create secret generic test-secret --from-literal=password=mypassword -n ${TEST_PROJECT}"

run_test "Listar Secrets" \
    "oc get secrets -n ${TEST_PROJECT}"

run_test "Descrever Secret" \
    "oc describe secret test-secret -n ${TEST_PROJECT}"

run_test "Ver chaves do Secret" \
    "oc get secret test-secret -n ${TEST_PROJECT} -o jsonpath='{.data}'"

