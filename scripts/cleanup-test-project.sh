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

echo -e "${BLUE}╔═════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Limpeza de Projeto de Teste OpenShift       ║${NC}"
echo -e "${BLUE}╚═════════════════════════════════════════════════╝${NC}"
echo ""

echo "Procurando projetos de teste..."

# Listar projetos com label test-validation
test_projects=$(oc get projects -l test-validation=true -o name  | sed 's|project.project.openshift.io/||')

if [ -z "$test_projects" ]; then
    echo -e "${GREEN}[✓]${NC} Nenhum projeto de teste encontrado no cluster"
    exit 0
else
    echo -e "${YELLOW}Projetos de teste encontrados:${NC}"
    echo "$test_projects"
    for project in $test_projects; do
        echo -e "${BLUE}[INFO]${NC} Deletando projeto: $project"
        oc delete project "$project" --wait=false
    done
    echo -e "${GREEN}[✓]${NC} Projetos marcados para deleção"
fi
exit 0
echo ""
