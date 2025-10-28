#!/usr/bin/env python3
"""
Script para melhorar comentários de comandos que usam grep em arquivos markdown.

Transforma comentários genéricos como "Exibir pod em formato YAML" 
em descrições específicas como "Exibir detalhes completos do pod filtrando por Volumes"
quando o comando usa grep.

Uso:
    python3 scripts/improve-grep-comments.py [--dry-run] [--file FILE]

Exemplos:
    # Modo dry-run (apenas mostra o que seria alterado)
    python3 scripts/improve-grep-comments.py --dry-run
    
    # Aplicar em um arquivo específico
    python3 scripts/improve-grep-comments.py --file 04-pods-containers.md
    
    # Aplicar em todos os arquivos
    python3 scripts/improve-grep-comments.py
"""

import re
import os
import sys
import argparse
from pathlib import Path
from typing import Optional, Tuple, List

def analyze_grep_pattern(command: str) -> Optional[str]:
    """
    Analisa um comando com grep e retorna uma descrição específica.
    
    Args:
        command: Linha de comando completa
        
    Returns:
        String descritiva do que o grep está filtrando, ou None se não aplicável
    """
    # Extrair o padrão do grep - ignorando flags que são parâmetros, não padrões
    grep_patterns = [
        # grep -A N "pattern with spaces" (com aspas)
        r'grep\s+-A\s+\d+\s+["\']([^"\']+)["\']',
        # grep -B N "pattern with spaces" (com aspas)
        r'grep\s+-B\s+\d+\s+["\']([^"\']+)["\']',
        # grep -C N "pattern with spaces" (com aspas)
        r'grep\s+-C\s+\d+\s+["\']([^"\']+)["\']',
        # grep -A N pattern (sem aspas)
        r'grep\s+-A\s+\d+\s+([A-Za-z][A-Za-z0-9_:-]*)',
        # grep -B N pattern (sem aspas)
        r'grep\s+-B\s+\d+\s+([A-Za-z][A-Za-z0-9_:-]*)',
        # grep -C N pattern (sem aspas)
        r'grep\s+-C\s+\d+\s+([A-Za-z][A-Za-z0-9_:-]*)',
        # grep -i "pattern" (case insensitive com aspas)
        r'grep\s+-i\s+["\']([^"\']+)["\']',
        # grep -i pattern (case insensitive sem aspas)
        r'grep\s+-i\s+([A-Za-z][A-Za-z0-9_\s:-]*)',
        # grep "pattern with spaces" (com aspas)
        r'grep\s+["\']([^"\']+)["\']',
        # grep pattern (simples, sem aspas, apenas palavras)
        r'grep\s+([A-Za-z][A-Za-z0-9_:-]*)',
    ]
    
    pattern_found = None
    for pattern in grep_patterns:
        match = re.search(pattern, command)
        if match:
            candidate = match.group(1).strip()
            # Ignorar padrões que são regex complexos (contêm caracteres especiais de regex)
            # Aceitar apenas padrões simples: letras, números, underscore, hífen, dois-pontos, espaços
            if re.match(r'^[A-Za-z][A-Za-z0-9_:\s-]*$', candidate):
                pattern_found = candidate
                break
    
    if not pattern_found:
        return None
    
    # Determinar o tipo de comando base (antes do pipe)
    command_base = command.split('|')[0].strip()
    
    # Analisar o comando base para determinar o recurso
    resource_type = None
    action = None
    
    # Detectar oc describe
    if 'oc describe' in command_base or 'oc adm' in command_base:
        action = "Exibir detalhes completos"
        
        # Detectar tipo de recurso
        if re.search(r'\bpod\b', command_base):
            resource_type = "do pod"
        elif re.search(r'\bpods\b', command_base):
            resource_type = "dos pods"
        elif re.search(r'\bnode\b', command_base):
            resource_type = "do node"
        elif re.search(r'\bnodes\b', command_base):
            resource_type = "dos nodes"
        elif re.search(r'\bdeployment\b|\bdeploy\b', command_base):
            resource_type = "do deployment"
        elif re.search(r'\bservice\b|\bsvc\b', command_base):
            resource_type = "do service"
        elif re.search(r'\broute\b', command_base):
            resource_type = "da route"
        elif re.search(r'\bconfigmap\b|\bcm\b', command_base):
            resource_type = "do configmap"
        elif re.search(r'\bsecret\b', command_base):
            resource_type = "do secret"
        elif re.search(r'\bpvc\b|persistentvolumeclaim', command_base):
            resource_type = "do pvc"
        elif re.search(r'\bpv\b|persistentvolume', command_base):
            resource_type = "do pv"
        elif re.search(r'\bco\b|clusteroperator', command_base):
            resource_type = "do cluster operator"
        elif re.search(r'\bmcp\b|machineconfigpool', command_base):
            resource_type = "do machineconfigpool"
        elif re.search(r'\bclusterversion\b', command_base):
            resource_type = "do clusterversion"
        elif re.search(r'\bcsr\b|certificatesigningrequest', command_base):
            resource_type = "do csr"
        elif re.search(r'\bnamespace\b|\bns\b', command_base):
            resource_type = "do namespace"
        elif re.search(r'\bbuildconfig\b|\bbc\b', command_base):
            resource_type = "do buildconfig"
        elif re.search(r'\bproject\b', command_base):
            resource_type = "do projeto"
        elif re.search(r'\bclusterversion\b', command_base):
            resource_type = "da clusterversion"
        elif re.search(r'\bclusterrole\b', command_base):
            resource_type = "da clusterrole"
        else:
            resource_type = "do recurso"
    
    # Detectar oc get
    elif 'oc get' in command_base:
        action = "Listar"
        
        if re.search(r'\bpods?\b', command_base):
            resource_type = "pods"
        elif re.search(r'\bnodes?\b', command_base):
            resource_type = "nodes"
        elif re.search(r'\bdeployments?\b|\bdeploy\b', command_base):
            resource_type = "deployments"
        elif re.search(r'\bservices?\b|\bsvc\b', command_base):
            resource_type = "services"
        elif re.search(r'\broutes?\b', command_base):
            resource_type = "routes"
        elif re.search(r'\bevents?\b', command_base):
            resource_type = "eventos"
        elif re.search(r'\bco\b|clusteroperators?', command_base):
            resource_type = "cluster operators"
        else:
            resource_type = "recursos"
    
    # Detectar oc logs
    elif 'oc logs' in command_base:
        action = "Exibir logs"
        resource_type = ""
    
    # Detectar outros comandos
    elif 'oc adm top' in command_base:
        action = "Exibir métricas de uso"
        if 'node' in command_base:
            resource_type = "de nodes"
        elif 'pod' in command_base:
            resource_type = "de pods"
        else:
            resource_type = ""
    
    else:
        action = "Filtrar saída"
        resource_type = ""
    
    # Criar descrição baseada no padrão encontrado
    filter_desc = None
    
    # Padrões específicos conhecidos
    pattern_lower = pattern_found.lower()
    
    # Padrões de recursos
    if pattern_lower in ['volumes', 'volume']:
        filter_desc = "Volumes"
    elif pattern_lower in ['containers', 'container']:
        filter_desc = "Containers"
    elif pattern_lower in ['events', 'event']:
        filter_desc = "Events"
    elif pattern_lower in ['conditions', 'condition']:
        filter_desc = "Conditions"
    elif pattern_lower in ['labels', 'label']:
        filter_desc = "Labels"
    elif pattern_lower in ['annotations', 'annotation']:
        filter_desc = "Annotations"
    elif pattern_lower in ['status']:
        filter_desc = "Status"
    elif pattern_lower in ['spec']:
        filter_desc = "Spec"
    elif pattern_lower in ['metadata']:
        filter_desc = "Metadata"
    elif pattern_lower in ['limits', 'limit']:
        filter_desc = "Limites de recursos"
    elif pattern_lower in ['requests', 'request']:
        filter_desc = "Requisições de recursos"
    elif pattern_lower in ['ready']:
        filter_desc = "estado Ready"
    elif pattern_lower in ['running']:
        filter_desc = "estado Running"
    elif pattern_lower in ['pending']:
        filter_desc = "estado Pending"
    elif pattern_lower in ['failed']:
        filter_desc = "estado Failed"
    elif pattern_lower in ['error']:
        filter_desc = "erros"
    elif pattern_lower in ['warning']:
        filter_desc = "warnings"
    elif pattern_lower in ['image', 'images']:
        filter_desc = "imagens"
    elif pattern_lower in ['port', 'ports']:
        filter_desc = "portas"
    elif pattern_lower in ['env', 'environment']:
        filter_desc = "variáveis de ambiente"
    elif pattern_lower in ['mount', 'mounts']:
        filter_desc = "montagens"
    elif pattern_lower in ['node']:
        filter_desc = "informações do node"
    elif pattern_lower in ['ip']:
        filter_desc = "endereços IP"
    elif pattern_lower in ['namespace', 'namespaces']:
        filter_desc = "namespaces"
    elif pattern_lower in ['age']:
        filter_desc = "idade/tempo de criação"
    elif pattern_lower in ['name', 'names']:
        filter_desc = "nomes"
    elif pattern_lower in ['type', 'types']:
        filter_desc = "tipos"
    elif pattern_lower in ['selector', 'selectors']:
        filter_desc = "seletores"
    elif pattern_lower in ['replicas', 'replica']:
        filter_desc = "réplicas"
    elif pattern_lower in ['available']:
        filter_desc = "estado Available"
    elif pattern_lower in ['degraded']:
        filter_desc = "estado Degraded"
    elif pattern_lower in ['progressing']:
        filter_desc = "estado Progressing"
    elif pattern_lower in ['version', 'versions']:
        filter_desc = "versões"
    elif pattern_lower in ['channel', 'channels']:
        filter_desc = "canais"
    elif pattern_lower in ['update', 'updates']:
        filter_desc = "atualizações"
    elif pattern_lower in ['upgrade', 'upgrades']:
        filter_desc = "upgrades"
    elif pattern_lower in ['certificate', 'certificates', 'cert']:
        filter_desc = "certificados"
    elif pattern_lower in ['secret', 'secrets']:
        filter_desc = "secrets"
    elif pattern_lower in ['configmap', 'configmaps']:
        filter_desc = "configmaps"
    elif pattern_lower in ['service', 'services', 'svc']:
        filter_desc = "services"
    elif pattern_lower in ['route', 'routes']:
        filter_desc = "routes"
    elif pattern_lower in ['endpoint', 'endpoints']:
        filter_desc = "endpoints"
    elif pattern_lower in ['ingress']:
        filter_desc = "ingress"
    elif pattern_lower in ['network', 'networking']:
        filter_desc = "configurações de rede"
    elif pattern_lower in ['storage']:
        filter_desc = "configurações de storage"
    elif pattern_lower in ['pvc', 'persistentvolumeclaim']:
        filter_desc = "PVCs"
    elif pattern_lower in ['pv', 'persistentvolume']:
        filter_desc = "PVs"
    elif pattern_lower in ['storageclass', 'sc']:
        filter_desc = "storage classes"
    elif pattern_lower in ['role', 'roles']:
        filter_desc = "roles"
    elif pattern_lower in ['rolebinding', 'rolebindings']:
        filter_desc = "rolebindings"
    elif pattern_lower in ['clusterrole', 'clusterroles']:
        filter_desc = "clusterroles"
    elif pattern_lower in ['clusterrolebinding', 'clusterrolebindings']:
        filter_desc = "clusterrolebindings"
    elif pattern_lower in ['serviceaccount', 'serviceaccounts', 'sa']:
        filter_desc = "service accounts"
    elif pattern_lower in ['user', 'users']:
        filter_desc = "usuários"
    elif pattern_lower in ['group', 'groups']:
        filter_desc = "grupos"
    elif pattern_lower in ['project', 'projects']:
        filter_desc = "projetos"
    elif pattern_lower in ['operator', 'operators']:
        filter_desc = "operators"
    elif pattern_lower in ['subscription', 'subscriptions']:
        filter_desc = "subscriptions"
    elif pattern_lower in ['csv', 'clusterserviceversion']:
        filter_desc = "ClusterServiceVersions"
    elif pattern_lower in ['installplan', 'installplans']:
        filter_desc = "install plans"
    elif pattern_lower in ['build', 'builds']:
        filter_desc = "builds"
    elif pattern_lower in ['buildconfig', 'buildconfigs', 'bc']:
        filter_desc = "buildconfigs"
    elif pattern_lower in ['imagestream', 'imagestreams', 'is']:
        filter_desc = "imagestreams"
    elif pattern_lower in ['job', 'jobs']:
        filter_desc = "jobs"
    elif pattern_lower in ['cronjob', 'cronjobs']:
        filter_desc = "cronjobs"
    elif pattern_lower in ['daemonset', 'daemonsets', 'ds']:
        filter_desc = "daemonsets"
    elif pattern_lower in ['statefulset', 'statefulsets', 'sts']:
        filter_desc = "statefulsets"
    elif pattern_lower in ['replicaset', 'replicasets', 'rs']:
        filter_desc = "replicasets"
    elif pattern_lower in ['replicationcontroller', 'rc']:
        filter_desc = "replication controllers"
    elif pattern_lower in ['hpa', 'horizontalpodautoscaler']:
        filter_desc = "horizontal pod autoscalers"
    elif pattern_lower in ['qos']:
        filter_desc = "QoS (Quality of Service)"
    elif pattern_lower in ['toleration', 'tolerations']:
        filter_desc = "tolerations"
    elif pattern_lower in ['affinity', 'affinities']:
        filter_desc = "afinidades"
    elif pattern_lower in ['taint', 'taints']:
        filter_desc = "taints"
    elif pattern_lower in ['capacity']:
        filter_desc = "capacidade"
    elif pattern_lower in ['allocatable']:
        filter_desc = "recursos alocáveis"
    elif pattern_lower in ['cpu']:
        filter_desc = "CPU"
    elif pattern_lower in ['memory', 'mem']:
        filter_desc = "memória"
    elif pattern_lower in ['disk']:
        filter_desc = "disco"
    elif pattern_lower in ['network']:
        filter_desc = "rede"
    else:
        # Capitalizar primeira letra do padrão se não for conhecido
        filter_desc = pattern_found.capitalize()
    
    # Construir a descrição final
    if action and resource_type and filter_desc:
        if action == "Listar":
            return f"{action} {resource_type} filtrando por {filter_desc}"
        else:
            return f"{action} {resource_type} filtrando por {filter_desc}"
    elif action and filter_desc:
        return f"{action} filtrando por {filter_desc}"
    elif filter_desc:
        return f"Filtrar saída por {filter_desc}"
    
    return None


def improve_grep_comment(comment: str, command: str) -> str:
    """
    Melhora um comentário baseado na análise do comando grep.
    
    Args:
        comment: Comentário original
        command: Comando completo
        
    Returns:
        Comentário melhorado ou original se não aplicável
    """
    # Se o comando não tem grep, retornar comentário original
    if 'grep' not in command.lower():
        return comment
    
    # Se o comentário já é específico (não genérico), retornar original
    generic_patterns = [
        r'^Exibir \w+ em formato (YAML|JSON)',
        r'^Listar \w+$',
        r'^Exibir detalhes completos do \w+$',
        r'^Ver \w+$',
        r'^Mostrar \w+$',
    ]
    
    is_generic = False
    for pattern in generic_patterns:
        if re.match(pattern, comment):
            is_generic = True
            break
    
    # Se já tem "filtrando por" no comentário, manter
    if 'filtrando por' in comment.lower():
        return comment
    
    # Analisar o grep
    improved = analyze_grep_pattern(command)
    
    if improved:
        return improved
    
    return comment


def process_markdown_file(filepath: Path, dry_run: bool = False) -> Tuple[int, int]:
    """
    Processa um arquivo markdown melhorando comentários de comandos com grep.
    
    Args:
        filepath: Caminho do arquivo
        dry_run: Se True, apenas simula as mudanças
        
    Returns:
        Tupla (total de comentários, comentários melhorados)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Padrão para encontrar blocos: **Comentário** seguido de ```bash ... ```
    # Captura: comentário (grupo 1), separador (grupo 2), código completo (grupo 3)
    pattern = r'(\*\*[^*]+\*\*)\n\n(```bash(?:\s+ignore-test)?)\n(.*?)\n```'
    
    comments_found = 0
    comments_improved = 0
    new_content = content
    
    def replace_comment(match):
        nonlocal comments_found, comments_improved
        
        comment_full = match.group(1)  # **Comentário**
        separator = match.group(2)      # ```bash ou ```bash ignore-test
        code = match.group(3)           # Código dentro do bloco
        
        comments_found += 1
        
        # Extrair apenas o texto do comentário (sem **)
        comment_text = comment_full.replace('**', '')
        
        # Pegar a primeira linha do comando (pode ter múltiplas linhas)
        command_lines = [line for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
        if not command_lines:
            return match.group(0)  # Sem comando, retornar original
        
        first_command = command_lines[0]
        
        # Tentar melhorar o comentário
        improved_comment = improve_grep_comment(comment_text, first_command)
        
        if improved_comment != comment_text:
            comments_improved += 1
            if dry_run:
                print(f"  {filepath.name}:")
                print(f"    - {comment_text}")
                print(f"    + {improved_comment}")
                print(f"    Comando: {first_command[:80]}...")
                print()
            
            # Retornar bloco com comentário melhorado
            return f"**{improved_comment}**\n\n{separator}\n{code}\n```"
        
        # Comentário não foi melhorado, retornar original
        return match.group(0)
    
    # Substituir todos os blocos
    new_content = re.sub(pattern, replace_comment, content, flags=re.DOTALL)
    
    # Salvar se houve mudanças e não é dry-run
    if not dry_run and new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return comments_found, comments_improved


def main():
    parser = argparse.ArgumentParser(
        description='Melhora comentários de comandos com grep em arquivos markdown.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Modo dry-run (visualizar mudanças)
  python3 scripts/improve-grep-comments.py --dry-run
  
  # Aplicar em arquivo específico
  python3 scripts/improve-grep-comments.py --file 04-pods-containers.md
  
  # Aplicar em todos os arquivos
  python3 scripts/improve-grep-comments.py
        """
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Apenas mostra o que seria alterado sem modificar arquivos')
    parser.add_argument('--file', type=str,
                        help='Processar apenas um arquivo específico')
    
    args = parser.parse_args()
    
    # Determinar quais arquivos processar
    if args.file:
        files = [Path(args.file)]
        if not files[0].exists():
            print(f"❌ Arquivo não encontrado: {args.file}")
            return 1
    else:
        # Processar todos os arquivos numerados .md
        files = sorted(Path('.').glob('[0-9][0-9]-*.md'))
    
    if not files:
        print("❌ Nenhum arquivo encontrado para processar")
        return 1
    
    print(f"{'🔍 Modo DRY-RUN - Nenhum arquivo será modificado' if args.dry_run else '✏️  Processando arquivos...'}")
    print(f"📁 {len(files)} arquivo(s) para processar\n")
    
    total_comments = 0
    total_improved = 0
    files_changed = 0
    
    for filepath in files:
        found, improved = process_markdown_file(filepath, args.dry_run)
        total_comments += found
        
        if improved > 0:
            files_changed += 1
            total_improved += improved
            if not args.dry_run:
                print(f"✅ {filepath.name}: {improved} comentário(s) melhorado(s)")
    
    print(f"\n{'─' * 60}")
    print(f"📊 Resumo:")
    print(f"  • Total de comentários encontrados: {total_comments}")
    print(f"  • Comentários melhorados: {total_improved}")
    print(f"  • Arquivos modificados: {files_changed}")
    
    if args.dry_run:
        print(f"\n💡 Execute novamente sem --dry-run para aplicar as mudanças")
    else:
        print(f"\n✨ Melhorias aplicadas com sucesso!")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
