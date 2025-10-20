#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

MODULE_NUM=$(basename "$(dirname "$0")" | cut -d'-' -f1)
section_header "$MODULE_NUM - $(basename "$(dirname "$0")" | cut -d'-' -f2- | tr '-' ' ' | tr '[:lower:]' '[:upper:]')"

run_test "Listar PVCs no projeto de teste" \
    "oc get pvc -n ${TEST_PROJECT}"


run_test "Listar PVs do cluster" \
    "oc get pv | head -10"


run_test "Verificar storage classes disponíveis" \
    "oc get sc"


run_test "Ver eventos relacionados a storage" \
    "oc get events -n ${TEST_PROJECT} --field-selector involvedObject.kind=PersistentVolumeClaim | head -10"


run_test "Descrever storage class padrão" \
    "oc describe sc \$(oc get sc -o jsonpath='{.items[?(@.metadata.annotations.storageclass\.kubernetes\.io/is-default-class==\"true\")].metadata.name}' 2>/dev/null) 2>/dev/null || echo 'Nenhuma SC padrão'"


run_test "Listar pods com volumes" \
    "oc get pods -n ${TEST_PROJECT} -o json | grep -i volumemount | head -5 || echo 'Sem pods com volumes'"


run_test "Ver PVCs por status" \
    "oc get pvc -A --field-selector=status.phase=Bound | head -10"


run_test "Verificar se pode criar PVC" \
    "oc auth can-i create pvc -n ${TEST_PROJECT}"

