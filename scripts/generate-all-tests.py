#!/usr/bin/env python3
"""
Gerador Automático de Testes para OpenShift Commands Reference

Lê arquivos markdown (01-31) e gera automaticamente os test.sh
correspondentes com base nos comandos documentados.

Uso: python3 generate-all-tests.py [--verbose]
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional


class TestGenerator:
    """Gerador de scripts de teste a partir de documentação markdown."""
    
    # Constantes
    MARKDOWN_START = 1
    MARKDOWN_END = 31
    BASH_BLOCK_PATTERN = r'```bash(?:\s+ignore-test)?\n(.*?)```'
    OC_COMMAND_PREFIX = 'oc '
    
    def __init__(self, verbose: bool = False):
        # Script está em scripts/, então base_dir é o parent do parent
        self.base_dir = Path(__file__).parent.parent
        self.tests_dir = self.base_dir / "tests"
        self.verbose = verbose
        
    def _log(self, message: str, level: str = "info") -> None:
        """Log mensagens com níveis de verbosidade."""
        if level == "debug" and not self.verbose:
            return
        print(message)
        
    def find_markdown_files(self) -> List[Path]:
        """Encontra todos os arquivos markdown numerados (01-31)."""
        files = []
        for i in range(self.MARKDOWN_START, self.MARKDOWN_END + 1):
            matches = list(self.base_dir.glob(f"{i:02d}-*.md"))
            if matches:
                files.extend(matches)
            elif self.verbose:
                self._log(f"  Arquivo {i:02d}-*.md não encontrado", "debug")
        return sorted(files)
       
    def extract_commands(self, md_file: Path) -> Tuple[List[Tuple[str, str]], int]:
        """Extrai comandos de blocos ```bash (exceto os com ignore).

        Retorna uma tupla (commands, ignored_count).
        """
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            self._log(f"  ERRO ao ler {md_file.name}: {e}", "error")
            return [], 0
        
        commands = []
        ignored_count = 0
        
        # Split content in lines for easier processing
        lines = content.split('\n')
        
        # Encontra todos os blocos de código bash
        for block in re.finditer(self.BASH_BLOCK_PATTERN, content, re.DOTALL):
            # Ignora blocos marcados com 'ignore-test'
            first_line = block.group(0).split('\n')[0]
            if 'ignore-test' in first_line:
                self._log(f"  Bloco com teste ignorado: {block.group(0).split('\n')[1]} -> {block.group(0).split('\n')[2]}", "debug")
                # Count all commands inside ignored blocks approximately as lines starting with 'oc '
                for l in block.group(1).split('\n'):
                    if l.strip().startswith(self.OC_COMMAND_PREFIX):
                        ignored_count += 1
                continue
            
            # Try to find description in bold text before the code block
            # Look for pattern: **Description text**
            block_start_pos = block.start()
            
            # Find the line number of the block start
            preceding_text = content[:block_start_pos]
            preceding_lines = preceding_text.split('\n')
            
            # Look backwards for a line with **text**
            description_from_markdown = None
            for i in range(len(preceding_lines) - 1, max(0, len(preceding_lines) - 5), -1):
                line = preceding_lines[i].strip()
                # Match: **Some description text**
                desc_match = re.match(r'^\*\*(.+?)\*\*$', line)
                if desc_match:
                    description_from_markdown = desc_match.group(1).strip()
                    break
            
            # Processa comandos do bloco
            block_cmds, block_ignored = self._process_code_block(
                block.group(1), 
                default_description=description_from_markdown
            )
            commands.extend(block_cmds)
            ignored_count += block_ignored
        
        return commands, ignored_count
    
    def _process_code_block(self, block_content: str, default_description: str = None) -> Tuple[List[Tuple[str, str]], int]:
        """Processa um bloco de código e extrai comandos válidos.

        Retorna (commands, ignored_count_in_block).
        
        Args:
            block_content: Conteúdo do bloco de código
            default_description: Descrição extraída do markdown (texto em negrito antes do bloco)
        """
        commands = []
        comment = None
        ignored_count = 0

        lines = block_content.split('\n')
        i = 0
        while i < len(lines):
            raw = lines[i]
            line = raw.rstrip()

            # Skip empty lines
            if not line.strip():
                i += 1
                continue

            # Capture comments above commands
            if line.lstrip().startswith('#'):
                comment = line.lstrip('#').strip()
                i += 1
                continue

            # Check if line contains 'oc ' command (including pipes and here-docs)
            # Matches: oc ..., cat <<EOF | oc ..., echo ... | oc ...
            if self.OC_COMMAND_PREFIX in line:
                # Start accumulating possible multi-line command
                cmd_lines = [line]

                # Detect here-document on the first line (e.g. <<EOF)
                heredoc_match = re.search(r'<<-?\s*(?:"|\')?(?P<delim>\w+)(?:"|\')?', line)
                j = i + 1

                if heredoc_match:
                    delim = heredoc_match.group('delim')
                    # include lines until a line that equals the delimiter
                    while j < len(lines):
                        cmd_lines.append(lines[j])
                        if lines[j].strip() == delim:
                            j += 1
                            break
                        j += 1
                else:
                    # otherwise, include continuation lines while they look like part of the command
                    while j < len(lines):
                        nxt = lines[j]
                        # If previous line explicitly ends with backslash, always continue
                        if cmd_lines[-1].rstrip().endswith('\\'):
                            cmd_lines.append(nxt)
                            j += 1
                            continue

                        # If next line is a comment or empty, stop
                        if not nxt.strip() or nxt.lstrip().startswith('#'):
                            break

                        # If next line contains 'oc ' it's a new command -> stop
                        if self.OC_COMMAND_PREFIX in nxt:
                            break

                        # If next line is indented (common continuation) or starts with pipe/operators, include
                        if re.match(r'^\s', nxt) or re.match(r'^\s*[|&;]', nxt):
                            cmd_lines.append(nxt)
                            j += 1
                            continue

                        # Otherwise, stop accumulation
                        break

                full_cmd = '\n'.join(cmd_lines).strip()

                # Validate command (use the first non-empty line for validation)
                first_cmd_line = full_cmd.split('\n', 1)[0].strip()
                
                # Priority: comment from code > default_description > auto-extracted
                if comment:
                    desc = comment
                elif default_description:
                    desc = default_description
                else:
                    desc = self._extract_description(first_cmd_line)
                
                commands.append((desc, full_cmd))
                comment = None
                i = j
                continue

            # If we reach here, not a comment or oc command -> skip
            i += 1

        return commands, ignored_count
        
    def _extract_description(self, cmd: str) -> str:
        """Extrai descrição amigável do comando (oc <action> <resource>)."""
        parts = cmd.split()
        if len(parts) >= 3:
            return f"{parts[1].capitalize()} {parts[2]}"
        elif len(parts) >= 2:
            return parts[1].capitalize()
        return "Comando OpenShift"
    
    def _escape_shell_string(self, text: str) -> str:
        """Escapa caracteres especiais para uso em strings shell."""
        return text.replace('"', '\\"').replace('$', '\\$')
    
    def _parse_module_info(self, md_file: Path) -> Optional[Tuple[str, str]]:
        """Extrai número e nome do módulo do nome do arquivo."""
        match = re.match(r'(\d+)-(.*)', md_file.stem)
        if not match:
            self._log(f"  AVISO: Nome de arquivo inválido: {md_file.name}", "error")
            return None
        
        module_num = match.group(1)
        module_name = match.group(2).replace('-', ' ').upper()
        return module_num, module_name
    
    def generate_test_file(self, md_file: Path, commands: List[Tuple[str, str]]) -> str:
        """Gera conteúdo do test.sh a partir dos comandos extraídos."""
        module_info = self._parse_module_info(md_file)
        if not module_info:
            return ""
        
        module_num, module_name = module_info
        
        # Cabeçalho do arquivo
        lines = [
            "#!/bin/bash",
            "#",
            f"# Testes para Módulo {module_num}: {module_name}",
            f"# Auto-gerado a partir de {md_file.name}",
            "#\n",
            'SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"\n',
            'source "${SCRIPT_DIR}/../../lib/common.sh"\n',
            f'section_header "{module_num} - {module_name}"\n'
        ]
        
        # Adiciona cada teste
        for comment, cmd in commands:
            comment_esc = self._escape_shell_string(comment)
            cmd_esc = self._escape_shell_string(cmd)
            
            lines.append(f'run_test "{comment_esc}" \\')
            lines.append(f'    "{cmd_esc}"\n')
        
        return '\n'.join(lines)
    
    def write_test_file(self, md_file: Path, content: str) -> Path:
        """Escreve test.sh no diretório apropriado e torna executável."""
        test_dir = self.tests_dir / md_file.stem
        test_dir.mkdir(parents=True, exist_ok=True)
        
        test_file = test_dir / "test.sh"
        
        try:
            test_file.write_text(content, encoding='utf-8')
            test_file.chmod(0o755)
        except Exception as e:
            self._log(f"  ERRO ao escrever {test_file}: {e}", "error")
            raise
        
        return test_file
    
    def generate_all(self) -> None:
        """Gera todos os testes a partir dos arquivos markdown."""
        print("Gerador Automático de Testes")
        print("=" * 60)

        md_files = self.find_markdown_files()
        print(f"\n{len(md_files)} arquivos markdown encontrados\n")

        total_commands = 0
        total_ignored = 0
        generated = 0
        errors = 0
        total_included = 0

        for md_file in md_files:
            print(md_file.name)

            try:
                commands, ignored = self.extract_commands(md_file)
                if not commands:
                    print("  Nenhum comando válido encontrado\n")
                    total_ignored += ignored
                    continue

                print(f"  {len(commands)} comandos extraídos ({ignored} ignorados)")

                content = self.generate_test_file(md_file, commands)
                if not content:
                    errors += 1
                    continue
                
                test_file = self.write_test_file(md_file, content)
                print(f"  Gerado: {test_file.relative_to(self.base_dir)}\n")

                total_commands += len(commands)
                total_ignored += ignored
                total_included += len(commands)
                generated += 1
                
            except Exception as e:
                self._log(f"  ERRO ao processar: {e}\n", "error")
                errors += 1
                continue

        # Sumário
        print("=" * 60)
        print("Concluído!")
        print(f"   {generated} arquivos test.sh gerados")
        print(f"   {total_included} comandos incluídos (entraram nos testes)")
        print(f"   {total_ignored} comandos ignorados (ignore-test ou inválidos)")
        print(f"   {total_included + total_ignored} comandos totais")
        if errors > 0:
            print(f"   {errors} erros encontrados")
        print(f"\nExecute: ./scripts/test-commands.sh")

        # Retorna código de saída apropriado
        sys.exit(1 if errors > 0 else 0)


def main():
    """Ponto de entrada principal."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Gerador Automático de Testes para OpenShift Commands'
    )
    parser.add_argument('-v', '--verbose', action='store_true', help='Ativa saída verbosa')

    args = parser.parse_args()

    generator = TestGenerator(verbose=args.verbose)
    generator.generate_all()


if __name__ == "__main__":
    main()
