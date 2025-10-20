#!/bin/bash

##############################################################################
# Biblioteca Comum para Scripts de Teste
# Funções compartilhadas entre todos os scripts de validação
##############################################################################

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Arquivo de projeto compartilhado (persiste entre execuções)
PROJECT_STATE_FILE="/tmp/oc-test-project-state"

# Arquivo de estado compartilhado
STATE_FILE="${STATE_FILE:-/tmp/oc-test-state-$$}"

# Arquivo de log (para execuções standalone)
LOG_FILE="${LOG_FILE:-/tmp/test-module-$(date +%Y%m%d-%H%M%S).log}"

# Variáveis de controle
VERBOSE="${VERBOSE:-0}"
STOP_ON_ERROR="${STOP_ON_ERROR:-0}"

# Inicializar arquivo de estado se não existir
if [ ! -f "$STATE_FILE" ]; then
    echo "TOTAL_TESTS=0" > "$STATE_FILE"
    echo "PASSED_TESTS=0" >> "$STATE_FILE"
    echo "FAILED_TESTS=0" >> "$STATE_FILE"
    echo "SKIPPED_TESTS=0" >> "$STATE_FILE"
fi

# Carregar estado
source "$STATE_FILE"

# Função para salvar estado
save_state() {
    echo "TOTAL_TESTS=$TOTAL_TESTS" > "$STATE_FILE"
    echo "PASSED_TESTS=$PASSED_TESTS" >> "$STATE_FILE"
    echo "FAILED_TESTS=$FAILED_TESTS" >> "$STATE_FILE"
    echo "SKIPPED_TESTS=$SKIPPED_TESTS" >> "$STATE_FILE"
}

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
    save_state
    
    # Verificar se should_skip é um número antes de comparar
    if [[ "$should_skip" =~ ^[0-9]+$ ]] && [ "$should_skip" -eq 1 ]; then
        log_skip "$description"
        SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
        save_state
        echo ""
        return 0
    fi
    
    if [ "$VERBOSE" -eq 1 ]; then
        log_info "Executando: $command"
    fi
    
    echo "# Test $TOTAL_TESTS: $description" >> "$LOG_FILE"
    echo "# Command: $command" >> "$LOG_FILE"
    
    # Capturar saída do comando para exibir em modo verbose
    local output
    local exit_code
    
    if [ "$VERBOSE" -eq 1 ]; then
        # Em modo verbose, captura a saída e exibe com [DEBUG]
        output=$(eval "$command" 2>&1)
        exit_code=$?
        
        # Adiciona ao log
        echo "$output" >> "$LOG_FILE"
        
        if [ $exit_code -eq 0 ]; then
            log_success "$description"
            if [ -n "$output" ]; then
                echo -e "${BLUE}[DEBUG]${NC} Saída do comando:" | tee -a "$LOG_FILE"
                echo "$output" | sed 's/^/  /' | tee -a "$LOG_FILE"
            fi
            PASSED_TESTS=$((PASSED_TESTS + 1))
            save_state
            echo ""
            return 0
        else
            log_error "$description"
            log_error "  Comando: $command"
            if [ -n "$output" ]; then
                echo -e "${BLUE}[DEBUG]${NC} Saída do comando:" | tee -a "$LOG_FILE"
                echo "$output" | sed 's/^/  /' | tee -a "$LOG_FILE"
            fi
            FAILED_TESTS=$((FAILED_TESTS + 1))
            save_state
            
            if [ "$STOP_ON_ERROR" -eq 1 ]; then
                log_error "Parando execução devido ao erro (--stop-on-error)"
                exit 1
            fi
            echo ""
            return 1
        fi
    else
        # Modo normal, apenas registra no log
        if eval "$command" >> "$LOG_FILE" 2>&1; then
            log_success "$description"
            PASSED_TESTS=$((PASSED_TESTS + 1))
            save_state
            echo ""
            return 0
        else
            log_error "$description"
            log_error "  Comando: $command"
            FAILED_TESTS=$((FAILED_TESTS + 1))
            save_state
            
            if [ "$STOP_ON_ERROR" -eq 1 ]; then
                log_error "Parando execução devido ao erro (--stop-on-error)"
                exit 1
            fi
            echo ""
            return 1
        fi
    fi
}

# Função para exibir header de seção
section_header() {
    local section_name="$1"
    echo ""
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "$section_name"
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Função para obter ou criar projeto de teste
get_test_project() {
    # Se TEST_PROJECT já está definido (vindo do script principal), usar ele
    if [ -n "$TEST_PROJECT" ]; then
        # Salvar no arquivo para reutilizar em execuções subsequentes
        echo "TEST_PROJECT=$TEST_PROJECT" > "$PROJECT_STATE_FILE"
        return 0
    fi
    
    # Tentar carregar de arquivo de estado persistente
    if [ -f "$PROJECT_STATE_FILE" ]; then
        source "$PROJECT_STATE_FILE"
        
        # Verificar se o projeto ainda existe
        if oc get project "$TEST_PROJECT" &>/dev/null; then
            echo -e "${BLUE}[INFO]${NC} Reutilizando projeto de teste: $TEST_PROJECT"
            return 0
        else
            echo -e "${YELLOW}[⚠]${NC} Projeto $TEST_PROJECT não existe mais, criando novo..."
            rm -f "$PROJECT_STATE_FILE"
        fi
    fi
    
    # Criar novo projeto de teste
    local project_name="test-validation-$(date +%s)"
    
    if oc new-project "$project_name" --description="Projeto de teste automático" &>/dev/null || \
       oc project "$project_name" &>/dev/null; then
        
        # Adicionar label para identificação
        oc label namespace "$project_name" test-validation=true &>/dev/null || true
        
        TEST_PROJECT="$project_name"
        echo "TEST_PROJECT=$TEST_PROJECT" > "$PROJECT_STATE_FILE"
        echo -e "${GREEN}[✓]${NC} Projeto de teste criado: $TEST_PROJECT"
        return 0
    else
        echo -e "${RED}[✗]${NC} Falha ao criar projeto de teste"
        return 1
    fi
}

# Inicializar projeto de teste
get_test_project

# Exportar variáveis e funções para subshells
export STATE_FILE
export TEST_PROJECT
export PROJECT_STATE_FILE
export LOG_FILE
export VERBOSE
export STOP_ON_ERROR
export -f log_info log_success log_warning log_error log_skip run_test section_header save_state get_test_project
export RED GREEN YELLOW BLUE NC
