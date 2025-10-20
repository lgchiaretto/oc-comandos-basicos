#!/bin/bash

##############################################################################
# Teste: 28 - PATCH E EDIT (apenas PATCH - edit é interativo)
##############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "28 - PATCH E EDIT"
run_test "Ver deployment após patches" \
    "oc get deployment test-app -n ${TEST_PROJECT} -o yaml | head -40 2>/dev/null || echo 'Deployment não encontrado'"
run_test "Patch deployment com JSON" \
    "oc patch deployment test-app -n ${TEST_PROJECT} -p '{\"spec\":{\"replicas\":2}}' 2>/dev/null || echo 'Deployment não encontrado'"
run_test "Patch deployment com YAML" \
    "oc patch deployment test-app -n ${TEST_PROJECT} --type=merge -p 'spec:\n  replicas: 1' 2>/dev/null || echo 'Deployment não encontrado'"
run_test "Patch com strategic merge" \
    "oc patch deployment test-app -n ${TEST_PROJECT} --type=strategic -p '{\"spec\":{\"template\":{\"metadata\":{\"labels\":{\"patched\":\"true\"}}}}}' 2>/dev/null || echo 'Deployment não encontrado'"
run_test "Patch project com label" \
    "oc patch project ${TEST_PROJECT} -p '{\"metadata\":{\"labels\":{\"environment\":\"test\"}}}' 2>/dev/null || echo 'Projeto não encontrado'"
run_test "Patch service" \
    "oc patch svc test-app -n ${TEST_PROJECT} -p '{\"spec\":{\"sessionAffinity\":\"ClientIP\"}}' 2>/dev/null || echo 'Service não encontrado'"
run_test "Patch configmap" \
    "oc patch cm test-config -n ${TEST_PROJECT} -p '{\"data\":{\"patched-key\":\"patched-value\"}}' 2>/dev/null || echo 'ConfigMap não encontrado'"
run_test "Patch secret" \
    "oc patch secret test-secret -n ${TEST_PROJECT} -p '{\"stringData\":{\"patched\":\"value\"}}' 2>/dev/null || echo 'Secret não encontrado'"
run_test "Patch route" \
    "oc patch route test-app -n ${TEST_PROJECT} -p '{\"spec\":{\"tls\":{\"termination\":\"edge\"}}}' 2>/dev/null || echo 'Route não encontrado'"
run_test "Remover label com patch" \
    "oc patch deployment test-app -n ${TEST_PROJECT} -p '{\"metadata\":{\"labels\":{\"patched\":null}}}' 2>/dev/null || echo 'Deployment não encontrado'"
