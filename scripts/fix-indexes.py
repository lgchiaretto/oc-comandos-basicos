#!/usr/bin/env python3
"""
Script para corrigir automaticamente os índices em arquivos markdown.
Gera índice APENAS com seções de nível 2 (##), excluindo subseções (###).
"""

import re
from pathlib import Path
from typing import List, Tuple


def extract_main_sections(content: str) -> List[Tuple[str, str, str]]:
    """Extrai apenas seções principais (## Título) do markdown.
    
    Retorna lista de tuplas (titulo, anchor).
    Ignora subseções (###) e seções especiais.
    """
    sections = []
    
    # Pattern para capturar apenas ## (nível 2)
    # Usa ^## seguido de espaço (não ###)
    pattern = r'^## ([^#].*?)$'
    
    for match in re.finditer(pattern, content, re.MULTILINE):
        full_title = match.group(1).strip()
        
        # Ignorar seções especiais
        if any(x in full_title for x in ['Índice', 'Navegação', 'Documentação']):
            continue
        
        title = full_title
        
        # Gerar anchor (lowercase, sem acentos, hífens)
        anchor = title.lower()
        ## Remove acentos
        #anchor = re.sub(r'[àáâãäå]', 'a', anchor)
        #anchor = re.sub(r'[èéêë]', 'e', anchor)
        #anchor = re.sub(r'[ìíîï]', 'i', anchor)
        #anchor = re.sub(r'[òóôõö]', 'o', anchor)
        #anchor = re.sub(r'[ùúûü]', 'u', anchor)
        #anchor = re.sub(r'[ç]', 'c', anchor)
        ## Remove caracteres especiais
        #anchor = re.sub(r'[^a-z0-9\s-]', '', anchor)
        ## Substitui espaços por hífens
        #anchor = re.sub(r'\s+', '-', anchor)
        ## Remove hífens duplicados
        #anchor = re.sub(r'-+', '-', anchor)
        #anchor = anchor.strip('-')
        
        sections.append((title, anchor))
    
    return sections


def generate_index(sections: List[Tuple[str, str]]) -> str:
    """Gera o conteúdo do índice a partir das seções."""
    if not sections:
        return ""
    
    lines = ["## Índice\n"]
    
    for i, (title, anchor) in enumerate(sections, 1):
        # Formato: 1. [Título](#anchor)
        lines.append(f"{i}. [{title}](#{anchor})")
    
    return '\n'.join(lines)


def fix_index_in_file(file_path: Path, verbose: bool = False) -> bool:
    """Corrige o índice em um arquivo markdown.
    
    Retorna True se houve modificação.
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ERRO ao ler {file_path.name}: {e}")
        return False
    
    # Extrair seções principais
    sections = extract_main_sections(content)
    
    if not sections:
        print(f"  AVISO:  Nenhuma seção principal encontrada")
        return False
    
    if verbose:
        print(f"  Seções encontradas: {[s[0] for s in sections]}")
    
    # Gerar novo índice
    new_index = generate_index(sections)
    
    # Pattern para encontrar o índice existente
    # Procura por "## Índice" até a próxima linha com "---"
    # Inclui a linha com "---" para manter separador após índice
    index_pattern = r'## Índice\n.*?\n---'
    
    # Verificar se índice existe
    if not re.search(index_pattern, content, re.DOTALL):
        print(f"  AVISO:  Índice não encontrado no arquivo")
        return False
    
    # Substituir índice (adiciona --- no final)
    new_content = re.sub(
        index_pattern, 
        new_index.rstrip() + '\n---', 
        content, 
        count=1, 
        flags=re.DOTALL
    )
    
    # Salvar apenas se houve mudança
    if new_content != content:
        file_path.write_text(new_content, encoding='utf-8')
        print(f"  OK Índice corrigido ({len(sections)} seções)")
        return True
    else:
        print(f"  INFO:  Índice já está correto")
        return False


def main():
    """Ponto de entrada principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Corrige índices em arquivos markdown')
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verbose')
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    
    print("Corretor Automático de Índices")
    print("=" * 60)
    
    # Encontrar arquivos markdown numerados
    md_files = []
    for i in range(1, 31):
        matches = list(base_dir.glob(f"{i:02d}-*.md"))
        if matches:
            md_files.extend(matches)
    
    md_files = sorted(md_files)
    print(f"\n{len(md_files)} arquivos encontrados\n")
    
    fixed_count = 0
    
    for md_file in md_files:
        print(f"{md_file.name}")
        if fix_index_in_file(md_file, args.verbose):
            fixed_count += 1
        print()
    
    print("=" * 60)
    print(f"Concluído! {fixed_count} índices corrigidos")


if __name__ == "__main__":
    main()
