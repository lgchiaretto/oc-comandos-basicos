#!/usr/bin/env python3
"""
Script para adicionar seção de Documentação Oficial do OpenShift 4.19
em cada arquivo markdown.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


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
        ("Developer CLI (odo)", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/developer-cli-odo"),
        ("Deployments", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/deployments"),
        ("Images - Using templates", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images"),
    ],
    "04-pods-containers.md": [
        ("Nodes - Working with pods", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/working-with-pods"),
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
        ("Nodes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
    ],
    "05-deployments-scaling.md": [
        ("Building applications - Deployments", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/deployments"),
        ("Nodes - Autoscaling", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
        ("Nodes - Managing pods", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
    ],
    "06-services-routes.md": [
        ("Networking - Configuring ingress", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/configuring-ingress"),
        ("Networking - Configuring routes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/configuring-routes"),
        ("Networking - Understanding Services", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/understanding-networking"),
        ("Secured routes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/configuring-routes#nw-ingress-creating-a-route-via-an-ingress_route-configuration"),
    ],
    "07-configmaps-secrets.md": [
        ("Nodes - ConfigMaps and Secrets", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
        ("Nodes - Working with pods", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/working-with-pods"),
        ("Security and compliance", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance"),
    ],
    "08-storage.md": [
        ("Storage", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage"),
        ("Storage - Dynamic provisioning", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage/dynamic-provisioning"),
        ("Understanding persistent storage", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage/understanding-persistent-storage"),
        ("Expanding persistent volumes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage/expanding-persistent-volumes"),
    ],
    "09-builds-images.md": [
        ("Building applications - Builds", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
        ("Images - Managing images", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images"),
        ("Building applications - Build configuration", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
        ("Images - ImageStreams", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images"),
    ],
    "10-registry-imagens.md": [
        ("Registry - Integrated OpenShift image registry", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/registry"),
        ("Images - Managing images", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images"),
        ("Image Registry Operator", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/registry/configuring-registry-operator"),
        ("Pruning objects to reclaim resources", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
    ],
    "11-monitoramento-logs.md": [
        ("Monitoring - Monitoring overview", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/monitoring"),
        ("Logging", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/logging"),
        ("Nodes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
    ],
    "12-must-gather.md": [
        ("Support - Gathering data about your cluster", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support"),
    ],
    "13-troubleshooting-pods.md": [
        ("Support - Troubleshooting", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support"),
        ("Nodes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
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
        ("Security and compliance - Security Context Constraints", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance"),
        ("RBAC - Using RBAC to define and apply permissions", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization/using-rbac"),
        ("Service Accounts", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization/understanding-and-creating-service-accounts"),
    ],
    "17-cluster-operators.md": [
        ("Operators - Understanding Operators", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators"),
        ("Operators - Cluster Operators", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators"),
        ("Operator Lifecycle Manager", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators"),
        ("Post-installation configuration", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration"),
    ],
    "18-nodes-machine.md": [
        ("Machine management", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/machine_management"),
        ("Nodes - Working with nodes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
        ("Post-installation configuration", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration"),
    ],
    "19-certificados-csr.md": [
        ("Security and compliance - Certificate management", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance"),
        ("Authentication and authorization", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization"),
    ],
    "20-cluster-networking.md": [
        ("Networking - Understanding networking", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking"),
        ("Networking - Multiple networks", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/multiple-networks"),
        ("Post-installation configuration", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration"),
    ],
    "21-cluster-version-updates.md": [
        ("Updating clusters", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/updating_clusters"),
        ("Post-installation configuration", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration"),
    ],
    "22-etcd-backup.md": [
        ("Backup and restore - Backing up etcd", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/backup_and_restore"),
        ("Post-installation configuration", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration"),
    ],
    "23-comandos-customizados.md": [
        ("CLI Tools - Using the OpenShift CLI", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools"),
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
        ("Post-installation configuration", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration"),
    ],
    "28-patch-edit.md": [
        ("CLI Tools - OpenShift CLI (oc)", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/openshift-cli-oc"),
        ("Building applications", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
    ],
    "29-jobs-cronjobs.md": [
        ("Nodes - Working with jobs", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
        ("Building applications - Jobs and CronJobs", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications"),
        ("Nodes", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes"),
    ],
    "30-operators-operandos.md": [
        ("Operators - Understanding Operators", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators"),
        ("Operators - Administrator tasks", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators/administrator-tasks"),
        ("Operators - User tasks", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators/user-tasks"),
        ("Operator Lifecycle Manager", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators"),
        ("Custom Resources", "https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators"),
    ],
}


def validate_url(url: str, timeout: int = 10) -> Tuple[bool, str]:
    """Valida se uma URL está acessível.
    
    Retorna (sucesso, mensagem)
    """
    try:
        # Criar request com headers para evitar bloqueios
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        req = Request(url, headers=headers)
        
        # Tenta abrir a URL
        with urlopen(req, timeout=timeout) as response:
            status = response.status
            if status == 200:
                return True, f"OK (200)"
            else:
                return False, f"Status {status}"
    
    except HTTPError as e:
        return False, f"HTTP Error {e.code}: {e.reason}"
    except URLError as e:
        return False, f"URL Error: {e.reason}"
    except Exception as e:
        return False, f"Erro: {str(e)}"


def validate_all_urls(docs_map: Dict[str, List[Tuple[str, str]]], 
                     verbose: bool = False,
                     max_workers: int = 10) -> Dict[str, List[Tuple[str, str, bool, str]]]:
    """Valida todas as URLs no mapeamento usando paralelização.
    
    Args:
        docs_map: Dicionário com mapeamento de arquivos para URLs
        verbose: Se True, mostra detalhes de cada validação
        max_workers: Número de threads paralelas (padrão: 10)
    
    Retorna dict: filename -> [(title, url, valid, message)]
    """
    # Preparar lista de todas as URLs para validar
    url_list = []
    for filename, links in sorted(docs_map.items()):
        for title, url in links:
            url_list.append((filename, title, url))
    
    total_urls = len(url_list)
    completed = 0
    results_dict = {filename: [] for filename in docs_map.keys()}
    
    print(f"\nValidando {total_urls} URLs (paralelizando {max_workers} por vez)...")
    print("=" * 60)
    
    # Usar ThreadPoolExecutor para paralelizar as validações
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submeter todas as tarefas
        future_to_url = {
            executor.submit(validate_url, url): (filename, title, url)
            for filename, title, url in url_list
        }
        
        # Processar resultados conforme completam
        for future in as_completed(future_to_url):
            filename, title, url = future_to_url[future]
            completed += 1
            
            try:
                valid, message = future.result()
                results_dict[filename].append((title, url, valid, message))
                
                if verbose:
                    print(f"[{completed}/{total_urls}] {url}")
                    if valid:
                        print(f"  ✅ {message}")
                    else:
                        print(f"  ❌ {message}")
                else:
                    # Mostrar progresso compacto
                    print(f"[{completed}/{total_urls}] Validando URLs...", end='\r')
                
                # Mostrar erros imediatamente
                if not valid and not verbose:
                    print(f"\n  ❌ ERRO: {title}")
                    print(f"     Arquivo: {filename}")
                    print(f"     URL: {url}")
                    print(f"     Razão: {message}")
                    print(f"[{completed}/{total_urls}] Validando URLs...", end='\r')
                    
            except Exception as e:
                print(f"\n  ❌ EXCEÇÃO ao validar {url}: {str(e)}")
                results_dict[filename].append((title, url, False, f"Exceção: {str(e)}"))
    
    print("\n" + "=" * 60)
    return results_dict


def print_validation_summary(results: Dict[str, List[Tuple[str, str, bool, str]]]):
    """Imprime sumário da validação."""
    total = 0
    valid = 0
    invalid = 0
    errors_by_file = {}
    
    for filename, url_results in results.items():
        file_errors = []
        for title, url, is_valid, message in url_results:
            total += 1
            if is_valid:
                valid += 1
            else:
                invalid += 1
                file_errors.append((title, url, message))
        
        if file_errors:
            errors_by_file[filename] = file_errors
    
    print("\n" + "=" * 60)
    print("SUMÁRIO DA VALIDAÇÃO")
    print("=" * 60)
    print(f"Total de URLs: {total}")
    print(f"✅ Válidas: {valid}")
    print(f"❌ Inválidas: {invalid}")
    
    if errors_by_file:
        print("\n" + "=" * 60)
        print("URLS COM PROBLEMAS")
        print("=" * 60)
        
        for filename, errors in sorted(errors_by_file.items()):
            print(f"\n{filename}:")
            for title, url, message in errors:
                print(f"  ❌ {title}")
                print(f"     URL: {url}")
                print(f"     Erro: {message}")
    
    print("\n" + "=" * 60)
    
    return invalid == 0


def generate_docs_section(links: List[Tuple[str, str]]) -> str:
    """Gera a seção de documentação oficial com links que abrem em nova aba."""
    lines = [
        "## Documentação Oficial",
        "",
        "Consulte a documentação oficial do OpenShift 4.19 da Red Hat:",
        ""
    ]
    
    for title, url in links:
        # Usa HTML para forçar abertura em nova aba
        lines.append(f'- <a href="{url}">{title}</a>')
    
    lines.append("")
    return '\n'.join(lines)


def add_docs_section(file_path: Path, force: bool = False) -> bool:
    """Adiciona a seção de documentação oficial no arquivo.
    
    Insere a seção antes da seção de Navegação.
    Retorna True se houve modificação.
    """
    filename = file_path.name
    
    if filename not in DOCS_MAP:
        print(f"  Sem mapeamento de documentação para {filename}")
        return False
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ERRO ao ler {filename}: {e}")
        return False
    
    # Verificar se já tem a seção
    if "## Documentação Oficial" in content and not force:
        print(f"  Seção de documentação já existe (use --force para sobrescrever)")
        return False
    
    # Se force=True, remove seção existente primeiro
    if force and "## Documentação Oficial" in content:
        # Remove seção existente e separadores extras
        pattern = r'---\s*\n\s*---\s*\n\s*---\s*\n\s*## Documentação Oficial.*?(?=\n---\s*\n\s*## Navegação|\Z)'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        # Também limpa pattern simples
        pattern = r'## Documentação Oficial.*?(?=\n---\s*\n\s*## Navegação|\Z)'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Gerar nova seção
    docs_section = generate_docs_section(DOCS_MAP[filename])
    
    # Inserir antes da seção de Navegação
    nav_pattern = r'(---\s*\n\s*## Navegação)'
    
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
        print(f"  Não foi possível adicionar seção")
        return False
    
    # Salvar
    file_path.write_text(new_content, encoding='utf-8')
    print(f"  Seção de documentação adicionada ({len(DOCS_MAP[filename])} links)")
    return True


def main():
    """Ponto de entrada principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Adiciona seção de documentação oficial')
    parser.add_argument('-f', '--force', action='store_true', 
                        help='Sobrescreve seção existente')
    parser.add_argument('--validate-only', action='store_true',
                        help='Apenas valida URLs sem modificar arquivos')
    parser.add_argument('--skip-validation', action='store_true',
                        help='Pula validação de URLs (não recomendado)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Mostra detalhes de cada validação')
    parser.add_argument('--workers', type=int, default=10,
                        help='Número de threads paralelas para validação (padrão: 10)')
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    
    print("Adicionar Seções de Documentação Oficial")
    print("=" * 60)
    
    # Validar URLs primeiro (a menos que seja pulado)
    if not args.skip_validation:
        validation_results = validate_all_urls(DOCS_MAP, verbose=args.verbose, max_workers=args.workers)
        all_valid = print_validation_summary(validation_results)
        
        if not all_valid:
            print("\n⚠️  AVISO: Algumas URLs estão inválidas!")
            print("Verifique os links acima e corrija-os no arquivo.")
            
            if not args.validate_only:
                response = input("\nDeseja continuar mesmo assim? (s/N): ").strip().lower()
                if response not in ['s', 'sim', 'y', 'yes']:
                    print("Operação cancelada.")
                    sys.exit(1)
        else:
            print("\n✅ Todas as URLs foram validadas com sucesso!")
        
        # Se apenas validação, sair aqui
        if args.validate_only:
            sys.exit(0 if all_valid else 1)
    
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
        print(f"{md_file.name}")
        if add_docs_section(md_file, args.force):
            added_count += 1
        print()
    
    print("=" * 60)
    print(f"Concluído! {added_count} seções adicionadas/atualizadas")


if __name__ == "__main__":
    main()
