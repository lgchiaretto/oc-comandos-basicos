#!/usr/bin/env python3
"""
Script para corrigir blocos markdown onde comandos exemplo aparecem como itens de lista.
Transforma linhas como "* oc command <args>" em descrições formatadas com código inline.
"""

import re
import sys
from pathlib import Path

def fix_markdown_block(content: str) -> str:
    """
    Corrige blocos markdown que têm comandos como itens de lista.
    Transforma:
        * oc project <project-name>
    Em:
        **Exemplo:** `oc project <project-name>`
    """
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Detecta linhas que são comandos oc em formato de lista
        match = re.match(r'^\* (oc .+)$', line)
        if match:
            command = match.group(1)
            # Se o comando tem placeholders <...>, trata como exemplo
            if '<' in command and '>' in command:
                fixed_lines.append(f"**Exemplo:** `{command}`")
            # Se parece com uma flag/opção explicativa
            elif command.startswith('oc ') and ':' not in command and '--' not in line:
                fixed_lines.append(f"**Sintaxe:** `{command}`")
            else:
                # Mantém como está (é uma descrição válida)
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def process_file(file_path: Path) -> tuple[bool, int]:
    """
    Processa um arquivo markdown.
    Retorna (modificado, numero_de_correcoes)
    """
    content = file_path.read_text(encoding='utf-8')
    
    # Padrão para encontrar blocos markdown
    pattern = r'```markdown\n(.*?)\n```'
    
    corrections = 0
    
    def fix_block(match):
        nonlocal corrections
        markdown_content = match.group(1)
        fixed_content = fix_markdown_block(markdown_content)
        
        if fixed_content != markdown_content:
            corrections += 1
        
        return f'```markdown\n{fixed_content}\n```'
    
    # Substitui todos os blocos markdown
    new_content = re.sub(pattern, fix_block, content, flags=re.DOTALL)
    
    # Retorna se houve modificação
    modified = new_content != content
    
    if modified:
        file_path.write_text(new_content, encoding='utf-8')
    
    return modified, corrections

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
    
    print(f"Verificando {len(markdown_files)} arquivos...")
    
    total_modified = 0
    total_corrections = 0
    
    # Processa cada arquivo
    for file_path in markdown_files:
        modified, corrections = process_file(file_path)
        
        if modified:
            total_modified += 1
            total_corrections += corrections
            print(f"✓ {file_path.name}: {corrections} correções")
    
    print(f"\n{'='*60}")
    if total_modified > 0:
        print(f"✓ Correção concluída!")
        print(f"  - {total_modified} arquivos modificados")
        print(f"  - {total_corrections} blocos corrigidos")
    else:
        print("✓ Nenhuma correção necessária")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
