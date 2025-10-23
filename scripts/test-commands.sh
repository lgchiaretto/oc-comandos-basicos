#!/bin/bash

##############################################################################
# Script Principal de Validação de Comandos OpenShift
# Executa todos os módulos de teste organizados por tópico
#
# Uso: ./scripts/test-commands.sh [OPÇÕES]
#
# Opções:
#   --verbose              Mostra saída detalhada de cada comando
#   --stop-on-error        Para execução no primeiro erro
#   --skip-destructive     Pula comandos destrutivos (padrão)
#   --allow-destructive    Permite comandos destrutivos
#   --cleanup              Executa limpeza após os testes
#   --module <num>         Executa apenas o módulo especificado (ex: --module 01)
#   --start-module <num>   Inicia a partir do módulo especificado (ex: --start-module 10)
#   --end-module <num>     Termina no módulo especificado (ex: --end-module 15)
#
# Exemplos:
#   ./scripts/test-commands.sh                              # Executa todos os módulos
#   ./scripts/test-commands.sh --module 05                  # Executa apenas módulo 05
#   ./scripts/test-commands.sh --start-module 10            # Executa do 10 ao 30
#   ./scripts/test-commands.sh --start-module 01 --end-module 05  # Executa 01 a 05
#   ./scripts/test-commands.sh --start-module 06 --end-module 08  # Executa 06 a 08
#   ./scripts/test-commands.sh --start-module 08 --end-module 30  # Executa 08 a 30
##############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
source "${REPO_ROOT}/lib/common.sh"

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
CLEANUP=0      # Default: Do not cleanup
SPECIFIC_MODULE=""
START_MODULE=""
END_MODULE=""
STATE_FILE="/tmp/oc-test-state-$$"
LOG_FILE="/tmp/test-commands-$(date +%Y%m%d-%H%M%S).log"
TIMING_FILE="/tmp/oc-test-timing-$$"

# Inicializar arquivo de estado
echo "TOTAL_TESTS=0" > "$STATE_FILE"
echo "PASSED_TESTS=0" >> "$STATE_FILE"
echo "FAILED_TESTS=0" >> "$STATE_FILE"

# Inicializar arquivo de timing
echo "# Tempo de execução dos módulos" > "$TIMING_FILE"

# Tempo de início total
SCRIPT_START_TIME=$(date +%s)

# Parse argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose)
            VERBOSE=1
            shift
            ;;
        --stop-on-error)
            STOP_ON_ERROR=1
            shift
            ;;
        --skip-destructive)
            SKIP_DESTRUCTIVE=1
            shift
            ;;
        --allow-destructive)
            SKIP_DESTRUCTIVE=0
            shift
            ;;
        --cleanup)
            CLEANUP=1
            shift
            ;;
        --module)
            SPECIFIC_MODULE="$2"
            shift 2
            ;;
        --start-module)
            START_MODULE="$2"
            shift 2
            ;;
        --end-module)
            END_MODULE="$2"
            shift 2
            ;;
        --help)
            echo "Uso: $0 [OPÇÕES]"
            echo ""
            echo "Opções:"
            echo "  --verbose              Mostra saída detalhada"
            echo "  --stop-on-error        Para no primeiro erro"
            echo "  --skip-destructive     Pula comandos destrutivos (padrão)"
            echo "  --allow-destructive    Permite comandos destrutivos"
            echo "  --cleanup              Executa a limpeza após os testes (Default: não)"
            echo "  --module <num>         Executa apenas módulo específico (ex: 01)"
            echo "  --start-module <num>   Inicia a partir do módulo especificado (ex: 10)"
            echo "  --end-module <num>     Termina no módulo especificado (ex: 15)"
            echo ""
            echo "Exemplos:"
            echo "  $0                                # Executa todos os módulos"
            echo "  $0 --module 05                    # Executa apenas o módulo 05"
            echo "  $0 --start-module 10              # Executa do módulo 10 ao 30"
            echo "  $0 --start-module 01 --end-module 05  # Executa módulos 01 a 05"
            echo "  $0 --start-module 06 --end-module 08  # Executa módulos 06 a 08"
            exit 0
            ;;
        *)
            echo "Opção desconhecida: $1"
            echo "Use --help para ver as opções disponíveis"
            exit 1
            ;;
    esac
done

# Exportar variáveis para os módulos
export VERBOSE
export STOP_ON_ERROR
export SKIP_DESTRUCTIVE
export LOG_FILE
export STATE_FILE
export TIMING_FILE

# Validar combinações de parâmetros
if [ -n "$SPECIFIC_MODULE" ] && { [ -n "$START_MODULE" ] || [ -n "$END_MODULE" ]; }; then
    log_error "Erro: --module não pode ser usado com --start-module ou --end-module"
    exit 1
fi

# Funções de logging (definidas aqui para o script principal)
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1" | tee -a "$LOG_FILE"
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
    if ! oc auth can-i create pods &> /dev/null; then
        echo -e "${YELLOW}[⚠]${NC} Usuário pode não ter permissão para criar projetos. Alguns testes podem falhar." | tee -a "$LOG_FILE"
    fi
    
    log_success "Pré-requisitos verificados"
    echo ""
}

# Função de limpeza
cleanup() {
    # Verificar se deve pular a limpeza
    if [ "$CLEANUP" -eq 0 ]; then
        log_info "Limpeza pulada (--cleanup desativado)"
        return 0
    fi    
    log_info "Executando limpeza..."
    
    # Remover arquivos de estado
    rm -f "$STATE_FILE"
    
    log_success "Limpeza concluída"
}

# Trap para garantir limpeza
trap cleanup EXIT

# Função para executar um módulo de teste
run_test_module() {
    local module_dir="$1"
    local test_script="${module_dir}/test.sh"
    local module_name=$(basename "$module_dir")
    
    if [ ! -f "$test_script" ]; then
        echo -e "${YELLOW}[⚠]${NC} Script de teste não encontrado: $test_script" | tee -a "$LOG_FILE"
        return 1
    fi
    
    # Tornar o script executável
    chmod +x "$test_script"
    
    # Registrar tempo de início do módulo
    local module_start=$(date +%s)
    
    # Executar o módulo
    bash "$test_script"
    local exit_code=$?
    
    # Calcular tempo de execução
    local module_end=$(date +%s)
    local module_duration=$((module_end - module_start))
    
    # Registrar tempo no arquivo
    echo "$module_name:$module_duration" >> "$TIMING_FILE"
    
    # Capturar variáveis atualizadas (o módulo as exporta)
    return $exit_code
}

# Banner inicial
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     Script de Validação de Comandos OpenShift                  ║"
echo "║     Testando comandos da documentação (modular)                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
log_info "Iniciando validação em $(date)"
log_info "Cluster: $(oc whoami --show-server)"
log_info "Usuário: $(oc whoami)"
log_info "Log: $LOG_FILE"
echo ""

# Verificar pré-requisitos
check_prerequisites

# Diretório de testes (relativo à raiz do repositório)
TESTS_DIR="${REPO_ROOT}/tests"

if [ ! -d "$TESTS_DIR" ]; then
    log_error "Diretório de testes não encontrado: $TESTS_DIR"
    exit 1
fi

# Função para filtrar módulos por range
filter_modules() {
    local all_modules=("$@")
    local filtered=()
    
    for module_dir in "${all_modules[@]}"; do
        local module_num=$(basename "$module_dir" | cut -d'-' -f1)
        
        # Remover zeros à esquerda para comparação numérica
        module_num=$((10#$module_num))
        
        # Aplicar filtro de início
        if [ -n "$START_MODULE" ]; then
            local start_num=$((10#$START_MODULE))
            if [ $module_num -lt $start_num ]; then
                continue
            fi
        fi
        
        # Aplicar filtro de fim
        if [ -n "$END_MODULE" ]; then
            local end_num=$((10#$END_MODULE))
            if [ $module_num -gt $end_num ]; then
                continue
            fi
        fi
        
        filtered+=("$module_dir")
    done
    
    echo "${filtered[@]}"
}

# Lista de módulos
if [ -n "$SPECIFIC_MODULE" ]; then
    # Executar apenas módulo específico
    modules=("${TESTS_DIR}/${SPECIFIC_MODULE}-"*)
else
    # Executar todos os módulos em ordem
    all_modules=($(find "$TESTS_DIR" -maxdepth 1 -type d -name '[0-9][0-9]-*' | sort))
    
    # Aplicar filtros de range se especificados
    if [ -n "$START_MODULE" ] || [ -n "$END_MODULE" ]; then
        modules=($(filter_modules "${all_modules[@]}"))
    else
        modules=("${all_modules[@]}")
    fi
fi

# Verificar se há módulos para executar
if [ ${#modules[@]} -eq 0 ]; then
    log_error "Nenhum módulo encontrado com os critérios especificados"
    exit 1
fi

# Mostrar informações sobre os módulos que serão executados
log_info "Módulos a serem executados: ${#modules[@]}"
if [ -n "$START_MODULE" ] || [ -n "$END_MODULE" ]; then
    range_info="Range: "
    [ -n "$START_MODULE" ] && range_info+="início=${START_MODULE} "
    [ -n "$END_MODULE" ] && range_info+="fim=${END_MODULE}"
    log_info "$range_info"
fi
echo ""

# Executar cada módulo
for module_dir in "${modules[@]}"; do
    if [ -d "$module_dir" ]; then
        run_test_module "$module_dir"
    fi
done

##############################################################################
# RELATÓRIO FINAL
##############################################################################

# Carregar estado final
source "$STATE_FILE"

# Calcular tempo total de execução
SCRIPT_END_TIME=$(date +%s)
TOTAL_DURATION=$((SCRIPT_END_TIME - SCRIPT_START_TIME))

# Função para formatar tempo
format_time() {
    local seconds=$1
    local hours=$((seconds / 3600))
    local minutes=$(( (seconds % 3600) / 60 ))
    local secs=$((seconds % 60))
    
    if [ $hours -gt 0 ]; then
        echo "${hours}h ${minutes}m ${secs}s"
    elif [ $minutes -gt 0 ]; then
        echo "${minutes}m ${secs}s"
    else
        echo "${secs}s"
    fi
}

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
echo ""

if [ "$TOTAL_TESTS" -gt 0 ]; then
    success_rate=$(awk "BEGIN {printf \"%.2f\", ($PASSED_TESTS/$TOTAL_TESTS)*100}")
    echo "Taxa de sucesso: ${success_rate}%"
else
    echo "Nenhum teste executado"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║               TEMPO DE EXECUÇÃO POR MÓDULO                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Exibir tempo de cada módulo
if [ -f "$TIMING_FILE" ]; then
    printf "%-40s %15s\n" "Módulo" "Tempo"
    echo "────────────────────────────────────────────────────────────────"
    
    while IFS=: read -r module_name duration; do
        if [[ ! "$module_name" =~ ^# ]]; then
            formatted_time=$(format_time "$duration")
            printf "%-40s %15s\n" "$module_name" "$formatted_time"
        fi
    done < "$TIMING_FILE"
    
    echo "────────────────────────────────────────────────────────────────"
    formatted_total=$(format_time "$TOTAL_DURATION")
    printf "%-40s %15s\n" "TEMPO TOTAL" "$formatted_total"
    
    # Limpar arquivo de timing
    rm -f "$TIMING_FILE"
fi

echo ""
log_info "Log completo salvo em: $LOG_FILE"
echo ""

# Exit code baseado em falhas
if [ $FAILED_TESTS -gt 0 ]; then
    exit 1
else
    exit 0
fi
