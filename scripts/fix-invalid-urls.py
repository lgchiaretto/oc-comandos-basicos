#!/usr/bin/env python3
"""
Script para corrigir URLs inválidas identificadas pelo add-docs-section.py
"""

from typing import Dict, List, Tuple

# URLs inválidas identificadas e suas correções
URL_FIXES: Dict[str, str] = {
    # Applications - URL fragmentada não existe, usar URL principal
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/applications": 
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications",
    
    # Nodes - URLs fragmentadas não existem, usar URL principal
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/pods":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes",
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/containers":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes",
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/configmaps":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes",
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/secrets":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes",
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/viewing-system-event-information":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes",
    
    # Post-installation - URL fragmentada não existe, usar URL principal
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/post_installation_configuration":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/post-installation_configuration",
    
    # Storage - URL fragmentada não existe, usar URL principal
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage/persistent-storage":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage",
    
    # CI/CD - URL fragmentada não existe, usar URL principal
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cicd/builds":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cicd",
    
    # Images - URL fragmentada não existe, usar URL principal
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images/image-streams":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images",
    
    # Support - URL fragmentada não existe, usar URL principal
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support/remote-health-monitoring":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support",
    
    # Building applications - URL fragmentada não existe
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/troubleshooting":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications",
    
    # Operators - URL fragmentada não existe
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators/cluster-operators-reference":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators",
    
    # Updating - URL não existe, usar versão correta
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/updating":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/updating_clusters",
    
    # CLI Tools - URL fragmentada não existe
    "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/extending-the-openshift-cli":
        "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools",
}


def generate_corrected_docs_map() -> str:
    """Gera o código Python corrigido do DOCS_MAP."""
    
    from add_docs_section import DOCS_MAP
    
    output = []
    output.append("# Mapeamento corrigido de arquivo para links de documentação")
    output.append("DOCS_MAP: Dict[str, List[Tuple[str, str]]] = {")
    
    for filename, links in sorted(DOCS_MAP.items()):
        output.append(f'    "{filename}": [')
        
        for title, url in links:
            # Aplicar correção se a URL estiver na lista de fixes
            corrected_url = URL_FIXES.get(url, url)
            output.append(f'        ("{title}", "{corrected_url}"),')
        
        output.append("    ],")
    
    output.append("}")
    
    return '\n'.join(output)


def print_url_mapping_report():
    """Imprime relatório de correções."""
    print("=" * 80)
    print("RELATÓRIO DE CORREÇÕES DE URLS")
    print("=" * 80)
    print(f"\nTotal de URLs a corrigir: {len(URL_FIXES)}\n")
    
    for i, (old_url, new_url) in enumerate(URL_FIXES.items(), 1):
        print(f"{i}. URL Inválida:")
        print(f"   {old_url}")
        print(f"   ↓")
        print(f"   {new_url}")
        print()
    
    print("=" * 80)


def main():
    """Ponto de entrada principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Corrige URLs inválidas')
    parser.add_argument('--report', action='store_true',
                        help='Mostra relatório de correções')
    parser.add_argument('--generate', action='store_true',
                        help='Gera código Python corrigido')
    args = parser.parse_args()
    
    if args.report:
        print_url_mapping_report()
    
    if args.generate:
        print("\n" + "=" * 80)
        print("CÓDIGO PYTHON CORRIGIDO PARA add-docs-section.py")
        print("=" * 80)
        print("\nSubstitua o DOCS_MAP no arquivo add-docs-section.py pelo código abaixo:\n")
        print(generate_corrected_docs_map())
        print()
    
    if not args.report and not args.generate:
        # Default: mostrar relatório
        print_url_mapping_report()


if __name__ == "__main__":
    main()
