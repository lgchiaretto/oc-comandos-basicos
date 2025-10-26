#!/usr/bin/env python3
"""
Script para remover comandos duplicados dos arquivos markdown.
Usa regras de prioridade baseadas no contexto do arquivo.
"""

import re
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict


# Mapeamento de prioridade: qual arquivo deve MANTER o comando
# Baseado no contexto mais apropriado para cada tipo de comando
PRIORITY_MAP = {
    # Comandos básicos de pods
    "oc get pods": "04-pods-containers.md",
    "oc get pods -A": "04-pods-containers.md",
    "oc describe pod": "04-pods-containers.md",
    "oc logs": "11-monitoramento-logs.md",
    "oc rsh": "04-pods-containers.md",
    "oc exec": "04-pods-containers.md",
    "oc debug pod": "13-troubleshooting-pods.md",
    
    # Comandos de rede
    "oc get svc": "06-services-routes.md",
    "oc get routes": "06-services-routes.md",
    "oc get endpoints": "06-services-routes.md",
    "oc get networkpolicy": "20-cluster-networking.md",
    "oc get ingresscontroller": "20-cluster-networking.md",
    
    # Storage
    "oc get pvc": "08-storage.md",
    "oc get pv": "08-storage.md",
    "oc get sc": "08-storage.md",
    "oc describe pvc": "08-storage.md",
    
    # Cluster operators
    "oc get co": "17-cluster-operators.md",
    "oc get clusteroperators": "17-cluster-operators.md",
    
    # Nodes
    "oc get nodes": "18-nodes-machine.md",
    "oc debug node": "18-nodes-machine.md",
    "oc adm top nodes": "18-nodes-machine.md",
    
    # RBAC
    "oc get sa": "16-seguranca-rbac.md",
    "oc adm policy": "16-seguranca-rbac.md",
    
    # Operators
    "oc get csv": "30-operators-operandos.md",
    "oc get catalogsources": "30-operators-operandos.md",
    
    # Updates
    "oc get clusterversion": "21-cluster-version-updates.md",
    
    # ConfigMaps/Secrets
    "oc get configmap": "07-configmaps-secrets.md",
    "oc get secret": "07-configmaps-secrets.md",
    
    # Images/Builds
    "oc get is": "10-registry-imagens.md",
    
    # Templates
    "oc get templates": "26-templates-manifests.md",
    
    # Events
    "oc get events": "11-monitoramento-logs.md",
    
    # Must-gather
    "oc adm must-gather": "12-must-gather.md",
}


def get_priority_file(command: str) -> str:
    """Retorna o arquivo de maior prioridade para manter o comando."""
    # Procura por match exato ou parcial
    for key, file in PRIORITY_MAP.items():
        if key in command:
            return file
    
    # Se não tem prioridade definida, usa heurística
    # Troubleshooting tem baixa prioridade (mantém em outros lugares)
    # Comandos customizados/field-selectors são exemplos (mantém)
    
    if "troubleshooting" in command:
        return ""  # Remove de troubleshooting
    
    return ""  # Sem prioridade clara


def main():
    """Ponto de entrada principal."""
    print("Removedor de Comandos Duplicados")
    print("=" * 80)
    print("\nEste script é ANÁLISE APENAS.")
    print("Para implementar remoções, revise manualmente o relatório CSV.\n")
    print("=" * 80)
    
    base_dir = Path(__file__).parent.parent
    csv_file = base_dir / "duplicates-report.csv"
    
    if not csv_file.exists():
        print("\n❌ Arquivo duplicates-report.csv não encontrado.")
        print("Execute primeiro: python3 scripts/find-duplicates.py")
        return
    
    print(f"\n📄 Analisando: {csv_file}\n")
    
    # Lê o CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()[1:]  # Skip header
    
    # Análise de ações sugeridas
    actions = defaultdict(int)
    consolidar = []
    
    for line in lines:
        # Parse CSV line
        match = re.match(r'"([^"]+)","([^"]+)",(\d+),(\w+)', line)
        if not match:
            continue
        
        cmd, files_str, count, action = match.groups()
        actions[action] += 1
        
        if action == "CONSOLIDAR":
            files = [f.strip() for f in files_str.split(';')]
            priority = get_priority_file(cmd)
            consolidar.append((cmd, files, priority))
    
    print("\n📊 Resumo de Ações:")
    print("-" * 80)
    for action, count in sorted(actions.items()):
        print(f"  {action}: {count} comandos")
    
    print(f"\n\n🎯 Comandos que devem ser CONSOLIDADOS ({len(consolidar)}):")
    print("-" * 80)
    
    for cmd, files, priority in sorted(consolidar, key=lambda x: len(x[1]), reverse=True):
        print(f"\nComando: {cmd[:70]}...")
        print(f"Aparece em {len(files)} arquivos: {', '.join(files[:3])}{'...' if len(files) > 3 else ''}")
        if priority:
            print(f"✓ Manter em: {priority}")
            print(f"✗ Remover de: {', '.join([f for f in files if f != priority])}")
        else:
            print(f"⚠️  SEM PRIORIDADE DEFINIDA - Revisar manualmente")
    
    print("\n" + "=" * 80)
    print("\n💡 Próximos Passos:")
    print("1. Revise o arquivo duplicates-report.csv")
    print("2. Identifique comandos que devem ser mantidos em múltiplos contextos")
    print("3. Para comandos que devem ser removidos, edite manualmente os arquivos")
    print("4. Considere adicionar referências cruzadas em vez de duplicar")
    print("\nExemplo de referência cruzada:")
    print("  'Ver [Pods e Containers](04-pods-containers.md#logs) para comandos de logs'")


if __name__ == "__main__":
    main()
