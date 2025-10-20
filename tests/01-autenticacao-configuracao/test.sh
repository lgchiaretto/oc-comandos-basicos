#!/bin/bash

##############################################################################
# Teste: 01 - AUTENTICAÇÃO E CONFIGURAÇÃO
# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
section_header "01 - AUTENTICAÇÃO E CONFIGURAÇÃO"

run_test "Verificar usuário atual (whoami)" \
    "oc whoami"

run_test "Verificar token de acesso" \
    "oc whoami -t"

run_test "Verificar contexto atual" \
    "oc whoami --show-context"

run_test "Verificar URL da console" \
    "oc whoami --show-console"

run_test "Verificar servidor conectado" \
    "oc whoami --show-server"

run_test "Verificar versão do oc" \
    "oc version"

run_test "Verificar informações do cluster" \
    "oc cluster-info"

run_test "Exibir configuração atual" \
    "oc config view"

run_test "Listar todos os contextos" \
    "oc config get-contexts"

run_test "Ver contexto atual" \
    "oc config current-context"

run_test "Testar conexão com API" \
    "oc get --raw /healthz"

run_test "Ver endpoints da API" \
    "oc api-resources 2>/dev/null | head -20 || true"

run_test "Ver versões da API" \
    "oc api-versions 2>/dev/null | head -20 || true"
    
run_test "Versão e Informações: cluster-info dump" \
    "oc cluster-info dump"

#run_test "Namespace Padrão: config set-context" \#
#    "oc config set-context --current --namespace=default"#

#run_test "Listar e Gerenciar Contextos: config use-context" \
#    "oc config use-context default"

#run_test "Listar e Gerenciar Contextos: config rename-context" \
#    "oc config rename-context default cluster-default"

run_test "Status de Conexão: whoami 2>/dev/null" \
    "oc whoami 2>/dev/null && echo "Conectado" || echo "Não conectado"

run_test "Status de Conexão: Listar --raw" \
    "oc get --raw /healthz -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"

run_test "Status de Conexão: api-resources " \
    "oc api-resources"

run_test "Status de Conexão: api-versions " \
    "oc api-versions"
    
#run_test "Troubleshooting de Conexão: --proxy-url=http://proxy:port login" \
#    "oc --proxy-url=http://proxy:port login test-app"

run_test "Múltiplos Clusters: config set-cluster" \
    "oc config set-cluster test-app"

run_test "Múltiplos Clusters: config set-credentials" \
    "oc config set-credentials test-app"
#    "oc whoami 2>/dev/null && echo "Conectado" || echo "Não conectado"
#    "oc get --raw /healthz -n ${TEST_PROJECT} 2>/dev/null || echo "Recurso não encontrado"
