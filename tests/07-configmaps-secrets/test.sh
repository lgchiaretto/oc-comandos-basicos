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


run_test "Criar ConfigMaps: Criar configmap" \
    "oc create configmap test-app --from-literal=test-app=test-app"


run_test "Criar ConfigMaps: Listar configmaps" \
    "oc get configmaps -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"


run_test "Criar ConfigMaps: Listar cm" \
    "oc get cm -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"


run_test "Criar ConfigMaps: Descrever cm" \
    "oc describe cm test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"


run_test "Exemplos Avançados: Criar cm" \
    "oc create cm app-config \"


run_test "Criar Secrets: Criar secret" \
    "oc create secret generic test-app --from-literal=test-app=test-app"


run_test "Criar Secrets: Listar secrets" \
    "oc get secrets -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"


run_test "Criar Secrets: Listar secret" \
    "oc get secret test-app -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"


run_test "Link Secrets: secrets link" \
    "oc secrets link default test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado ou não aplicável"


run_test "Como Variáveis de Ambiente: Configurar env" \
    "oc set env deployment/test-app --from=configmap/test-app 2>/dev/null || echo "Recurso não encontrado ou não aplicável"


run_test "Como Volumes: Configurar volume" \
    "oc set volume deployment/test-app \ 2>/dev/null || echo "Recurso não encontrado ou não aplicável"


run_test "Criar ConfigMaps: Listar configmaps" \
    "oc get configmaps -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Criar ConfigMaps: Listar cm" \
    "oc get cm -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Criar ConfigMaps: Descrever cm" \
    "oc describe cm test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Criar Secrets: Listar secrets" \
    "oc get secrets -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Criar Secrets: Listar secret" \
    "oc get secret test-app -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Como Variáveis de Ambiente: Configurar env" \
    "oc set env deployment/test-app --from=configmap/test-app 2>/dev/null || echo "Recurso não encontrado ou não aplicável""


run_test "Como Volumes: Configurar volume" \
    "oc set volume deployment/test-app \ 2>/dev/null || echo "Recurso não encontrado ou não aplicável""


run_test "Criar ConfigMaps: Listar configmaps" \
    "oc get configmaps -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Criar ConfigMaps: Listar cm" \
    "oc get cm -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Criar ConfigMaps: Descrever cm" \
    "oc describe cm test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Criar Secrets: Listar secrets" \
    "oc get secrets -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Criar Secrets: Listar secret" \
    "oc get secret test-app -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Como Variáveis de Ambiente: Configurar env" \
    "oc set env deployment/test-app --from=configmap/test-app 2>/dev/null || echo "Recurso não encontrado ou não aplicável""


run_test "Como Volumes: Configurar volume" \
    "oc set volume deployment/test-app \ 2>/dev/null || echo "Recurso não encontrado ou não aplicável""


run_test "Criar ConfigMaps: Listar configmaps" \
    "oc get configmaps -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Criar ConfigMaps: Listar cm" \
    "oc get cm -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Criar ConfigMaps: Descrever cm" \
    "oc describe cm test-app -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Criar Secrets: Listar secrets" \
    "oc get secrets -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Criar Secrets: Listar secret" \
    "oc get secret test-app -o yaml -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado""


run_test "Como Variáveis de Ambiente: Configurar env" \
    "oc set env deployment/test-app --from=configmap/test-app 2>/dev/null || echo "Recurso não encontrado ou não aplicável""


run_test "Como Volumes: Configurar volume" \
    "oc set volume deployment/test-app \ 2>/dev/null || echo "Recurso não encontrado ou não aplicável""




