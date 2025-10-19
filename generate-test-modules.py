#!/usr/bin/env python3
"""
Gerador de scripts de teste modulares a partir do test-commands.sh original
"""

import os
import re

# Mapeamento de seções para números e nomes
SECTIONS = {
    "01": ("AUTENTICAÇÃO E CONFIGURAÇÃO", "01-autenticacao-configuracao"),
    "02": ("PROJETOS", "02-projetos"),
    "03": ("APLICAÇÕES", "03-aplicacoes"),
    "04": ("PODS E CONTAINERS", "04-pods-containers"),
    "05": ("DEPLOYMENTS E SCALING", "05-deployments-scaling"),
    "06": ("SERVICES E ROUTES", "06-services-routes"),
    "07": ("CONFIGMAPS E SECRETS", "07-configmaps-secrets"),
    "08": ("STORAGE", "08-storage"),
    "09": ("BUILDS E IMAGES", "09-builds-images"),
    "10": ("REGISTRY E IMAGENS", "10-registry-imagens"),
    "11": ("MONITORAMENTO E LOGS", "11-monitoramento-logs"),
    "12": ("MUST-GATHER", "12-must-gather"),
    "13": ("TROUBLESHOOTING PODS", "13-troubleshooting-pods"),
    "14": ("TROUBLESHOOTING REDE", "14-troubleshooting-rede"),
    "15": ("TROUBLESHOOTING STORAGE", "15-troubleshooting-storage"),
    "16": ("SEGURANÇA E RBAC", "16-seguranca-rbac"),
    "17": ("CLUSTER OPERATORS", "17-cluster-operators"),
    "18": ("NODES E MACHINE", "18-nodes-machine"),
    "19": ("CERTIFICADOS E CSR", "19-certificados-csr"),
    "20": ("CLUSTER NETWORKING", "20-cluster-networking"),
    "21": ("CLUSTER VERSION E UPDATES", "21-cluster-version-updates"),
    "22": ("ETCD BACKUP", "22-etcd-backup"),
    "23": ("COMANDOS CUSTOMIZADOS (awk/jq)", "23-comandos-customizados"),
    "24": ("FIELD SELECTORS", "24-field-selectors"),
    "25": ("OUTPUT E FORMATAÇÃO", "25-output-formatacao"),
    "26": ("TEMPLATES E MANIFESTS", "26-templates-manifests"),
    "27": ("BACKUP E DISASTER RECOVERY", "27-backup-disaster-recovery"),
    "28": ("PATCH E EDIT", "28-patch-edit"),
    "29": ("JOBS E CRONJOBS", "29-jobs-cronjobs"),
    "30": ("OPERATORS E OPERANDOS", "30-operators-operandos"),
}

def parse_old_script(filepath):
    """Parse o script antigo e extrai os testes por seção"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    sections_tests = {}
    current_section = None
    current_tests = []
    
    lines = content.split('\n')
    in_test = False
    test_desc = ""
    test_cmd = ""
    test_skip = ""
    
    for line in lines:
        # Detectar header de seção
        if '# ' in line and '-' in line and any(section[0] in line for section in SECTIONS.values()):
            # Salvar seção anterior
            if current_section and current_tests:
                sections_tests[current_section] = current_tests
            
            # Nova seção
            for num, (title, dirname) in SECTIONS.items():
                if title in line:
                    current_section = num
                    current_tests = []
                    break
        
        # Detectar run_test
        if line.strip().startswith('run_test'):
            in_test = True
            # Extrair descrição
            match = re.search(r'run_test "([^"]+)"', line)
            if match:
                test_desc = match.group(1)
        elif in_test and '"' in line and '\\' not in line:
            # Extrair comando
            match = re.search(r'"([^"]+)"', line)
            if match:
                test_cmd = match.group(1)
                # Verificar se tem skip parameter
                match_skip = re.search(r'"([^"]+)"\s+\$', line)
                test_skip = "1" if match_skip else "0"
                
                if current_section:
                    current_tests.append({
                        'description': test_desc,
                        'command': test_cmd,
                        'skip': test_skip
                    })
                
                in_test = False
                test_desc = ""
                test_cmd = ""
    
    # Salvar última seção
    if current_section and current_tests:
        sections_tests[current_section] = current_tests
    
    return sections_tests

def generate_test_script(section_num, tests):
    """Gera um script de teste para uma seção"""
    title, dirname = SECTIONS[section_num]
    
    script = f"""#!/bin/bash

##############################################################################
# Teste: {section_num} - {title}
##############################################################################

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
source "${{SCRIPT_DIR}}/../lib/common.sh"

section_header "{section_num} - {title}"

"""
    
    for test in tests:
        skip_param = f" {test['skip']}" if test['skip'] == "1" else ""
        script += f'''run_test "{test['description']}" \\
    "{test['command']}"{skip_param}

'''
    
    return script

def main():
    # Ler script antigo
    old_script_path = 'test-commands.sh'
    if not os.path.exists(old_script_path):
        print(f"Erro: {old_script_path} não encontrado")
        return
    
    print("Parseando script antigo...")
    sections_tests = parse_old_script(old_script_path)
    
    print(f"Encontradas {len(sections_tests)} seções")
    
    # Gerar scripts individuais
    tests_dir = 'tests'
    for section_num, tests in sections_tests.items():
        if section_num not in SECTIONS:
            continue
        
        title, dirname = SECTIONS[section_num]
        section_dir = os.path.join(tests_dir, dirname)
        
        if not os.path.exists(section_dir):
            print(f"Aviso: Diretório {section_dir} não existe, criando...")
            os.makedirs(section_dir, exist_ok=True)
        
        script_content = generate_test_script(section_num, tests)
        script_path = os.path.join(section_dir, 'test.sh')
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        os.chmod(script_path, 0o755)
        print(f"✓ Criado: {script_path} ({len(tests)} testes)")
    
    print("\n✓ Geração concluída!")

if __name__ == '__main__':
    main()
