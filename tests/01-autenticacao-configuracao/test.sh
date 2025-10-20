#!/bin/bash

##############################################################################
# Teste: 01 - AUTENTICAÇÃO E CONFIGURAÇÃO
# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
section_header "01 - AUTENTICAÇÃO E CONFIGURAÇÃO"

run_test "Verificar usuário atual" \
    "oc whoami"

run_test "Verificar token de acesso" \
    "oc whoami -t"

run_test "Verificar contexto atual" \
    "oc whoami --show-context"

run_test "Verificar a URL da console" \
    "oc whoami --show-console"

run_test "Verificar servidor conectado" \
    "oc whoami --show-server"

run_test "Listar todos os recursos da API disponíveis" \
    "oc api-resources"

run_test "Filtrar por verbo" \
    "oc api-resources --verbs=list,get"

run_test "Filtrar por grupo de API" \
    "oc api-resources --api-group=apps"

run_test "Ver recursos com alias" \
    "oc api-resources | grep -E '^(NAME|pod|deploy|svc)'"

run_test "Listar todas as versões da API disponíveis" \
    "oc api-versions"

run_test "Verificar versão do oc" \
    "oc version"

run_test "Verificar informações do cluster" \
    "oc cluster-info"

run_test "Ver informações do servidor" \
    "oc cluster-info dump"

run_test "Exibir configuração atual" \
    "oc config view"

run_test "Exibir configuração com credenciais (cuidado!)" \
    "oc config view --raw"

run_test "Ver arquivo de configuração ~/.kube/config" \
    "cat ~/.kube/config"

run_test "Listar todos os contextos" \
    "oc config get-contexts"

run_test "Ver contexto atual" \
    "oc config current-context"

run_test "Múltiplos Clusters: config set-cluster" \
    "oc config set-cluster test-app"

run_test "Múltiplos Clusters: config set-credentials" \
    "oc config set-credentials test-app"

run_test "Testar conexão com API" \
    "oc get --raw /healthz"

run_test "Status de Conexão: Listar --raw" \
    "oc get --raw /healthz -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
