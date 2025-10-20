#!/bin/bash

##############################################################################
# Teste: 07 - CONFIGMAPS E SECRETS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "07 - CONFIGMAPS E SECRETS"

run_test "Listar ConfigMaps" \
    "oc get configmaps -n ${TEST_PROJECT}"

run_test "Listar ConfigMaps (cm)" \
    "oc get cm -n ${TEST_PROJECT}"

run_test "Ver conteúdo do ConfigMap" \
    "oc get cm test-config -o yaml -n ${TEST_PROJECT}"

run_test "Ver apenas as chaves do ConfigMap" \
    "oc get cm test-config -o jsonpath='{.data}' -n ${TEST_PROJECT}"

run_test "Listar Secrets" \
    "oc get secrets -n ${TEST_PROJECT}"

run_test "Ver secret em YAML" \
    "oc get secret test-secret -o yaml -n ${TEST_PROJECT}"

run_test "Ver chaves do Secret" \
    "oc get secret test-secret -n ${TEST_PROJECT} -o jsonpath='{.data}'"

run_test "Criar ConfigMap de teste" \
    "oc create configmap test-config --from-literal=key1=value1 --from-literal=key2=value2 -n ${TEST_PROJECT} 2>/dev/null || echo 'ConfigMap já existe'"

run_test "Criar Secret genérico" \
    "oc create secret generic test-secret --from-literal=password=mypassword -n ${TEST_PROJECT} 2>/dev/null || echo 'Secret já existe'"

run_test "Exemplo prático" \
    "oc describe configmap test-config -n ${TEST_PROJECT}"

run_test "Exemplo prático" \
    "oc describe secret test-secret -n ${TEST_PROJECT}"

run_test "Link secret a service account" \
    "oc secrets link default test-secret -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado ou não aplicável'"

run_test "Configurar env do deployment com configmap" \
    "oc set env deployment/test-app --from=configmap/test-config -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado ou não aplicável'"

run_test "Configurar volume do deployment com configmap" \
    "oc set volume deployment/test-app --add -t configmap --name=config-vol --mount-path=/etc/config --configmap-name=test-config -n ${TEST_PROJECT} 2>/dev/null || echo 'Recurso não encontrado ou não aplicável'"
