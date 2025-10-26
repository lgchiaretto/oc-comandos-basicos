#!/usr/bin/env python3
"""
Script para adicionar exemplos com placeholders em comandos oc nos arquivos markdown.
Autor: GitHub Copilot
Data: 2025-10-22
"""

import re
import os
import sys
from pathlib import Path

def extract_placeholder_pattern(command):
    """
    Extrai um padrão com placeholders de um comando oc concreto.
    
    Exemplos:
    - "oc describe istag s2i-chiaretto:latest" -> "oc describe istag <istag-name>:<tag>"
    - "oc get pod my-app-1-abc123" -> "oc get pod <pod-name>"
    - "oc delete project test-project" -> "oc delete project <project-name>"
    """
    
    # Remove comentários inline
    cmd = re.sub(r'\s*#.*$', '', command).strip()
    
    # Casos especiais: comandos sem argumentos específicos
    no_placeholder_patterns = [
        r'^oc\s+whoami\s*$',
        r'^oc\s+projects\s*$',
        r'^oc\s+get\s+\w+\s*$',  # oc get pods, oc get all, etc
        r'^oc\s+get\s+\w+\s+-[A-Za-z]',  # oc get pods -A
        r'^oc\s+get\s+\w+\s+-A',
        r'^oc\s+api-resources\s*',
        r'^oc\s+api-versions\s*',
        r'^oc\s+config\s+view\s*',
        r'^oc\s+status\s*$',
        r'^oc\s+registry\s+login\s*$',
        r'^oc\s+cluster-info\s*$',
        r'^oc\s+version\s*$',
    ]
    
    for pattern in no_placeholder_patterns:
        if re.match(pattern, cmd):
            return None
    
    # Já é um placeholder - não processar
    if '<' in cmd and '>' in cmd:
        return None
    
    # Tem variáveis de ambiente ou backticks - não processar
    if '$' in cmd or '`' in cmd:
        return None
    
    # Padrões de substituição
    replacements = [
        # ImageStreamTag name:tag
        (r'(istag\s+)[a-zA-Z0-9][-a-zA-Z0-9]*:[a-zA-Z0-9][-a-zA-Z0-9\.]*', r'\1<istag-name>:<tag>'),
        # ImageStream:tag
        (r'(is\s+)[a-zA-Z0-9][-a-zA-Z0-9]*:[a-zA-Z0-9][-a-zA-Z0-9\.]*', r'\1<imagestream-name>:<tag>'),
        # Pod names with generated suffixes (pod-name-xxx-yyy)
        (r'(pod\s+)[a-zA-Z0-9][-a-zA-Z0-9]*-[a-zA-Z0-9]+-[a-zA-Z0-9]+\b', r'\1<pod-name>'),
        # Deployment/ReplicaSet names with hash (name-xxx)
        (r'(deploy(?:ment)?\s+)[a-zA-Z0-9][-a-zA-Z0-9]*-[a-zA-Z0-9]+\b', r'\1<deployment-name>'),
        (r'(rs\s+)[a-zA-Z0-9][-a-zA-Z0-9]*-[a-zA-Z0-9]+\b', r'\1<replicaset-name>'),
        # Service names
        (r'(service/)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<service-name>'),
        (r'(svc\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<service-name>'),
        (r'(service\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<service-name>'),
        # Route names
        (r'(route\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<route-name>'),
        (r'(route/)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<route-name>'),
        # ConfigMap names
        (r'(configmap\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<configmap-name>'),
        (r'(cm\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<configmap-name>'),
        # Secret names
        (r'(secret\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<secret-name>'),
        # PVC names
        (r'(pvc\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1test-app'),
        # PV names
        (r'(pv\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<pv-name>'),
        # Node names
        (r'(node\s+)[a-zA-Z0-9][-a-zA-Z0-9\.]*\b', r'\1<node-name>'),
        (r'(node/)[a-zA-Z0-9][-a-zA-Z0-9\.]*\b', r'\1<node-name>'),
        # Namespace/Project names (mais genérico)
        (r'(namespace\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<namespace-name>'),
        (r'(project\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<project-name>'),
        (r'(-n\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<namespace>'),
        (r'(--namespace\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<namespace>'),
        # BuildConfig
        (r'(bc\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<buildconfig-name>'),
        (r'(buildconfig\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<buildconfig-name>'),
        # Build
        (r'(build\s+)[a-zA-Z0-9][-a-zA-Z0-9]*-\d+\b', r'\1<build-name>'),
        # ImageStream
        (r'(is\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<imagestream-name>'),
        (r'(imagestream\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<imagestream-name>'),
        # DeploymentConfig
        (r'(dc\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<deploymentconfig-name>'),
        # Job
        (r'(job\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<job-name>'),
        # CronJob
        (r'(cronjob\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<cronjob-name>'),
        (r'(cj\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<cronjob-name>'),
        # ServiceAccount
        (r'(serviceaccount\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<serviceaccount-name>'),
        (r'(sa\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<serviceaccount-name>'),
        # Role/RoleBinding
        (r'(role\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<role-name>'),
        (r'(rolebinding\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<rolebinding-name>'),
        # ClusterRole/ClusterRoleBinding
        (r'(clusterrole\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<clusterrole-name>'),
        (r'(clusterrolebinding\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<clusterrolebinding-name>'),
        # User/Group
        (r'(user\s+)[a-zA-Z0-9][-a-zA-Z0-9@\.]*\b', r'\1<username>'),
        (r'(group\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<group-name>'),
        # Container name in -c flag
        (r'(-c\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<container-name>'),
        (r'(--container\s+)[a-zA-Z0-9][-a-zA-Z0-9]*\b', r'\1<container-name>'),
        # Generic resource name (fallback - deve ser o último)
        (r'(oc\s+\w+\s+\w+\s+)([a-zA-Z0-9][-a-zA-Z0-9]*)\b(?!\s*-)', r'\1<resource-name>'),
    ]
    
    result = cmd
    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result)
    
    # Se nada mudou, não há placeholder a adicionar
    if result == cmd:
        return None
    
    return result


def process_markdown_file(filepath):
    """
    Processa um arquivo markdown adicionando placeholders aos comandos oc.
    """
    print(f"Processando: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    changes_made = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Detecta início de bloco bash (com ou sem ignore-test)
        if line.strip().startswith('```bash'):
            i += 1
            # Processa linhas dentro do bloco
            while i < len(lines) and not lines[i].strip().startswith('```'):
                current_line = lines[i]
                stripped = current_line.strip()
                
                # É um comando oc (não é comentário e começa com oc)
                if stripped.startswith('oc ') and not stripped.startswith('#'):
                    # Verifica se a linha anterior já é um placeholder
                    if i > 0 and new_lines:
                        prev_line = new_lines[-1].strip()
                        if prev_line.startswith('# oc ') and '<' in prev_line and '>' in prev_line:
                            # Já tem placeholder, pula
                            new_lines.append(current_line)
                            i += 1
                            continue
                    
                    # Tenta extrair placeholder
                    placeholder = extract_placeholder_pattern(stripped)
                    if placeholder:
                        # Adiciona linha de comentário com placeholder
                        indent = len(current_line) - len(current_line.lstrip())
                        placeholder_line = ' ' * indent + '# ' + placeholder + '\n'
                        new_lines.append(placeholder_line)
                        changes_made += 1
                
                new_lines.append(current_line)
                i += 1
            
            # Adiciona linha de fechamento do bloco ```
            if i < len(lines):
                new_lines.append(lines[i])
        
        i += 1
    
    # Escreve arquivo apenas se houve mudanças
    if changes_made > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"  ✅ {changes_made} placeholders adicionados")
        return changes_made
    else:
        print(f"  ℹ️  Nenhuma mudança necessária")
        return 0


def main():
    """
    Processa todos os arquivos markdown numerados (01-30).
    """
    base_dir = Path(__file__).parent.parent
    
    # Lista de arquivos markdown numerados
    markdown_files = sorted([
        f for f in base_dir.glob('*.md')
        if re.match(r'^\d{2}-.*\.md$', f.name)
    ])
    
    if not markdown_files:
        print("❌ Nenhum arquivo markdown encontrado!")
        return 1
    
    print(f"📝 Encontrados {len(markdown_files)} arquivos markdown\n")
    
    total_changes = 0
    for md_file in markdown_files:
        changes = process_markdown_file(md_file)
        total_changes += changes
    
    print(f"\n✅ Processamento concluído!")
    print(f"📊 Total de placeholders adicionados: {total_changes}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
