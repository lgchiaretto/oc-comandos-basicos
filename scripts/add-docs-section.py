#!/usr/bin/env python3
"""
Script para adicionar seção de Documentação Oficial do OpenShift 4.19
em cada arquivo markdown.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


# Mapeamento de arquivo para links de documentação relevantes
DOCS_MAP: Dict[str, List[Tuple[str, str]]] = {
    "01-autenticacao-configuracao.md": [
        ("CLI Tools", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools"),
        ("OpenShift CLI (oc)", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/openshift-cli-oc"),
        ("Authentication and Authorization", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization"),
    ],
    "02-projetos.md": [
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
        ("Working with projects", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/projects"),
    ],
    "03-aplicacoes.md": [
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
        ("Application development", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/applications"),
        ("Developer CLI (odo)", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/developer-cli-odo"),
    ],
    "04-pods-containers.md": [
        ("Nodes - Working with pods", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/pods"),
        ("Nodes - Working with containers", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/containers"),
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
    ],
    "05-deployments-scaling.md": [
        ("Building applications - Deployments", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/deployments"),
        ("Nodes - Working with pods", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/pods"),
        ("Post-installation configuration", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/post_installation_configuration"),
    ],
    "06-services-routes.md": [
        ("Networking - Configuring ingress", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/configuring-ingress"),
        ("Networking - Configuring routes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/configuring-routes"),
        ("Networking", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking"),
    ],
    "07-configmaps-secrets.md": [
        ("Nodes - ConfigMaps", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/configmaps"),
        ("Nodes - Secrets", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/secrets"),
        ("Security and compliance", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance"),
    ],
    "08-storage.md": [
        ("Storage", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage"),
        ("Storage - Persistent storage", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage/persistent-storage"),
        ("Storage - Dynamic provisioning", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage/dynamic-provisioning"),
    ],
    "09-builds-images.md": [
        ("CI/CD - Builds", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cicd/builds"),
        ("Images", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images"),
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
    ],
    "10-registry-imagens.md": [
        ("Registry - Integrated OpenShift image registry", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/registry"),
        ("Images - Managing images", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images"),
        ("Images - Image streams", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images/image-streams"),
    ],
    "11-monitoramento-logs.md": [
        ("Monitoring - Monitoring overview", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/monitoring"),
        ("Logging", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/logging"),
        ("Nodes - Viewing system event information", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/viewing-system-event-information"),
    ],
    "12-must-gather.md": [
        ("Support - Gathering data about your cluster", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support"),
        ("Support - Remote health monitoring", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support/remote-health-monitoring"),
    ],
    "13-troubleshooting-pods.md": [
        ("Support - Troubleshooting", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support"),
        ("Nodes - Working with pods", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/pods"),
        ("Building applications - Troubleshooting", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/troubleshooting"),
    ],
    "14-troubleshooting-rede.md": [
        ("Networking - Troubleshooting network issues", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking"),
        ("Support - Troubleshooting", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support"),
    ],
    "15-troubleshooting-storage.md": [
        ("Storage - Troubleshooting persistent storage", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage"),
        ("Support - Troubleshooting", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support"),
    ],
    "16-seguranca-rbac.md": [
        ("Authentication and authorization", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization"),
        ("Security and compliance - Managing security context constraints", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance"),
        ("Post-installation configuration - Configuring RBAC", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/post_installation_configuration"),
    ],
    "17-cluster-operators.md": [
        ("Operators - Understanding Operators", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators"),
        ("Operators - Cluster Operators reference", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators/cluster-operators-reference"),
        ("Post-installation configuration", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/post_installation_configuration"),
    ],
    "18-nodes-machine.md": [
        ("Machine management", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/machine_management"),
        ("Nodes - Working with nodes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
        ("Post-installation configuration - Configuring nodes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/post_installation_configuration"),
    ],
    "19-certificados-csr.md": [
        ("Security and compliance - Certificate management", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance"),
        ("Authentication and authorization", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization"),
    ],
    "20-cluster-networking.md": [
        ("Networking - Understanding networking", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking"),
        ("Networking - Multiple networks", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/multiple-networks"),
        ("Post-installation configuration - Cluster capabilities", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/post_installation_configuration"),
    ],
    "21-cluster-version-updates.md": [
        ("Updating clusters", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/updating"),
        ("Post-installation configuration", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/post_installation_configuration"),
    ],
    "22-etcd-backup.md": [
        ("Backup and restore - Backing up etcd", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/backup_and_restore"),
        ("Post-installation configuration", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/post_installation_configuration"),
    ],
    "23-comandos-customizados.md": [
        ("CLI Tools - Using the OpenShift CLI", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools"),
        ("CLI Tools - Extending the OpenShift CLI", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/extending-the-openshift-cli"),
    ],
    "24-field-selectors.md": [
        ("CLI Tools - OpenShift CLI (oc)", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/openshift-cli-oc"),
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
    ],
    "25-output-formatacao.md": [
        ("CLI Tools - OpenShift CLI (oc)", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/openshift-cli-oc"),
        ("CLI Tools - Usage of oc and kubectl", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools"),
    ],
    "26-templates-manifests.md": [
        ("Images - Using templates", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images"),
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
    ],
    "27-backup-disaster-recovery.md": [
        ("Backup and restore", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/backup_and_restore"),
        ("Post-installation configuration", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/post_installation_configuration"),
    ],
    "28-patch-edit.md": [
        ("CLI Tools - OpenShift CLI (oc)", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/openshift-cli-oc"),
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
    ],
    "29-jobs-cronjobs.md": [
        ("Nodes - Working with jobs and cron jobs", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
    ],
    "30-operators-operandos.md": [
        ("Operators - Understanding Operators", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators"),
        ("Operators - Administrator tasks", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators/administrator-tasks"),
        ("Operators - User tasks", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators/user-tasks"),
    ],
}


def generate_docs_section(links: List[Tuple[str, str]]) -> str:
    """Gera a seção de documentação oficial com links que abrem em nova aba."""
    lines = [
        "## 📚 Documentação Oficial",
        "",
        "Consulte a documentação oficial do OpenShift 4.19 da Red Hat:",
        ""
    ]
    
    for title, url in links:
        # Usa HTML para forçar abertura em nova aba
        lines.append(f'- <a href="{url}" target="_blank">{title}</a>')
    
    lines.append("")
    return '\n'.join(lines)


def add_docs_section(file_path: Path, force: bool = False) -> bool:
    """Adiciona a seção de documentação oficial no arquivo.
    
    Insere a seção antes da seção de Navegação.
    Retorna True se houve modificação.
    """
    filename = file_path.name
    
    if filename not in DOCS_MAP:
        print(f"  ⚠️  Sem mapeamento de documentação para {filename}")
        return False
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ❌ ERRO ao ler {filename}: {e}")
        return False
    
    # Verificar se já tem a seção
    if "## 📚 Documentação Oficial" in content and not force:
        print(f"  ℹ️  Seção de documentação já existe (use --force para sobrescrever)")
        return False
    
    # Se force=True, remove seção existente primeiro
    if force and "## 📚 Documentação Oficial" in content:
        # Remove seção existente e separadores extras
        pattern = r'---\s*\n\s*---\s*\n\s*---\s*\n\s*## 📚 Documentação Oficial.*?(?=\n---\s*\n\s*## 📖 Navegação|\Z)'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        # Também limpa pattern simples
        pattern = r'## 📚 Documentação Oficial.*?(?=\n---\s*\n\s*## 📖 Navegação|\Z)'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Gerar nova seção
    docs_section = generate_docs_section(DOCS_MAP[filename])
    
    # Inserir antes da seção de Navegação
    nav_pattern = r'(---\s*\n\s*## 📖 Navegação)'
    
    if re.search(nav_pattern, content):
        new_content = re.sub(
            nav_pattern,
            docs_section + '---\n\n\\1',
            content,
            count=1
        )
    else:
        # Se não tem navegação, adicionar antes da última atualização
        update_pattern = r'(\*\*Última atualização\*\*)'
        if re.search(update_pattern, content):
            new_content = re.sub(
                update_pattern,
                docs_section + '\n---\n\n\\1',
                content,
                count=1
            )
        else:
            # Como último recurso, adiciona no final
            new_content = content.rstrip() + '\n\n---\n\n' + docs_section
    
    if new_content == content:
        print(f"  ❌ Não foi possível adicionar seção")
        return False
    
    # Salvar
    file_path.write_text(new_content, encoding='utf-8')
    print(f"  ✓ Seção de documentação adicionada ({len(DOCS_MAP[filename])} links)")
    return True


def main():
    """Ponto de entrada principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Adiciona seção de documentação oficial')
    parser.add_argument('-f', '--force', action='store_true', 
                        help='Sobrescreve seção existente')
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    
    print("Adicionar Seções de Documentação Oficial")
    print("=" * 60)
    
    # Encontrar arquivos markdown numerados
    md_files = []
    for i in range(1, 31):
        matches = list(base_dir.glob(f"{i:02d}-*.md"))
        if matches:
            md_files.extend(matches)
    
    md_files = sorted(md_files)
    print(f"\n{len(md_files)} arquivos encontrados\n")
    
    added_count = 0
    
    for md_file in md_files:
        print(f"📄 {md_file.name}")
        if add_docs_section(md_file, args.force):
            added_count += 1
        print()
    
    print("=" * 60)
    print(f"✅ Concluído! {added_count} seções adicionadas/atualizadas")


if __name__ == "__main__":
    main()
