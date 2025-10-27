#!/usr/bin/env python3
"""
Script para transformar blocos bash nos markdowns:
- Extrair comentários dos blocos bash
- Criar blocos markdown com as explicações
- Deixar apenas comandos puros nos blocos bash
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

def extract_command_info(bash_block: str) -> Tuple[List[str], List[str]]:
    """
    Extrai informações e comandos de um bloco bash.
    Retorna (linhas_de_explicacao, comandos_puros)
    """
    lines = bash_block.split('\n')
    explanations = []
    commands = []
    current_explanation = []
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Se é uma linha vazia, mantém nos comandos se necessário
        if not line:
            if commands or current_explanation:
                commands.append('')
            i += 1
            continue
        
        # Se é um comentário
        if line.strip().startswith('#'):
            comment_text = line.strip()[1:].strip()
            current_explanation.append(comment_text)
            i += 1
            continue
        
        # Se é um comando
        if line.strip() and not line.strip().startswith('#'):
            # Se temos explicações acumuladas, processa elas
            if current_explanation:
                # Procura por padrões especiais nos comentários
                full_explanation = ' '.join(current_explanation)
                
                # Detecta se é uma ação principal
                if len(current_explanation) == 1 and not any(c in current_explanation[0] for c in [':', '-', '*']):
                    explanations.append(f"**Ação:** {current_explanation[0]}")
                # Detecta se já tem formatação de lista
                elif any(item.strip().startswith('-') or item.strip().startswith('*') for item in current_explanation):
                    explanations.extend([f"* {item.strip().lstrip('*-').strip()}" if not item.strip().startswith(('*', '-')) else item for item in current_explanation])
                # Detecta padrão de flag: descrição
                elif ':' in full_explanation and len(current_explanation) == 1:
                    explanations.append(f"* {current_explanation[0]}")
                # Caso de múltiplas linhas de explicação
                else:
                    # Primeira linha como ação
                    if current_explanation:
                        explanations.append(f"**Ação:** {current_explanation[0]}")
                        # Demais linhas como detalhes
                        for detail in current_explanation[1:]:
                            if detail.strip():
                                explanations.append(f"* {detail}")
                
                current_explanation = []
            
            # Adiciona o comando e todas as suas continuações
            command_lines = [line]
            i += 1
            
            # Captura continuações de comando (linhas que terminam com \ ou fazem parte de here-doc)
            in_heredoc = False
            heredoc_delimiter = None
            
            # Detecta here-doc
            if '<<' in line:
                match = re.search(r'<<\s*["\']?(\w+)["\']?', line)
                if match:
                    in_heredoc = True
                    heredoc_delimiter = match.group(1)
            
            while i < len(lines):
                next_line = lines[i].rstrip()
                
                # Se estamos em here-doc
                if in_heredoc:
                    command_lines.append(next_line)
                    if next_line.strip() == heredoc_delimiter:
                        in_heredoc = False
                    i += 1
                    continue
                
                # Se linha anterior termina com \
                if command_lines[-1].rstrip().endswith('\\'):
                    command_lines.append(next_line)
                    i += 1
                    continue
                
                # Se próxima linha é continuação de pipe ou lógica
                if next_line.strip() and next_line.strip()[0] in '|&':
                    command_lines.append(next_line)
                    i += 1
                    continue
                
                # Se próxima linha é indentada (continuação de comando multi-linha)
                if next_line and next_line[0] in ' \t' and command_lines[-1].strip():
                    # Mas não é um novo comando
                    if not next_line.strip().startswith('#'):
                        command_lines.append(next_line)
                        i += 1
                        continue
                
                break
            
            commands.append('\n'.join(command_lines))
            continue
        
        i += 1
    
    # Se sobrou explicação sem comando, adiciona também
    if current_explanation:
        explanations.extend([f"* {item}" for item in current_explanation])
    
    return explanations, commands

def transform_bash_block(bash_content: str, ignore_test: bool) -> str:
    """
    Transforma um bloco bash extraindo comentários para markdown.
    """
    explanations, commands = extract_command_info(bash_content)
    
    # Se não há comandos, retorna o bloco original
    if not commands or all(not cmd.strip() for cmd in commands):
        return f"```bash{' ignore-test' if ignore_test else ''}\n{bash_content}\n```"
    
    result = []
    
    # Se há explicações, cria bloco markdown
    if explanations:
        result.append("```markdown")
        result.extend(explanations)
        result.append("```")
        result.append("")
    
    # Cria bloco bash com apenas os comandos
    result.append(f"```bash{' ignore-test' if ignore_test else ''}")
    
    # Filtra comandos vazios do início e fim
    clean_commands = []
    for cmd in commands:
        if cmd.strip() or clean_commands:  # Mantém vazias no meio
            clean_commands.append(cmd)
    
    # Remove vazias do final
    while clean_commands and not clean_commands[-1].strip():
        clean_commands.pop()
    
    result.append('\n'.join(clean_commands))
    result.append("```")
    
    return '\n'.join(result)

def process_markdown_file(file_path: Path) -> str:
    """
    Processa um arquivo markdown completo.
    """
    content = file_path.read_text(encoding='utf-8')
    
    # Padrão para encontrar blocos bash (com ou sem ignore-test)
    pattern = r'```bash( ignore-test)?\n(.*?)```'
    
    def replace_block(match):
        ignore_test = match.group(1) is not None
        bash_content = match.group(2).rstrip()
        
        # Se o bloco já está vazio ou só tem comandos sem comentários, mantém
        if not bash_content or '#' not in bash_content:
            return match.group(0)
        
        return transform_bash_block(bash_content, ignore_test)
    
    # Substitui todos os blocos bash
    new_content = re.sub(pattern, replace_block, content, flags=re.DOTALL)
    
    return new_content

def main():
    # Define o diretório base
    base_dir = Path(__file__).parent.parent
    
    # Lista de arquivos para processar
    markdown_files = []
    
    # Arquivos numerados (01-31)
    for i in range(1, 32):
        pattern = f"{i:02d}-*.md"
        markdown_files.extend(base_dir.glob(pattern))
    
    # Arquivos especiais
    special_files = ['README.md', 'INICIO-RAPIDO.md', 'ESTRUTURA.md']
    for special in special_files:
        file_path = base_dir / special
        if file_path.exists():
            markdown_files.append(file_path)
    
    # Ordena para processamento consistente
    markdown_files.sort()
    
    print(f"Encontrados {len(markdown_files)} arquivos para processar")
    
    # Processa cada arquivo
    for file_path in markdown_files:
        print(f"Processando: {file_path.name}...", end=' ')
        
        try:
            new_content = process_markdown_file(file_path)
            
            # Salva o arquivo transformado
            file_path.write_text(new_content, encoding='utf-8')
            print("✓")
            
        except Exception as e:
            print(f"✗ Erro: {e}")
            return 1
    
    print(f"\n✓ Processamento concluído! {len(markdown_files)} arquivos transformados.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
