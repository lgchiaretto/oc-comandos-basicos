#!/usr/bin/env python3
"""
Gerador Automático de Testes para OpenShift Commands Reference

Este script lê todos os arquivos markdown (01-30) e gera automaticamente
os arquivos test.sh correspondentes com base nos comandos documentados.

Uso:
    python3 generate-all-tests.py
"""

import re
from pathlib import Path
from typing import List, Tuple

# -----------------------------
# Customize here: comandos/padrões a serem ignorados pelo gerador.
# Adicione strings que devem ser ignoradas. A correspondência é
# case-insensitive e considera igualdade, startswith ou substring.
# Exemplo: ['oc logout', 'oc login --token']
IGNORED_COMMAND_PATTERNS = [
    'oc logout', "oc edit"
]
# -----------------------------

class TestGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.tests_dir = self.base_dir / "tests"
        self.markdown_files = []
        # Usa a lista definida acima; mantém-na acessível via instância
        self.ignored_patterns = IGNORED_COMMAND_PATTERNS
        
    def find_markdown_files(self) -> List[Path]:
        """Encontra todos os arquivos markdown numerados (01-30)"""
        md_files = []
        for i in range(1, 31):
            pattern = f"{i:02d}-*.md"
            matches = list(self.base_dir.glob(pattern))
            if matches:
                md_files.extend(matches)
        return sorted(md_files)
    
    def extract_commands(self, md_file: Path) -> List[Tuple[str, str]]:
        """
        Extrai comandos e comentários de um arquivo markdown
        
        Returns:
            Lista de tuplas (comentário, comando)
        """
        commands = []
        content = md_file.read_text(encoding='utf-8')
        
        # Regex para encontrar blocos de código bash
        code_blocks = re.finditer(r'```bash\n(.*?)```', content, re.DOTALL)
        
        for block in code_blocks:
            code_content = block.group(1)
            lines = code_content.strip().split('\n')
            
            comment = None
            for line in lines:
                line = line.strip()
                
                # Ignora linhas vazias
                if not line:
                    continue
                
                # Captura comentários
                if line.startswith('#'):
                    # Remove o # e espaços
                    comment = line.lstrip('#').strip()
                    continue
                
                # Se é um comando oc e temos um comentário
                if line.startswith('oc ') and comment:
                    # Limpa o comando
                    cmd = line.strip()

                    # Ignora comandos explicitamente configurados
                    if self._should_ignore_command(cmd):
                        comment = None
                        continue

                    # Ignora comandos que são apenas exemplos ou placeholders
                    if self._is_valid_command(cmd):
                        commands.append((comment, cmd))

                    comment = None  # Reset para o próximo comando
                
                # Se é um comando oc sem comentário, usa um genérico
                elif line.startswith('oc ') and not comment:
                    cmd = line.strip()
                    # Ignora comandos explicitamente configurados
                    if self._should_ignore_command(cmd):
                        continue

                    if self._is_valid_command(cmd):
                        # Tenta extrair uma descrição do comando
                        desc = self._generate_description(cmd)
                        commands.append((desc, cmd))
        
        return commands
    
    def _is_valid_command(self, cmd: str) -> bool:
        """Verifica se o comando é válido para teste"""
        # Ignora comandos com placeholders óbvios
        invalid_patterns = [
            '<', '>',  # Placeholders com < >
            'seu-', 'sua-', 'nome-do-', 'nome-da-',  # Placeholders em português
            'your-', 'my-',  # Placeholders em inglês
            'example', 'exemplo',
            'xxx', 'yyy'
            , '...',  # Comandos incompletos
        ]
        
        cmd_lower = cmd.lower()
        for pattern in invalid_patterns:
            if pattern in cmd_lower:
                return False

        # Também ignora padrões configurados no topo do script
        for pattern in getattr(self, 'ignored_patterns', []):
            if not pattern:
                continue
            p = pattern.lower().strip()
            if not p:
                continue
            if cmd_lower == p or cmd_lower.startswith(p) or p in cmd_lower:
                return False
        
        return True

    def _should_ignore_command(self, cmd: str) -> bool:
        """Retorna True se o comando deve ser ignorado com base nos padrões configurados."""
        if not cmd:
            return False

        cmd_lower = cmd.strip().lower()
        for pattern in getattr(self, 'ignored_patterns', []):
            if not pattern:
                continue
            p = pattern.lower().strip()
            if not p:
                continue
            if cmd_lower == p or cmd_lower.startswith(p) or p in cmd_lower:
                return True

        return False
    
    def _generate_description(self, cmd: str) -> str:
        """Gera uma descrição genérica baseada no comando"""
        # Extrai o verbo/ação principal do comando
        parts = cmd.split()
        if len(parts) >= 2:
            action = parts[1]
            if len(parts) >= 3:
                resource = parts[2]
                return f"{action.capitalize()} {resource}"
            return f"{action.capitalize()}"
        return "Comando OpenShift"
    
    def _sanitize_command(self, cmd: str) -> str:
        """
        Sanitiza o comando para ser usado no test.sh
        - Adiciona tratamento de erro quando apropriado
        - Suprime erros esperados
        """
        # Comandos que podem falhar legitimamente
        may_fail_patterns = [
            'oc delete',
            'oc create',
            'oc new-project',
            'oc scale',
            'oc set',
            'oc patch',
            'oc label',
            'oc annotate',
        ]
        
        # Comandos administrativos que podem requerer permissões
        admin_patterns = [
            'oc adm',
            'oc get nodes',
            'oc get clusteroperators',
            'oc get co ',
            'oc get csr',
            'oc get machinesets',
            'oc get machines',
        ]
        
        for pattern in may_fail_patterns:
            if cmd.startswith(pattern):
                if '||' not in cmd and '2>' not in cmd:
                    return f"{cmd} 2>/dev/null || true"
        
        for pattern in admin_patterns:
            if pattern in cmd:
                if '2>' not in cmd:
                    return f"{cmd} 2>/dev/null || true"
        
        return cmd
    
    def generate_test_file(self, md_file: Path, commands: List[Tuple[str, str]]) -> str:
        """Gera o conteúdo do arquivo test.sh"""
        # Extrai número e nome do módulo
        filename = md_file.stem
        match = re.match(r'(\d+)-(.*)', filename)
        if not match:
            return ""
        
        module_num = match.group(1)
        module_name = match.group(2).replace('-', ' ').upper()
        
        # Cabeçalho do arquivo
        content = f"""#!/bin/bash
#
# Testes para Módulo {module_num}: {module_name}
# Auto-gerado a partir de {md_file.name}
#

source "lib/common.sh"

section_header "{module_num} - {module_name}"

"""
        
        # Adiciona os testes
        for idx, (comment, cmd) in enumerate(commands, 1):
            sanitized_cmd = self._sanitize_command(cmd)
            
            # Escapa aspas duplas no comentário e comando
            comment_escaped = comment.replace('"', '\\"')
            cmd_escaped = sanitized_cmd.replace('"', '\\"').replace('$', '\\$')
            
            content += f"""run_test "{comment_escaped}" \\
    "{cmd_escaped}"

"""       
        return content
    
    def create_test_directory(self, md_file: Path) -> Path:
        """Cria o diretório de teste se não existir"""
        filename = md_file.stem
        test_dir = self.tests_dir / filename
        test_dir.mkdir(parents=True, exist_ok=True)
        return test_dir
    
    def write_test_file(self, test_dir: Path, content: str):
        """Escreve o arquivo test.sh e torna executável"""
        test_file = test_dir / "test.sh"
        test_file.write_text(content, encoding='utf-8')
        test_file.chmod(0o755)
        print(f"  ✅ Gerado: {test_file.relative_to(self.base_dir)}")
    
    def generate_all_tests(self):
        """Função principal que gera todos os testes"""
        print("🚀 Gerador Automático de Testes - OpenShift Commands")
        print("=" * 60)
        
        # Encontra todos os arquivos markdown
        self.markdown_files = self.find_markdown_files()
        print(f"\n📄 Encontrados {len(self.markdown_files)} arquivos markdown\n")
        
        total_commands = 0
        generated_files = 0
        
        for md_file in self.markdown_files:
            print(f"📝 Processando: {md_file.name}")
            
            # Extrai comandos
            commands = self.extract_commands(md_file)
            
            if not commands:
                print(f"  ⚠️  Nenhum comando encontrado")
                continue
            
            print(f"  📊 {len(commands)} comandos extraídos")
            
            # Gera conteúdo do test.sh
            test_content = self.generate_test_file(md_file, commands)
            
            if test_content:
                # Cria diretório e escreve arquivo
                test_dir = self.create_test_directory(md_file)
                self.write_test_file(test_dir, test_content)
                
                total_commands += len(commands)
                generated_files += 1
            
            print()
        
        # Sumário
        print("=" * 60)
        print(f"✅ Geração concluída!")
        print(f"📊 Estatísticas:")
        print(f"   - Arquivos processados: {len(self.markdown_files)}")
        print(f"   - Arquivos test.sh gerados: {generated_files}")
        print(f"   - Total de comandos: {total_commands}")
        print(f"\n💡 Para executar os testes:")
        print(f"   ./test-commands.sh")
        print(f"   ./test-commands.sh --module 05")


def main():
    """Função principal"""
    generator = TestGenerator()
    generator.generate_all_tests()


if __name__ == "__main__":
    main()
