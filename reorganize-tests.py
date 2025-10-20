#!/usr/bin/env python3
"""
Script para reorganizar testes para que sigam a mesma ordem dos comandos nos markdowns.
Preserva exatamente a formatação original dos blocos run_test.

Uso: python3 reorganize-tests.py
"""

import os
import re
from pathlib import Path
from typing import List, Tuple
import subprocess

# Diretório base
BASE_DIR = Path(__file__).parent
TESTS_DIR = BASE_DIR / "tests"


def extract_commands_from_markdown(md_file: Path) -> List[str]:
    """
    Extrai comandos oc (não comentados) de um arquivo markdown na ordem em que aparecem.
    Retorna uma lista de comandos principais (primeira palavra após 'oc').
    """
    commands = []
    in_code_block = False
    
    with open(md_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Detectar início/fim de blocos de código bash
            if line.strip().startswith('```bash'):
                in_code_block = True
                continue
            elif line.strip().startswith('```'):
                in_code_block = False
                continue
            
            # Processar apenas linhas dentro de blocos bash
            if in_code_block and not line.strip().startswith('#'):
                # Buscar comandos oc
                match = re.search(r'^oc\s+(\S+)', line.strip())
                if match:
                    cmd = match.group(1)
                    commands.append(cmd)
    
    return commands


def extract_tests_from_script(test_file: Path) -> List[Tuple[str, str, str, int]]:
    """
    Extrai testes de um script test.sh preservando o bloco original completo.
    Retorna lista de tuplas (descrição, comando, bloco_completo_original, linha_início).
    """
    tests = []
    
    with open(test_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Procura por run_test no início da linha (sem indentação ou com espaços)
        if re.match(r'^\s*run_test\s+', line):
            start_line = i
            # Captura o bloco completo (pode ter múltiplas linhas)
            block_lines = [line]
            
            # Se a linha termina com \, continua capturando linhas
            current_line = i
            while current_line < len(lines) - 1:
                if lines[current_line].rstrip().endswith('\\'):
                    current_line += 1
                    block_lines.append(lines[current_line])
                else:
                    break
            
            # Avança o índice
            i = current_line
            
            # Junta o bloco preservando exatamente a formatação original
            full_block = ''.join(block_lines)
            
            # Tenta extrair a descrição (primeiro parâmetro entre aspas)
            desc_match = re.search(r'run_test\s+"([^"]+)"', full_block)
            if not desc_match:
                desc_match = re.search(r"run_test\s+'([^']+)'", full_block)
            
            # Tenta extrair o comando (geralmente após \ e ")
            # Busca o texto após a primeira quebra de linha e aspas
            cmd_match = re.search(r'run_test\s+["\'][^"\']+["\']\s+\\\s+["\'](.+?)["\']', full_block, re.DOTALL)
            
            if desc_match:
                description = desc_match.group(1)
                command = cmd_match.group(1) if cmd_match else ""
                tests.append((description, command, full_block, start_line))
        
        i += 1
    
    return tests


def extract_command_keyword(command: str) -> str:
    """
    Extrai a palavra-chave principal de um comando (ex: 'get', 'whoami', 'create').
    """
    # Remove prefixos comuns e pega a primeira palavra significativa
    cmd = command.strip()
    
    # Remove pipes e pega só a primeira parte
    cmd = cmd.split('|')[0].strip()
    cmd = cmd.split('&&')[0].strip()
    cmd = cmd.split(';')[0].strip()
    cmd = cmd.split('2>')[0].strip()
    
    # Extrai o primeiro comando oc
    match = re.search(r'oc\s+([a-z\-]+)', cmd)
    if match:
        return match.group(1)
    
    return ""


def calculate_command_order_score(test_cmd: str, md_commands: List[str]) -> int:
    """
    Calcula um score de ordem baseado na primeira ocorrência do comando no markdown.
    Retorna o índice da primeira ocorrência (menor = aparece antes).
    """
    keyword = extract_command_keyword(test_cmd)
    
    if not keyword:
        return 999999  # Coloca no final se não conseguir extrair
    
    # Procura a primeira ocorrência desse comando no markdown
    for idx, md_cmd in enumerate(md_commands):
        if keyword == md_cmd or keyword in md_cmd:
            return idx
    
    return 999999  # Se não encontrar, coloca no final


def reorganize_test_script(test_file: Path, md_file: Path) -> str:
    """
    Reorganiza um script de teste para seguir a ordem do markdown.
    Preserva exatamente a formatação original.
    """
    # Ler o script original
    with open(test_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Encontrar a primeira linha com run_test
    first_test_line = None
    for i, line in enumerate(lines):
        if re.match(r'^\s*run_test\s+', line):
            first_test_line = i
            break
    
    if first_test_line is None:
        # Nenhum teste encontrado, retornar original
        return ''.join(lines)
    
    # Extrair cabeçalho (tudo antes do primeiro run_test)
    header = ''.join(lines[:first_test_line])
    
    # Extrair comandos do markdown
    md_commands = extract_commands_from_markdown(md_file)
    
    # Extrair testes
    tests = extract_tests_from_script(test_file)
    
    # Calcular scores de ordem para cada teste
    tests_with_scores = []
    for desc, cmd, block, line_num in tests:
        score = calculate_command_order_score(cmd, md_commands)
        tests_with_scores.append((score, line_num, desc, cmd, block))
    
    # Ordenar por score (menor score = aparece antes no markdown)
    # Em caso de empate, mantém a ordem original (line_num)
    tests_with_scores.sort(key=lambda x: (x[0], x[1]))
    
    # Reconstruir o script
    new_content = header
    
    for score, line_num, desc, cmd, block in tests_with_scores:
        new_content += block
        # Adiciona newline se o bloco não terminar com um
        if not block.endswith('\n'):
            new_content += '\n'
    
    return new_content


def main():
    """Processa todos os módulos de teste."""
    
    print("🔄 Reorganizando scripts de teste para seguir ordem dos markdowns...\n")
    
    # Lista de módulos (01-30)
    modules = []
    for i in range(1, 31):
        module_num = f"{i:02d}"
        
        # Encontrar arquivo markdown correspondente
        md_files = list(BASE_DIR.glob(f"{module_num}-*.md"))
        if not md_files:
            print(f"⚠️  Módulo {module_num}: markdown não encontrado")
            continue
        
        md_file = md_files[0]
        test_dir = TESTS_DIR / md_file.stem
        test_file = test_dir / "test.sh"
        
        if not test_file.exists():
            print(f"⚠️  Módulo {module_num}: test.sh não encontrado em {test_dir}")
            continue
        
        modules.append((module_num, md_file, test_file))
    
    # Processar cada módulo
    success_count = 0
    for module_num, md_file, test_file in modules:
        try:
            print(f"📝 Processando módulo {module_num}: {md_file.stem}...")
            
            # Reorganizar
            new_content = reorganize_test_script(test_file, md_file)
            
            # Fazer backup se ainda não existir
            backup_file = test_file.with_suffix('.sh.bak2')
            if not backup_file.exists():
                with open(test_file, 'r') as f:
                    backup_content = f.read()
                with open(backup_file, 'w') as f:
                    f.write(backup_content)
            
            # Escrever novo conteúdo
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Manter permissões de execução
            os.chmod(test_file, 0o755)
            
            print(f"   ✅ Reorganizado (backup: {backup_file.name})")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n✨ Concluído! {success_count}/{len(modules)} módulos reorganizados.")
    print("\n💡 Dica: Execute './test-commands.sh' para validar as mudanças")
    print("💡 Os backups (.sh.bak2) podem ser removidos se tudo estiver OK")


if __name__ == "__main__":
    main()
