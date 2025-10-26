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
    ],
    "02-projetos.md": [
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
    ],
    "03-aplicacoes.md": [
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
        ("Application development", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/applications"),
    ],
    "04-pods-containers.md": [
        ("Nodes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
        ("Working with pods", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/pods"),
    ],
    "05-deployments-scaling.md": [
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
        ("Nodes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
    ],
    "06-services-routes.md": [
        ("Networking", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking"),
    ],
    "07-configmaps-secrets.md": [
        ("Nodes - ConfigMaps and Secrets", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
    ],
    "08-storage.md": [
        ("Storage", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage"),
    ],
    "09-builds-images.md": [
        ("CI/CD", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cicd"),
        ("Builds", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cicd/builds"),
    ],
    "10-registry-imagens.md": [
        ("Registry", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/registry"),
        ("Images", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images"),
    ],
    "11-monitoramento-logs.md": [
        ("Monitoring", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/monitoring"),
        ("Logging", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/logging"),
    ],
    "12-must-gather.md": [
        ("Support", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support"),
    ],
    "13-troubleshooting-pods.md": [
        ("Support", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support"),
        ("Nodes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
    ],
    "14-troubleshooting-rede.md": [
        ("Networking", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking"),
    ],
    "15-troubleshooting-storage.md": [
        ("Storage", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage"),
    ],
    "16-seguranca-rbac.md": [
        ("Authentication and authorization", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization"),
    ],
    "17-cluster-operators.md": [
        ("Operators", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators"),
    ],
    "18-nodes-machine.md": [
        ("Machine management", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/machine_management"),
        ("Nodes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
    ],
    "19-certificados-csr.md": [
        ("Security and compliance", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance"),
    ],
    "20-cluster-networking.md": [
        ("Networking", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking"),
    ],
    "21-cluster-version-updates.md": [
        ("Updating clusters", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/updating"),
    ],
    "22-etcd-backup.md": [
        ("Backup and restore", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/backup_and_restore"),
    ],
    "23-comandos-customizados.md": [
        ("CLI Tools", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools"),
    ],
    "24-field-selectors.md": [
        ("CLI Tools", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools"),
    ],
    "25-output-formatacao.md": [
        ("CLI Tools", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools"),
    ],
    "26-templates-manifests.md": [
        ("Images", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images"),
    ],
    "27-backup-disaster-recovery.md": [
        ("Backup and restore", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/backup_and_restore"),
    ],
    "28-patch-edit.md": [
        ("CLI Tools", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools"),
    ],
    "29-jobs-cronjobs.md": [
        ("Nodes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
    ],
    "30-operators-operandos.md": [
        ("Operators", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators"),
    ],
}


def generate_docs_section(links: List[Tuple[str, str]]) -> str:
    """Gera a seção de documentação oficial."""
    lines = [
        "## 📚 Documentação Oficial",
        "",
        "Consulte a documentação oficial do OpenShift 4.19 da Red Hat:",
        ""
    ]
    
    for title, url in links:
        lines.append(f"- [{title}]({url})")
    
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
        # Remove seção existente
        pattern = r'## 📚 Documentação Oficial.*?(?=\n---|\n##|\Z)'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Gerar nova seção
    docs_section = generate_docs_section(DOCS_MAP[filename])
    
    # Inserir antes da seção de Navegação
    nav_pattern = r'(## 📖 Navegação)'
    
    if re.search(nav_pattern, content):
        new_content = re.sub(
            nav_pattern,
            docs_section + '\n---\n\n\\1',
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
