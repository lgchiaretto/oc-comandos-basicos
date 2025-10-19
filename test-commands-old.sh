#!/bin/bash

##############################################################################
# Script de Validação de Comandos OpenShift
# Valida todos os comandos documentados nos arquivos 01-30
#
# Uso: ./test-commands.sh [--verbose] [--stop-on-error]
#
# Opções:
#   --verbose        Mostra saída detalhada de cada comando
#   --stop-on-error  Para execução no primeiro erro
#   --skip-destructive  Pula comandos destrutivos (delete, etc)
##############################################################################

set -o pipefail

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variáveis globais
VERBOSE=0
STOP_ON_ERROR=0
SKIP_DESTRUCTIVE=1  # Default: skip destructive commands
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0
LOG_FILE="test-commands-$(date +%Y%m%d-%H%M%S).log"
PROJECT_PREFIX="test-validation"
TEMP_PROJECT="${PROJECT_PREFIX}-$(date +%s)"

# Parse argumentos
for arg in "$@"; do
    case $arg in
        --verbose)
            VERBOSE=1
            ;;
        --stop-on-error)
            STOP_ON_ERROR=1
            ;;
        --skip-destructive)
            SKIP_DESTRUCTIVE=1
            ;;
        --allow-destructive)
            SKIP_DESTRUCTIVE=0
            ;;
        *)
            echo "Uso: $0 [--verbose] [--stop-on-error] [--skip-destructive]"
            exit 1
            ;;
    esac
done

# Funções de logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1" | tee -a "$LOG_FILE"
}

log_skip() {
    echo -e "${YELLOW}[SKIP]${NC} $1" | tee -a "$LOG_FILE"
}

# Função para executar comando com validação
run_test() {
    local description="$1"
    local command="$2"
    local should_skip="${3:-0}"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [ "$should_skip" -eq 1 ]; then
        log_skip "$description"
        SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
        return 0
    fi
    
    if [ "$VERBOSE" -eq 1 ]; then
        log_info "Executando: $command"
    fi
    
    echo "# Test $TOTAL_TESTS: $description" >> "$LOG_FILE"
    echo "# Command: $command" >> "$LOG_FILE"
    
    if eval "$command" >> "$LOG_FILE" 2>&1; then
        log_success "$description"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        log_error "$description"
        log_error "  Comando: $command"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        
        if [ "$STOP_ON_ERROR" -eq 1 ]; then
            log_error "Parando execução devido ao erro (--stop-on-error)"
            exit 1
        fi
        return 1
    fi
}

# Função para verificar pré-requisitos
check_prerequisites() {
    log_info "Verificando pré-requisitos..."
    
    # Verificar se oc está instalado
    if ! command -v oc &> /dev/null; then
        log_error "Comando 'oc' não encontrado. Instale o OpenShift CLI."
        exit 1
    fi
    
    # Verificar autenticação
    if ! oc whoami &> /dev/null; then
        log_error "Não autenticado no cluster. Execute 'oc login' primeiro."
        exit 1
    fi
    
    # Verificar permissões básicas
    if ! oc auth can-i create projects &> /dev/null; then
        log_warning "Usuário pode não ter permissão para criar projetos. Alguns testes podem falhar."
    fi
    
    log_success "Pré-requisitos verificados"
    echo ""
}

# Função de limpeza
cleanup() {
    log_info "Executando limpeza..."
    
    # Deletar projetos de teste
    oc delete project -l "test-validation=true" --wait=false 2>/dev/null || true
    
    log_success "Limpeza concluída"
}

# Trap para garantir limpeza
trap cleanup EXIT

# Banner inicial
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     Script de Validação de Comandos OpenShift                 ║"
echo "║     Testando comandos da documentação 01-30                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
log_info "Iniciando validação em $(date)"
log_info "Cluster: $(oc whoami --show-server)"
log_info "Usuário: $(oc whoami)"
log_info "Log: $LOG_FILE"
echo ""

# Verificar pré-requisitos
check_prerequisites

##############################################################################
# 01 - AUTENTICAÇÃO E CONFIGURAÇÃO
##############################################################################
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "01 - AUTENTICAÇÃO E CONFIGURAÇÃO"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

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

##############################################################################
# 02 - PROJETOS
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "02 - PROJETOS"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar todos os projetos" \
    "oc projects"

run_test "Listar projetos (formato detalhado)" \
    "oc get projects 2>/dev/null | head -10 || true"

run_test "Ver projeto atual" \
    "oc project"

run_test "Criar novo projeto de teste" \
    "oc new-project ${TEMP_PROJECT} --description='Projeto de teste' --display-name='Test Validation'"

run_test "Adicionar label ao projeto" \
    "oc label namespace ${TEMP_PROJECT} test-validation=true env=test --overwrite"

run_test "Descrever projeto" \
    "oc describe project ${TEMP_PROJECT}"

run_test "Ver projeto em YAML" \
    "oc get project ${TEMP_PROJECT} -o yaml"

run_test "Verificar quotas do projeto" \
    "oc get quota -n ${TEMP_PROJECT}"

run_test "Ver limit ranges" \
    "oc get limitrange -n ${TEMP_PROJECT}"

run_test "Status do projeto" \
    "oc status -n ${TEMP_PROJECT}"

run_test "Filtrar projetos com label" \
    "oc get projects -l test-validation=true"

run_test "Verificar se pode criar projeto" \
    "oc auth can-i create projects"

run_test "Ver rolebindings do projeto" \
    "oc get rolebindings -n ${TEMP_PROJECT}"

##############################################################################
# 03 - APLICAÇÕES
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "03 - APLICAÇÕES"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Criar aplicação de teste (nginx)" \
    "oc new-app nginx:latest --name=test-app -n ${TEMP_PROJECT}"

run_test "Aguardar deployment" \
    "sleep 10"

run_test "Listar todas as aplicações" \
    "oc get all -n ${TEMP_PROJECT}"

run_test "Listar deployments" \
    "oc get deployment -n ${TEMP_PROJECT}"

run_test "Listar services" \
    "oc get svc -n ${TEMP_PROJECT}"

run_test "Expor service como route" \
    "oc expose service test-app -n ${TEMP_PROJECT}"

run_test "Listar routes" \
    "oc get routes -n ${TEMP_PROJECT}"

run_test "Listar templates disponíveis" \
    "oc get templates -n openshift | head -10 || true"

##############################################################################
# 04 - PODS E CONTAINERS
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "04 - PODS E CONTAINERS"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar todos os pods" \
    "oc get pods -n ${TEMP_PROJECT}"

run_test "Listar pods com mais informações" \
    "oc get pods -n ${TEMP_PROJECT} -o wide"

run_test "Listar pods em todos os namespaces" \
    "oc get pods -A | head -20 || true"

run_test "Descrever primeiro pod" \
    "oc get pods -n ${TEMP_PROJECT} -o name | head -1 | xargs -I {} oc describe {} -n ${TEMP_PROJECT}"

run_test "Ver logs do pod" \
    "oc get pods -n ${TEMP_PROJECT} -o name | head -1 | xargs -I {} oc logs {} -n ${TEMP_PROJECT} --tail=10"

run_test "Listar pods com labels" \
    "oc get pods -n ${TEMP_PROJECT} --show-labels"

run_test "Filtrar pods por label" \
    "oc get pods -n ${TEMP_PROJECT} -l deployment=test-app"

run_test "Ver eventos do namespace" \
    "oc get events -n ${TEMP_PROJECT} --sort-by='.lastTimestamp' | head -10 || true"

##############################################################################
# 05 - DEPLOYMENTS E SCALING
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "05 - DEPLOYMENTS E SCALING"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar deployments" \
    "oc get deployment -n ${TEMP_PROJECT}"

run_test "Descrever deployment" \
    "oc describe deployment test-app -n ${TEMP_PROJECT}"

run_test "Ver deployment em YAML" \
    "oc get deployment test-app -n ${TEMP_PROJECT} -o yaml | head -50 || true"

run_test "Scale para 2 réplicas" \
    "oc scale deployment test-app --replicas=2 -n ${TEMP_PROJECT}"

run_test "Verificar scale" \
    "sleep 5 && oc get deployment test-app -n ${TEMP_PROJECT}"

run_test "Scale de volta para 1" \
    "oc scale deployment test-app --replicas=1 -n ${TEMP_PROJECT}"

run_test "Ver ReplicaSets" \
    "oc get rs -n ${TEMP_PROJECT}"

run_test "Status do deployment" \
    "oc rollout status deployment/test-app -n ${TEMP_PROJECT} --timeout=10s 2>/dev/null || echo 'Deployment ainda em progresso'"

run_test "Histórico de rollout" \
    "oc rollout history deployment/test-app -n ${TEMP_PROJECT}"

##############################################################################
# 06 - SERVICES E ROUTES
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "06 - SERVICES E ROUTES"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar services" \
    "oc get svc -n ${TEMP_PROJECT}"

run_test "Descrever service" \
    "oc describe svc test-app -n ${TEMP_PROJECT}"

run_test "Ver service em YAML" \
    "oc get svc test-app -n ${TEMP_PROJECT} -o yaml | head -30 || true"

run_test "Listar routes" \
    "oc get routes -n ${TEMP_PROJECT}"

run_test "Descrever route" \
    "oc describe route test-app -n ${TEMP_PROJECT}"

run_test "Ver URL da route" \
    "oc get route test-app -n ${TEMP_PROJECT} -o jsonpath='{.spec.host}'"

run_test "Listar endpoints" \
    "oc get endpoints -n ${TEMP_PROJECT}"

##############################################################################
# 07 - CONFIGMAPS E SECRETS
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "07 - CONFIGMAPS E SECRETS"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Criar ConfigMap" \
    "oc create configmap test-config --from-literal=key1=value1 --from-literal=key2=value2 -n ${TEMP_PROJECT}"

run_test "Listar ConfigMaps" \
    "oc get configmap -n ${TEMP_PROJECT}"

run_test "Descrever ConfigMap" \
    "oc describe configmap test-config -n ${TEMP_PROJECT}"

run_test "Ver ConfigMap em YAML" \
    "oc get configmap test-config -n ${TEMP_PROJECT} -o yaml"

run_test "Criar Secret" \
    "oc create secret generic test-secret --from-literal=password=mypassword -n ${TEMP_PROJECT}"

run_test "Listar Secrets" \
    "oc get secrets -n ${TEMP_PROJECT}"

run_test "Descrever Secret" \
    "oc describe secret test-secret -n ${TEMP_PROJECT}"

run_test "Ver chaves do Secret" \
    "oc get secret test-secret -n ${TEMP_PROJECT} -o jsonpath='{.data}'"

##############################################################################
# 08 - STORAGE
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "08 - STORAGE"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar PVs (cluster-wide)" \
    "oc get pv | head -10 || true"

run_test "Listar PVCs" \
    "oc get pvc -n ${TEMP_PROJECT}"

run_test "Listar StorageClasses" \
    "oc get storageclass"

run_test "Descrever StorageClass padrão" \
    "oc get storageclass -o json | jq -r '.items[] | select(.metadata.annotations.\"storageclass.kubernetes.io/is-default-class\"==\"true\") | .metadata.name' | head -1 | xargs -I {} oc describe storageclass {}" "$SKIP_DESTRUCTIVE"

##############################################################################
# 09 - BUILDS E IMAGES
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "09 - BUILDS E IMAGES"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar BuildConfigs" \
    "oc get bc -n ${TEMP_PROJECT}"

run_test "Listar Builds" \
    "oc get builds -n ${TEMP_PROJECT}"

run_test "Listar ImageStreams" \
    "oc get is -n ${TEMP_PROJECT}"

run_test "Listar ImageStreams do OpenShift" \
    "oc get is -n openshift | head -10 || true"

##############################################################################
# 10 - REGISTRY E IMAGENS
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "10 - REGISTRY E IMAGENS"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Verificar registry interno" \
    "oc get route -n openshift-image-registry 2>/dev/null || echo 'Registry route não exposta'"

run_test "Listar ImageStreams do sistema" \
    "oc get is -n openshift | head -10 || true"

run_test "Ver tags de uma ImageStream" \
    "oc get is -n openshift -o name | head -1 | xargs oc get -n openshift -o jsonpath='{.spec.tags[*].name}' 2>/dev/null || echo 'N/A'"

##############################################################################
# 11 - MONITORAMENTO E LOGS
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "11 - MONITORAMENTO E LOGS"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Ver logs do primeiro pod" \
    "oc get pods -n ${TEMP_PROJECT} -o name | head -1 | xargs oc logs -n ${TEMP_PROJECT} --tail=5"

run_test "Ver eventos" \
    "oc get events -n ${TEMP_PROJECT} --sort-by='.lastTimestamp' | head -10 || true"

run_test "Ver top nodes" \
    "oc adm top nodes 2>/dev/null || echo 'Métricas podem não estar disponíveis'"

run_test "Ver top pods" \
    "oc adm top pods -n ${TEMP_PROJECT} 2>/dev/null || echo 'Métricas podem não estar disponíveis'"

##############################################################################
# 12 - MUST-GATHER
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "12 - MUST-GATHER"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Verificar comando must-gather (sem executar)" \
    "oc adm must-gather --help | head -5 || true"

##############################################################################
# 13 - TROUBLESHOOTING PODS
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "13 - TROUBLESHOOTING PODS"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Ver pods com problemas (todos os namespaces)" \
    "oc get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded | head -10 || true"

run_test "Ver pods em CrashLoopBackOff" \
    "oc get pods -A --field-selector=status.phase=Running | grep -E -i crash || echo 'Nenhum pod em CrashLoopBackOff'"

run_test "Descrever primeiro pod do projeto" \
    "oc get pods -n ${TEMP_PROJECT} -o name | head -1 | xargs oc describe -n ${TEMP_PROJECT}"

##############################################################################
# 14 - TROUBLESHOOTING REDE
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "14 - TROUBLESHOOTING REDE"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar services" \
    "oc get svc -n ${TEMP_PROJECT}"

run_test "Listar endpoints" \
    "oc get endpoints -n ${TEMP_PROJECT}"

run_test "Listar routes" \
    "oc get routes -n ${TEMP_PROJECT}"

run_test "Verificar DNS (pods dns)" \
    "oc get pods -n openshift-dns | head -5 || true"

##############################################################################
# 15 - TROUBLESHOOTING STORAGE
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "15 - TROUBLESHOOTING STORAGE"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar PVCs com status" \
    "oc get pvc -A | head -10 || true"

run_test "PVCs Pending" \
    "oc get pvc -A --field-selector=status.phase=Pending | head -10 || true"

run_test "Listar StorageClasses" \
    "oc get storageclass"

##############################################################################
# 16 - SEGURANÇA E RBAC
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "16 - SEGURANÇA E RBAC"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar roles" \
    "oc get roles -n ${TEMP_PROJECT}"

run_test "Listar rolebindings" \
    "oc get rolebindings -n ${TEMP_PROJECT}"

run_test "Listar clusterroles" \
    "oc get clusterroles | head -10 || true"

run_test "Listar clusterrolebindings" \
    "oc get clusterrolebindings | head -10 || true"

run_test "Verificar permissões (can-i)" \
    "oc auth can-i create pods -n ${TEMP_PROJECT}"

run_test "Listar o que posso fazer" \
    "oc auth can-i --list -n ${TEMP_PROJECT} | head -20 || true"

run_test "Listar SCCs" \
    "oc get scc"

run_test "Listar service accounts" \
    "oc get sa -n ${TEMP_PROJECT}"

##############################################################################
# 17 - CLUSTER OPERATORS
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "17 - CLUSTER OPERATORS"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar Cluster Operators" \
    "oc get co"

run_test "Cluster Operators degraded" \
    "oc get co --no-headers | awk '{if (\$3 != \"False\" || \$4 != \"False\" || \$5 != \"True\") print \$0}'"

run_test "Descrever primeiro CO" \
    "oc get co -o name | head -1 | xargs oc describe"

##############################################################################
# 18 - NODES E MACHINE
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "18 - NODES E MACHINE"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar nodes" \
    "oc get nodes"

run_test "Listar nodes com detalhes" \
    "oc get nodes -o wide"

run_test "Descrever primeiro node" \
    "oc get nodes -o name | head -1 | xargs oc describe"

run_test "Listar machines" \
    "oc get machines -n openshift-machine-api"

run_test "Listar machinesets" \
    "oc get machinesets -n openshift-machine-api"

##############################################################################
# 19 - CERTIFICADOS E CSR
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "19 - CERTIFICADOS E CSR"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar CSRs" \
    "oc get csr | head -10 || true"

run_test "CSRs Pending" \
    "oc get csr | grep -E Pending || echo 'Nenhum CSR pendente'"

##############################################################################
# 20 - CLUSTER NETWORKING
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "20 - CLUSTER NETWORKING"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Ver configuração de rede do cluster" \
    "oc get network.config.openshift.io cluster -o yaml | head -30 || true"

run_test "Listar Network Policies" \
    "oc get networkpolicy -n ${TEMP_PROJECT}"

run_test "Listar Ingress Controllers" \
    "oc get ingresscontroller -n openshift-ingress-operator"

##############################################################################
# 21 - CLUSTER VERSION E UPDATES
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "21 - CLUSTER VERSION E UPDATES"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Ver versão do cluster" \
    "oc get clusterversion"

run_test "Descrever ClusterVersion" \
    "oc describe clusterversion version"

run_test "Ver histórico de updates" \
    "oc get clusterversion version -o jsonpath='{.status.history}' | head -200 || true"

##############################################################################
# 22 - ETCD BACKUP
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "22 - ETCD BACKUP"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Verificar pods do etcd" \
    "oc get pods -n openshift-etcd | grep -E etcd"

run_test "Ver membros do etcd" \
    "oc get etcd -o=jsonpath='{range .items[0].status.conditions[?(@.type==\"EtcdMembersAvailable\")]}{.message}{end}' 2>/dev/null || echo 'Info de membros não disponível'"

##############################################################################
# 23 - COMANDOS CUSTOMIZADOS
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "23 - COMANDOS CUSTOMIZADOS (awk/jq)"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar pods com uso de recursos customizado" \
    "oc get pods -n ${TEMP_PROJECT} -o json | jq -r '.items[] | .metadata.name' | head -5 || true"

run_test "Contar pods por status" \
    "oc get pods -A --no-headers | awk '{print \$4}' | sort | uniq -c"

run_test "Extrair imagens dos pods" \
    "oc get pods -n ${TEMP_PROJECT} -o json | jq -r '.items[].spec.containers[].image' | head -5 || true"

##############################################################################
# 24 - FIELD SELECTORS
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "24 - FIELD SELECTORS"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Pods Running" \
    "oc get pods -n ${TEMP_PROJECT} --field-selector=status.phase=Running 2>/dev/null || echo 'Pods ainda não estão Running'"

run_test "Pods não Succeeded" \
    "oc get pods -A --field-selector=status.phase!=Succeeded | head -10 || true"

##############################################################################
# 25 - OUTPUT E FORMATAÇÃO
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "25 - OUTPUT E FORMATAÇÃO"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Output em JSON" \
    "oc get pods -n ${TEMP_PROJECT} -o json | head -50 || true"

run_test "Output em YAML" \
    "oc get pods -n ${TEMP_PROJECT} -o yaml | head -50 || true"

run_test "Output com JSONPath" \
    "oc get pods -n ${TEMP_PROJECT} -o jsonpath='{.items[*].metadata.name}'"

run_test "Custom columns" \
    "oc get pods -n ${TEMP_PROJECT} -o custom-columns=NAME:.metadata.name,STATUS:.status.phase"

##############################################################################
# 26 - TEMPLATES E MANIFESTS
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "26 - TEMPLATES E MANIFESTS"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar templates" \
    "oc get templates -n openshift | head -10 || true"

run_test "Exportar deployment como YAML" \
    "oc get deployment test-app -n ${TEMP_PROJECT} -o yaml | head -30 || true"

##############################################################################
# 27 - BACKUP E DISASTER RECOVERY
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "27 - BACKUP E DISASTER RECOVERY"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Exportar recursos do projeto" \
    "oc get all -n ${TEMP_PROJECT} -o yaml | head -50 || true"

##############################################################################
# 28 - PATCH E EDIT
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "28 - PATCH E EDIT"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Patch deployment (adicionar annotation)" \
    "oc patch deployment test-app -n ${TEMP_PROJECT} -p '{\"metadata\":{\"annotations\":{\"test\":\"validated\"}}}'"

run_test "Verificar annotation" \
    "oc get deployment test-app -n ${TEMP_PROJECT} -o jsonpath='{.metadata.annotations.test}'"

##############################################################################
# 29 - JOBS E CRONJOBS
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "29 - JOBS E CRONJOBS"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run_test "Listar Jobs" \
    "oc get jobs -n ${TEMP_PROJECT}"

run_test "Listar CronJobs" \
    "oc get cronjobs -n ${TEMP_PROJECT}"

run_test "Criar Job de teste" \
    "oc create job test-job --image=busybox -n ${TEMP_PROJECT} -- echo 'Hello from test job'"

run_test "Verificar Job criado" \
    "sleep 3 && oc get jobs -n ${TEMP_PROJECT}"

run_test "Ver logs do Job" \
    "sleep 5 && oc logs job/test-job -n ${TEMP_PROJECT}"

##############################################################################
# 30 - OPERATORS E OPERANDOS
##############################################################################
log_info ""
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "30 - OPERATORS E OPERANDOS"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

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

##############################################################################
# RELATÓRIO FINAL
##############################################################################
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    RELATÓRIO DE VALIDAÇÃO                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
log_info "Finalizado em $(date)"
echo ""
echo "Total de testes: $TOTAL_TESTS"
echo -e "${GREEN}Passou: $PASSED_TESTS${NC}"
echo -e "${RED}Falhou: $FAILED_TESTS${NC}"
echo -e "${YELLOW}Pulado: $SKIPPED_TESTS${NC}"
echo ""
echo "Taxa de sucesso: $(awk "BEGIN {printf \"%.2f\", ($PASSED_TESTS/$TOTAL_TESTS)*100}")%"
echo ""
log_info "Log completo salvo em: $LOG_FILE"
echo ""

# Exit code baseado em falhas
if [ $FAILED_TESTS -gt 0 ]; then
    exit 1
else
    exit 0
fi
