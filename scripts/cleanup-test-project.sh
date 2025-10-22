#!/bin/bash

##############################################################################
# Script de Limpeza Manual de Projeto de Teste
# Remove o projeto de teste persistente e limpa arquivos de estado
##############################################################################

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_STATE_FILE="/tmp/oc-test-project-state"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Limpeza de Projeto de Teste OpenShift                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar se existe arquivo de estado
if [ ! -f "$PROJECT_STATE_FILE" ]; then
    echo -e "${YELLOW}[⚠]${NC} Nenhum projeto de teste encontrado em $PROJECT_STATE_FILE"
    echo ""
    echo "Procurando projetos de teste manualmente..."
    
    # Listar projetos com label test-validation
    test_projects=$(oc get projects -l test-validation=true -o name  | sed 's|project.project.openshift.io/||')
    
    if [ -z "$test_projects" ]; then
        echo -e "${GREEN}[✓]${NC} Nenhum projeto de teste encontrado no cluster"
        exit 0
    else
        echo -e "${YELLOW}Projetos de teste encontrados:${NC}"
        echo "$test_projects"
        echo ""
        read -p "Deseja deletar estes projetos? (s/N) " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Ss]$ ]]; then
            for project in $test_projects; do
                echo -e "${BLUE}[INFO]${NC} Deletando projeto: $project"
                oc delete project "$project" --wait=false
            done
            echo -e "${GREEN}[✓]${NC} Projetos marcados para deleção"
        else
            echo -e "${YELLOW}[⚠]${NC} Operação cancelada"
        fi
    fi
    exit 0
fi

# Carregar projeto do arquivo de estado
source "$PROJECT_STATE_FILE"

echo -e "${BLUE}[INFO]${NC} Projeto de teste encontrado: ${YELLOW}$TEST_PROJECT${NC}"
echo ""

# Verificar se o projeto existe
if ! oc get project "$TEST_PROJECT" &>/dev/null; then
    echo -e "${YELLOW}[⚠]${NC} Projeto $TEST_PROJECT não existe no cluster"
    echo -e "${BLUE}[INFO]${NC} Removendo apenas arquivo de estado..."
    rm -f "$PROJECT_STATE_FILE"
    echo -e "${GREEN}[✓]${NC} Arquivo de estado removido"
    exit 0
fi

# Mostrar recursos do projeto
echo -e "${BLUE}[INFO]${NC} Recursos no projeto:"
oc get all -n "$TEST_PROJECT"  || echo "  (nenhum recurso)"
echo ""

# Confirmar deleção
read -p "Deseja deletar o projeto $TEST_PROJECT? (s/N) " -n 1 -r
echo

if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo ""
    echo -e "${BLUE}[INFO]${NC} Deletando projeto: $TEST_PROJECT"
    
    if oc delete project "$TEST_PROJECT" --wait=false ; then
        echo -e "${GREEN}[✓]${NC} Projeto marcado para deleção"
    else
        echo -e "${RED}[✗]${NC} Erro ao deletar projeto"
    fi
    
    # Remover arquivo de estado
    rm -f "$PROJECT_STATE_FILE"
    echo -e "${GREEN}[✓]${NC} Arquivo de estado removido: $PROJECT_STATE_FILE"
    
    # Limpar outros arquivos temporários
    rm -f /tmp/oc-test-state-* 
    rm -f /tmp/oc-test-timing-* 
    echo -e "${GREEN}[✓]${NC} Arquivos temporários limpos"
    
    echo ""
    echo -e "${GREEN}[✓]${NC} Limpeza concluída!"
else
    echo ""
    echo -e "${YELLOW}[⚠]${NC} Operação cancelada"
    echo -e "${BLUE}[INFO]${NC} Para forçar limpeza, delete: rm $PROJECT_STATE_FILE"
fi

echo ""
