#!/usr/bin/env python3
"""
Script para identificar comandos duplicados entre os arquivos markdown.
Analisa blocos de código bash e reporta duplicatas.
"""

import re
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict


class DuplicateFinder:
    """Encontra comandos duplicados entre arquivos markdown."""
    
    BASH_BLOCK_PATTERN = r'```bash(?:\s+ignore-test)?\n(.*?)```'
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.command_locations: Dict[str, List[tuple]] = defaultdict(list)
        
    def extract_commands(self, md_file: Path) -> List[str]:
        """Extrai comandos únicos de um arquivo markdown."""
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  ERRO ao ler {md_file.name}: {e}")
            return []
        
        commands = []
        
        # Encontra todos os blocos de código bash
        for block in re.finditer(self.BASH_BLOCK_PATTERN, content, re.DOTALL):
            block_content = block.group(1)
            
            # Extrai linhas que começam com 'oc ' ou contêm ' oc '
            for line in block_content.split('\n'):
                line = line.strip()
                
                # Ignora comentários e linhas vazias
                if not line or line.startswith('#'):
                    continue
                
                # Normaliza o comando para comparação
                # Remove espaços extras, aspas variáveis, etc
                if 'oc ' in line:
                    # Normaliza para comparação (mantém estrutura base)
                    normalized = self._normalize_command(line)
                    if normalized:
                        commands.append(normalized)
        
        return commands
    
    def _normalize_command(self, cmd: str) -> str:
        """Normaliza comando para facilitar comparação de duplicatas."""
        # Remove comentários inline
        cmd = re.sub(r'\s*#.*$', '', cmd)
        
        # Remove espaços extras
        cmd = ' '.join(cmd.split())
        
        # Ignora comandos muito genéricos (sem flags ou argumentos específicos)
        if cmd.strip() in ['oc get pods', 'oc get all', 'oc status', 'oc projects']:
            return ""
        
        # Remove valores específicos mas mantém flags
        # Ex: -n development -> -n <namespace>
        cmd = re.sub(r'-n\s+\S+', '-n <namespace>', cmd)
        cmd = re.sub(r'--namespace\s+\S+', '--namespace <namespace>', cmd)
        
        # Remove nomes específicos de recursos mas mantém tipo
        # Ex: oc get pod my-pod -> oc get pod <name>
        patterns = [
            (r'(oc\s+\w+\s+pod)\s+\S+', r'\1 <name>'),
            (r'(oc\s+\w+\s+deployment)\s+\S+', r'\1 <name>'),
            (r'(oc\s+\w+\s+service)\s+\S+', r'\1 <name>'),
            (r'(oc\s+\w+\s+route)\s+\S+', r'\1 <name>'),
            (r'(oc\s+\w+\s+secret)\s+\S+', r'\1 <name>'),
            (r'(oc\s+\w+\s+configmap)\s+\S+', r'\1 <name>'),
        ]
        
        for pattern, replacement in patterns:
            cmd = re.sub(pattern, replacement, cmd)
        
        return cmd.strip()
    
    def find_duplicates(self) -> Dict[str, List[tuple]]:
        """Encontra comandos duplicados em todos os arquivos."""
        # Encontrar arquivos markdown numerados
        md_files = []
        for i in range(1, 31):
            matches = list(self.base_dir.glob(f"{i:02d}-*.md"))
            if matches:
                md_files.extend(matches)
        
        md_files = sorted(md_files)
        
        # Extrair comandos de cada arquivo
        for md_file in md_files:
            commands = self.extract_commands(md_file)
            
            for cmd in commands:
                self.command_locations[cmd].append(md_file.name)
        
        # Filtrar apenas duplicatas
        duplicates = {
            cmd: files 
            for cmd, files in self.command_locations.items() 
            if len(set(files)) > 1  # Aparece em mais de um arquivo
        }
        
        return duplicates
    
    def report_duplicates(self, duplicates: Dict[str, List[tuple]]) -> None:
        """Gera relatório de comandos duplicados."""
        if not duplicates:
            print("\nOK Nenhum comando duplicado encontrado!")
            return
        
        print(f"\nAVISO:  {len(duplicates)} comandos duplicados encontrados:\n")
        print("=" * 80)
        
        # Agrupa por número de arquivos
        by_count = defaultdict(list)
        for cmd, files in duplicates.items():
            unique_files = list(set(files))
            by_count[len(unique_files)].append((cmd, unique_files))
        
        # Mostra em ordem decrescente de duplicação
        for count in sorted(by_count.keys(), reverse=True):
            items = by_count[count]
            print(f"\n## Comandos em {count} arquivos diferentes ({len(items)} comandos):\n")
            
            for cmd, files in sorted(items, key=lambda x: x[1]):
                print(f"Comando: {cmd}")
                print(f"Arquivos: {', '.join(sorted(files))}")
                print()
        
        print("=" * 80)
        print("\nDICA: Sugestões:")
        print("1. Revisar comandos muito comuns (get, describe) - podem ser legítimos")
        print("2. Comandos específicos duplicados devem ficar no contexto mais apropriado")
        print("3. Considerar criar referências cruzadas em vez de duplicar")
    
    def generate_removal_script(self, duplicates: Dict[str, List[tuple]]) -> None:
        """Gera um relatório CSV para análise manual."""
        csv_file = self.base_dir / "duplicates-report.csv"
        
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write("Comando,Arquivos,Contagem,Ação Sugerida\n")
            
            for cmd, files in sorted(duplicates.items()):
                unique_files = sorted(set(files))
                count = len(unique_files)
                files_str = '; '.join(unique_files)
                
                # Sugestão baseada no comando
                if count <= 2:
                    action = "MANTER_UM"
                elif any(word in cmd for word in ['get pods', 'get all', 'describe']):
                    action = "REVISAR"
                else:
                    action = "CONSOLIDAR"
                
                f.write(f'"{cmd}","{files_str}",{count},{action}\n')
        
        print(f"\n Relatório CSV gerado: {csv_file}")


def main():
    """Ponto de entrada principal."""
    print("Analisador de Comandos Duplicados")
    print("=" * 80)
    
    finder = DuplicateFinder()
    duplicates = finder.find_duplicates()
    
    finder.report_duplicates(duplicates)
    finder.generate_removal_script(duplicates)


if __name__ == "__main__":
    main()
