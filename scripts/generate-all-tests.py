#!/usr/bin/env python3
"""
Gerador Automático de Testes para OpenShift Commands Reference

Lê arquivos markdown (01-30) e gera automaticamente os test.sh
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
    MARKDOWN_END = 30
    BASH_BLOCK_PATTERN = r'```bash(?:\s+ignore)?\n(.*?)```'
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
        """Encontra todos os arquivos markdown numerados (01-30)."""
        files = []
        for i in range(self.MARKDOWN_START, self.MARKDOWN_END + 1):
            matches = list(self.base_dir.glob(f"{i:02d}-*.md"))
            if matches:
                files.extend(matches)
            elif self.verbose:
                self._log(f"  Arquivo {i:02d}-*.md não encontrado", "debug")
        return sorted(files)
    
    def _is_valid_command(self, cmd: str) -> bool:
        """Valida se o comando é apropriado para teste."""
        # Comandos interativos que não devem ser testados
        interactive_commands = ['oc login', 'oc logout', 'oc edit', 'oc rsh', 'oc rsync']
        if any(cmd.startswith(ic) for ic in interactive_commands):
            return False
            
        # Comandos com placeholders não substituídos
        if '<' in cmd and '>' in cmd:
            self._log(f"  Ignorando comando com placeholder: {cmd[:50]}...", "debug")
            return False
            
        return True
    
    def extract_commands(self, md_file: Path) -> List[Tuple[str, str]]:
        """Extrai comandos de blocos ```bash (exceto os com ignore)."""
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            self._log(f"  ERRO ao ler {md_file.name}: {e}", "error")
            return []
        
        commands = []
        
        # Encontra todos os blocos de código bash
        for block in re.finditer(self.BASH_BLOCK_PATTERN, content, re.DOTALL):
            # Ignora blocos marcados com 'ignore'
            first_line = block.group(0).split('\n')[0]
            if 'ignore' in first_line:
                self._log(f"  Bloco com teste ignorado: {block.group(0).split('\n')[1]} -> {block.group(0).split('\n')[2]}", "debug")
                continue
            
            # Processa comandos do bloco
            commands.extend(self._process_code_block(block.group(1)))
        
        return commands
    
    def _process_code_block(self, block_content: str) -> List[Tuple[str, str]]:
        """Processa um bloco de código e extrai comandos válidos."""
        commands = []
        comment = None
        
        for line in block_content.strip().split('\n'):
            line = line.strip()
            
            if not line:
                continue
                
            # Captura comentários
            if line.startswith('#'):
                comment = line.lstrip('#').strip()
                continue
            
            # Captura comandos oc válidos
            if line.startswith(self.OC_COMMAND_PREFIX):
                if not self._is_valid_command(line):
                    comment = None
                    continue
                    
                desc = comment or self._extract_description(line)
                commands.append((desc, line))
                comment = None
        
        return commands
        
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
            'source "lib/common.sh"\n',
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
        generated = 0
        errors = 0

        for md_file in md_files:
            print(md_file.name)

            try:
                commands = self.extract_commands(md_file)
                if not commands:
                    print("  Nenhum comando encontrado\n")
                    continue

                print(f"  {len(commands)} comandos extraídos")

                content = self.generate_test_file(md_file, commands)
                if not content:
                    errors += 1
                    continue
                
                test_file = self.write_test_file(md_file, content)
                print(f"  Gerado: {test_file.relative_to(self.base_dir)}\n")

                total_commands += len(commands)
                generated += 1
                
            except Exception as e:
                self._log(f"  ERRO ao processar: {e}\n", "error")
                errors += 1
                continue

        # Sumário
        print("=" * 60)
        print("Concluído!")
        print(f"   {generated} arquivos gerados")
        print(f"   {total_commands} comandos totais")
        if errors > 0:
            print(f"   {errors} erros encontrados")
        print(f"\nExecute: ./scripts/test-commands.sh")
        
        # Retorna código de saída apropriado
        sys.exit(1 if errors > 0 else 0)


def main():
    """Ponto de entrada principal."""
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    generator = TestGenerator(verbose=verbose)
    generator.generate_all()


if __name__ == "__main__":
    main()
