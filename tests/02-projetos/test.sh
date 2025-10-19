#!/bin/bash

##############################################################################
# Teste: 02 - PROJETOS
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "02 - PROJETOS"

run_test "Listar todos os projetos" \
    "oc projects"

run_test "Listar projetos (formato detalhado)" \
    "oc get projects 2>/dev/null | head -10 || true"

run_test "Criar novo projeto de teste" \
    "oc new-project ${TEST_PROJECT} --description='Projeto de teste' --display-name='Test Validation'"

run_test "Ver projeto atual" \
    "oc project"

run_test "Adicionar label ao projeto" \
    "oc label namespace ${TEST_PROJECT} test-validation=true env=test --overwrite"

run_test "Descrever projeto" \
    "oc describe project ${TEST_PROJECT}"

run_test "Ver projeto em YAML" \
    "oc get project ${TEST_PROJECT} -o yaml"

run_test "Verificar quotas do projeto" \
    "oc get quota -n ${TEST_PROJECT}"

run_test "Ver limit ranges" \
    "oc get limitrange -n ${TEST_PROJECT}"

run_test "Status do projeto" \
    "oc status -n ${TEST_PROJECT}"

run_test "Filtrar projetos com label" \
    "oc get projects -l test-validation=true"

run_test "Verificar se pode criar projeto" \
    "oc auth can-i create projects"

run_test "Ver rolebindings do projeto" \
    "oc get rolebindings -n ${TEST_PROJECT}"

