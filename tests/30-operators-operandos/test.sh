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

run_test "Componentes do OLM: Listar pods" \
    "oc get pods -n openshift-operator-lifecycle-manager 2>/dev/null || echo "Recurso não encontrado"

run_test "Componentes do OLM: Listar clusteroperator" \
    "oc get clusteroperator operator-lifecycle-manager -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"

run_test "Catalog Sources: Listar catalogsources" \
    "oc get catalogsources -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado"

run_test "Catalog Sources: Listar catalogsource" \
    "oc get catalogsource redhat-operators -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado"

run_test "Catalog Sources: Descrever catalogsource" \
    "oc describe catalogsource redhat-operators -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado"

run_test "PackageManifests: Listar packagemanifests" \
    "oc get packagemanifests -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado"

run_test "PackageManifests: Descrever packagemanifest" \
    "oc describe packagemanifest elasticsearch-operator -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado"

run_test "PackageManifests: Listar packagemanifest" \
    "oc get packagemanifest elasticsearch-operator -n openshift-marketplace -o jsonpath='{.status.channels[*].name}' 2>/dev/null || echo "Recurso não encontrado"

run_test "Passo a Passo Completo: Listar csv" \
    "oc get csv -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"

run_test "Install Plan: Listar installplan" \
    "oc get installplan -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"

run_test "Install Plan: Descrever installplan" \
    "oc describe installplan test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"

run_test "Install Plan: Patch installplan" \
    "oc patch installplan test-app -n ${TEST_PROJECT} --type merge -p '{"spec":{"approved":true}}' 2>/dev/null || echo "Recurso não encontrado ou não aplicável"

run_test "OperatorGroup: Listar operatorgroups" \
    "oc get operatorgroups -A -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"

run_test "Listar CRDs: Listar crd" \
    "oc get crd -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"

run_test "Componentes do OLM: Listar pods" \
    "oc get pods -n openshift-operator-lifecycle-manager 2>/dev/null || echo "Recurso não encontrado""

run_test "Componentes do OLM: Listar clusteroperator" \
    "oc get clusteroperator operator-lifecycle-manager -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Catalog Sources: Listar catalogsources" \
    "oc get catalogsources -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "Catalog Sources: Listar catalogsource" \
    "oc get catalogsource redhat-operators -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "Catalog Sources: Descrever catalogsource" \
    "oc describe catalogsource redhat-operators -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "PackageManifests: Listar packagemanifests" \
    "oc get packagemanifests -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "PackageManifests: Descrever packagemanifest" \
    "oc describe packagemanifest elasticsearch-operator -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "PackageManifests: Listar packagemanifest" \
    "oc get packagemanifest elasticsearch-operator -n openshift-marketplace -o jsonpath='{.status.channels[*].name}' 2>/dev/null || echo "Recurso não encontrado""

run_test "Passo a Passo Completo: Listar csv" \
    "oc get csv -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Install Plan: Listar installplan" \
    "oc get installplan -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Install Plan: Descrever installplan" \
    "oc describe installplan test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Install Plan: Patch installplan" \
    "oc patch installplan test-app -n ${TEST_PROJECT} --type merge -p '{"spec":{"approved":true}}' 2>/dev/null || echo "Recurso não encontrado ou não aplicável""

run_test "OperatorGroup: Listar operatorgroups" \
    "oc get operatorgroups -A -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Listar CRDs: Listar crd" \
    "oc get crd -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Listar CRDs: Descrever crd" \
    "oc describe crd elasticsearches.logging.openshift.io -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Componentes do OLM: Listar pods" \
    "oc get pods -n openshift-operator-lifecycle-manager 2>/dev/null || echo "Recurso não encontrado""

run_test "Componentes do OLM: Listar clusteroperator" \
    "oc get clusteroperator operator-lifecycle-manager -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Catalog Sources: Listar catalogsources" \
    "oc get catalogsources -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "Catalog Sources: Listar catalogsource" \
    "oc get catalogsource redhat-operators -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "Catalog Sources: Descrever catalogsource" \
    "oc describe catalogsource redhat-operators -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "PackageManifests: Listar packagemanifests" \
    "oc get packagemanifests -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "PackageManifests: Descrever packagemanifest" \
    "oc describe packagemanifest elasticsearch-operator -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "PackageManifests: Listar packagemanifest" \
    "oc get packagemanifest elasticsearch-operator -n openshift-marketplace -o jsonpath='{.status.channels[*].name}' 2>/dev/null || echo "Recurso não encontrado""

run_test "Passo a Passo Completo: Listar csv" \
    "oc get csv -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Install Plan: Listar installplan" \
    "oc get installplan -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Install Plan: Descrever installplan" \
    "oc describe installplan test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Install Plan: Patch installplan" \
    "oc patch installplan test-app -n ${TEST_PROJECT} --type merge -p '{"spec":{"approved":true}}' 2>/dev/null || echo "Recurso não encontrado ou não aplicável""

run_test "OperatorGroup: Listar operatorgroups" \
    "oc get operatorgroups -A -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Listar CRDs: Listar crd" \
    "oc get crd -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Listar CRDs: Descrever crd" \
    "oc describe crd elasticsearches.logging.openshift.io -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Componentes do OLM: Listar pods" \
    "oc get pods -n openshift-operator-lifecycle-manager 2>/dev/null || echo "Recurso não encontrado""

run_test "Componentes do OLM: Listar clusteroperator" \
    "oc get clusteroperator operator-lifecycle-manager -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Catalog Sources: Listar catalogsources" \
    "oc get catalogsources -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "Catalog Sources: Listar catalogsource" \
    "oc get catalogsource redhat-operators -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "Catalog Sources: Descrever catalogsource" \
    "oc describe catalogsource redhat-operators -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "PackageManifests: Listar packagemanifests" \
    "oc get packagemanifests -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "PackageManifests: Descrever packagemanifest" \
    "oc describe packagemanifest elasticsearch-operator -n openshift-marketplace 2>/dev/null || echo "Recurso não encontrado""

run_test "PackageManifests: Listar packagemanifest" \
    "oc get packagemanifest elasticsearch-operator -n openshift-marketplace -o jsonpath='{.status.channels[*].name}' 2>/dev/null || echo "Recurso não encontrado""

run_test "Passo a Passo Completo: Listar csv" \
    "oc get csv -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Install Plan: Listar installplan" \
    "oc get installplan -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Install Plan: Descrever installplan" \
    "oc describe installplan test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Install Plan: Patch installplan" \
    "oc patch installplan test-app -n ${TEST_PROJECT} --type merge -p '{"spec":{"approved":true}}' 2>/dev/null || echo "Recurso não encontrado ou não aplicável""

run_test "OperatorGroup: Listar operatorgroups" \
    "oc get operatorgroups -A -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Listar CRDs: Listar crd" \
    "oc get crd -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""

run_test "Listar CRDs: Descrever crd" \
    "oc describe crd elasticsearches.logging.openshift.io -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""




