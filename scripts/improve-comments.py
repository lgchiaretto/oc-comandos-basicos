#!/usr/bin/env python3
"""
Script para melhorar comentários genéricos de comandos OpenShift nos arquivos markdown.

Agora com análise inteligente de JSONPath!
"""

import re
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def analyze_jsonpath(jsonpath: str, resource: str) -> Optional[str]:
    """
    Analisa um JSONPath e retorna uma descrição específica do que está sendo extraído.
    """
    # Remove aspas e chaves externas
    path = jsonpath.replace("'", "").replace('"', '').strip('{}')
    
    # Detecções específicas para .items com filtros
    if '.items[?(@.status.phase==' in path:
        if 'Pending' in path:
            return f'Listar nomes de {resource}s em estado Pending'
        elif 'Available' in path:
            return f'Listar nomes de {resource}s em estado Available'
        elif 'Failed' in path:
            return f'Listar nomes de {resource}s em estado Failed'
        elif 'Active' in path:
            return f'Listar nomes de {resource}s em estado Active'
        elif 'Terminating' in path:
            return f'Listar nomes de {resource}s em processo de terminação'
        elif 'Running' in path:
            return f'Listar nomes de {resource}s em estado Running'
        elif 'Succeeded' in path:
            return f'Listar nomes de {resource}s concluídos com sucesso'
        elif 'Bound' in path:
            return f'Listar nomes de {resource}s em estado Bound (vinculados)'
    
    # Detecções para restart count
    if 'restartCount' in path:
        if '.items[?(' in path and 'restartCount>0' in path:
            return f'Listar {resource}s que reiniciaram pelo menos uma vez'
        elif '.status.containerStatuses[0].restartCount' in path:
            return f'Exibir número de reinicializações do container principal'
    
    # Detecções para range com formatação customizada
    if '{range .items[*]}' in path:
        if '.metadata.name' in path and '.spec.containers[*].image' in path:
            return f'Listar {resource}s com seus nomes e imagens de containers'
        elif '.metadata.name' in path and '.status.podIP' in path:
            return f'Listar {resource}s com seus nomes e endereços IP'
        elif '.metadata.name' in path and '.spec.claimRef.name' in path:
            return f'Listar {resource}s com seus PVCs associados'
        elif '.metadata.name' in path and 'kubeletVersion' in path:
            return f'Listar nodes com suas versões do kubelet'
        elif '.metadata.name' in path and 'node-role' in path:
            return f'Listar nodes com suas roles (funções)'
        elif '.metadata.name' in path:
            return f'Listar nomes de todos os {resource}s (um por linha)'
    
    # Detecções para nodes com condições
    if 'node' in resource.lower() and '.items[?(@.status.conditions' in path:
        if 'status=="True"' in path or 'status==\"True\"' in path:
            return 'Listar nodes em estado Ready'
    
    # Detecções para .items[*] simples
    if '.items[*].metadata.name' in path and 'range' not in path:
        return f'Listar nomes de todos os {resource}s (em uma linha)'
    
    # Detecções para spec.containers
    if '.spec.containers[0].image' in path:
        return f'Exibir imagem do primeiro container do {resource}'
    
    # Detecções específicas para clusterversion
    if 'clusterversion' in resource.lower():
        if '.items[0].status.desired.version' in path:
            return 'Exibir versão desejada para o cluster'
        elif '.items[0].spec.desiredUpdate' in path:
            return 'Exibir atualização desejada configurada'
        elif '.items[0].status.history' in path:
            return 'Exibir histórico de versões do cluster'
        elif '.items[0].spec.channel' in path:
            return 'Exibir canal de atualização configurado'
        elif '.items[0].status.conditions[?(@.type==' in path:
            if 'Available' in path:
                return 'Exibir condição de disponibilidade do cluster'
            elif 'Failing' in path:
                return 'Exibir condição de falha do cluster'
            elif 'Progressing' in path:
                if '.status' in path and 'message' not in path:
                    return 'Exibir status da progressão da atualização'
                elif '.message' in path:
                    return 'Exibir mensagem da progressão da atualização'
                else:
                    return 'Exibir informações da progressão da atualização'
        elif '.spec.overrides' in path:
            return 'Exibir overrides (sobrescritas) de versão configurados'
    
    # Detecções para MachineConfigPool (mcp)
    if 'mcp' in resource.lower() or 'machineconfigpool' in resource.lower():
        if 'Updated:' in path or 'updatedMachineCount' in path:
            return 'Exibir contadores de máquinas atualizadas/total/degradadas'
    
    # Detecções para lastState.terminated
    if '.status.containerStatuses[0].lastState.terminated.reason' in path:
        return 'Exibir motivo da última terminação do container'
    
    # Detecções para status.podIP
    if '.status.podIP' in path:
        return f'Exibir endereço IP do {resource}'
    
    # Detecções para securityContext
    if '.spec.securityContext.runAsUser' in path:
        return f'Exibir UID do usuário que executa o {resource}'
    elif '.spec.securityContext' in path:
        return f'Exibir contexto de segurança do {resource}'
    
    # Detecções para resources.limits e requests
    if '.spec.containers[0].resources.limits.memory' in path:
        return 'Exibir limite de memória do primeiro container'
    elif '.spec.containers[0].resources.limits.cpu' in path:
        return 'Exibir limite de CPU do primeiro container'
    elif '.spec.containers[0].resources.requests.memory' in path:
        return 'Exibir memória solicitada pelo primeiro container'
    elif '.spec.containers[0].resources.requests.cpu' in path:
        return 'Exibir CPU solicitada pelo primeiro container'
    
    # Detecções para services de tipo específico
    if 'service' in resource.lower() or 'svc' in resource.lower():
        if ".items[?(@.spec.type=='LoadBalancer')]" in path or '.items[?(@.spec.type=="LoadBalancer")]' in path:
            return 'Listar services do tipo LoadBalancer'
        elif ".items[?(@.spec.type=='NodePort')]" in path or '.items[?(@.spec.type=="NodePort")]' in path:
            return 'Listar services do tipo NodePort'
        elif ".items[?(@.spec.type=='ClusterIP')]" in path or '.items[?(@.spec.type=="ClusterIP")]' in path:
            return 'Listar services do tipo ClusterIP'
    
    # Detecções baseadas em campos específicos
    if '.status.phase' in path and not '.items' in path:
        return f'Exibir status/fase atual do {resource}'
    elif '.spec.volumeName' in path:
        return f'Exibir nome do volume associado ao {resource}'
    elif '.spec.resources.requests.storage' in path:
        return f'Exibir capacidade de armazenamento solicitada pelo {resource}'
    elif '.spec.claimRef.name' in path:
        return f'Exibir nome do PVC que utiliza este {resource}'
    elif '.spec.accessModes' in path:
        return f'Exibir modos de acesso configurados no {resource}'
    elif '.spec.nodeName' in path:
        return f'Exibir nome do node onde o {resource} está executando'
    elif '.metadata.finalizers' in path:
        return f'Exibir finalizers configurados no {resource}'
    elif '.metadata.name' in path and '.items' in path:
        return f'Listar nomes de todos os {resource}s'
    elif '.metadata.name' in path:
        return f'Exibir nome do {resource}'
    elif '.status.conditions[0].message' in path:
        return f'Exibir mensagem da primeira condição de status do {resource}'
    elif '.status.conditions' in path and 'type' in path and 'message' in path:
        cond_type = re.search(r'type==["\'](\w+)["\']', path)
        if cond_type:
            return f'Exibir mensagem da condição {cond_type.group(1)} do {resource}'
    elif '.status.conditions' in path and 'type' in path and 'status' in path:
        cond_type = re.search(r'type==["\'](\w+)["\']', path)
        if cond_type:
            return f'Exibir status da condição {cond_type.group(1)} do {resource}'
    elif '.status.health.status' in path:
        return f'Exibir status de health do {resource}'
    elif '.status.sync.status' in path:
        return f'Exibir status de sincronização do {resource}'
    elif '.spec.source.repoURL' in path:
        return f'Exibir URL do repositório Git da aplicação'
    elif '.spec.source.path' in path:
        return f'Exibir caminho do código no repositório'
    elif '.spec.syncPolicy' in path:
        return f'Exibir política de sincronização do {resource}'
    elif '.spec.host' in path:
        return f'Exibir hostname da {resource}'
    elif '.spec.provisioner' in path:
        return f'Exibir provisioner da {resource}'
    elif '.data.ca.crt' in path or '.data.ca\\.crt' in path:
        return f'Exibir certificado CA do secret (codificado em base64)'
    elif '.data.' in path:
        data_key = re.search(r'\.data\.([^}]+)', path)
        if data_key:
            key_name = data_key.group(1).replace('\\', '')
            return f'Exibir valor da chave {key_name} do secret (codificado em base64)'
    elif '.spec.containers[*].image' in path or '.spec.template.spec.containers[*].image' in path:
        return f'Listar imagens de todos os containers'
    elif '.status.versions[0].version' in path:
        return f'Exibir versão atual do {resource}'
    elif '.status.configuration.name' in path:
        return f'Exibir nome da configuração atual do {resource}'
    
    return None


# Recursos conhecidos e seus nomes amigáveis
RESOURCE_NAMES = {
    'pod': 'pod', 'pods': 'pods',
    'deployment': 'deployment', 'deployments': 'deployments',
    'service': 'service', 'services': 'services', 'svc': 'service',
    'route': 'route', 'routes': 'routes',
    'pvc': 'persistent volume claim',
    'pv': 'persistent volume',
    'persistentvolumeclaim': 'persistent volume claim',
    'persistentvolume': 'persistent volume',
    'node': 'node', 'nodes': 'nodes',
    'namespace': 'namespace', 'project': 'projeto', 'projects': 'projetos',
    'configmap': 'configmap', 'secret': 'secret',
    'sa': 'ServiceAccount', 'serviceaccount': 'ServiceAccount',
    'hpa': 'horizontal pod autoscaler',
    'quota': 'quota', 'limitrange': 'limit range',
    'networkpolicy': 'política de rede',
    'rolebinding': 'vinculação de role', 'rolebindings': 'vinculações de roles',
    'role': 'role', 'roles': 'roles',
    'build': 'build', 'builds': 'builds',
    'buildconfig': 'build config',
    'imagestream': 'image stream',
    'co': 'cluster operator', 'clusteroperator': 'cluster operator', 'clusteroperators': 'cluster operators',
    'csr': 'certificate signing request',
    'events': 'eventos', 'event': 'evento',
    'all': 'recurso',
    'storageclass': 'storageclass', 'sc': 'storageclass',
    'application': 'aplicação',
    'mcp': 'mcp',
    'clusterversion': 'clusterversion',
    'resourcequotas': 'resourcequotas',
    'limitranges': 'limitranges',
    'jobs': 'jobs',
}


def get_resource_name(resource: str) -> str:
    """Converte nome de recurso para versão amigável."""
    resource_lower = resource.lower()
    return RESOURCE_NAMES.get(resource_lower, resource)


def improve_comment(command: str, current_comment: str) -> Optional[str]:
    """
    Melhora um comentário genérico baseado no comando.
    """
    # Padrões genéricos conhecidos que devem ser melhorados
    generic_patterns = [
        r'^Exibir [\w\s-]+ em formato (JSON|YAML)$',
        r'^Exibir recurso "[^"]*" em formato (JSON|YAML)$',
        r'^Listar (todos os )?[\w\s-]+ (do|de todos os) .*$',
        r'^Listar recurso .*$',
        r'^Exibir detalhes .*$',
        r'^Deletar o recurso .*$',
        r'^Aplicar modificação .*$',
        r'^Adicionar .*$',
        r'^Remover .*$',
        r'^Executar comando .*$',
    ]
    
    # Se o comentário não é genérico, não precisa melhorar
    is_generic = any(re.match(pattern, current_comment) for pattern in generic_patterns)
    if not is_generic:
        return None
    
    # 1. PRIMEIRO: Tenta capturar JSONPath (mais específico)
    jsonpath_match = re.search(r'oc get ([\w\./-]+)(?:\s+[\w-]+)?\s+-o\s+jsonpath=([^\s]+)', command)
    if jsonpath_match:
        resource = jsonpath_match.group(1)
        jsonpath = jsonpath_match.group(2)
        resource_name = get_resource_name(resource)
        
        analyzed = analyze_jsonpath(jsonpath, resource_name)
        if analyzed:
            return analyzed
        # Se não conseguiu analisar, usa genérico mas melhorado
        return f'Exibir {resource_name} usando JSONPath customizado'
    
    # 2. Outros padrões de 'oc get'
    if re.search(r'oc get ([\w\./-]+)(?:\s+[\w-]+)?\s+-o\s+json', command):
        match = re.search(r'oc get ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            if match.group(1).lower() == 'pod':
                return 'Exibir configuração completa do pod em formato JSON'
            elif match.group(1).lower() in ['pvc', 'persistentvolumeclaim']:
                return 'Exibir configuração completa do PVC em formato JSON'
            return f'Exibir {resource_name} em formato JSON completo'
    
    if re.search(r'oc get ([\w\./-]+)(?:\s+[\w-]+)?\s+-o\s+yaml', command):
        match = re.search(r'oc get ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Exibir {resource_name} em formato YAML completo'
    
    if re.search(r'oc get ([\w\./-]+)\s+-A', command):
        match = re.search(r'oc get ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Listar {resource_name} de todos os namespaces do cluster'
    
    if re.search(r'oc get ([\w\./-]+)\s+-l\s+', command):
        match = re.search(r'oc get ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Listar {resource_name} filtrados por label'
    
    if re.search(r'oc get ([\w\./-]+)\s+--field-selector', command):
        match = re.search(r'oc get ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Listar {resource_name} filtrados por campo específico'
    
    if re.search(r'oc get ([\w\./-]+)\s+--sort-by', command):
        match = re.search(r'oc get ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Listar {resource_name} ordenados por campo específico'
    
    # 3. oc describe
    if re.search(r'oc describe ([\w\./-]+)\s+[\w-]+', command):
        match = re.search(r'oc describe ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Exibir detalhes completos do {resource_name}'
    
    # 4. oc delete
    if re.search(r'oc delete ([\w\./-]+)\s+[\w-]+\s+--grace-period=0\s+--force', command):
        match = re.search(r'oc delete ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Deletar {resource_name} forçadamente (sem período de espera)'
    
    if re.search(r'oc delete ([\w\./-]+)\s+-l\s+', command):
        match = re.search(r'oc delete ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Deletar {resource_name} que correspondem ao seletor de label'
    
    if re.search(r'oc delete ([\w\./-]+)\s+[\w-]+', command):
        match = re.search(r'oc delete ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Deletar o {resource_name} especificado'
    
    # 5. oc patch
    if re.search(r'oc patch ([\w\./-]+)\s+[\w-]+\s+-p', command):
        match = re.search(r'oc patch ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Aplicar modificação parcial ao {resource_name} usando patch'
    
    # 6. oc scale
    if re.search(r'oc scale ([\w\./-]+)\s+[\w-]+\s+--replicas=0', command):
        match = re.search(r'oc scale ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Escalar {resource_name} para zero (parar todos os pods)'
    
    if re.search(r'oc scale ([\w\./-]+)\s+[\w-]+\s+--replicas=', command):
        match = re.search(r'oc scale ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Ajustar número de réplicas do {resource_name}'
    
    # 7. oc label
    if re.search(r'oc label ([\w\./-]+)\s+[\w-]+.*--overwrite', command):
        match = re.search(r'oc label ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Atualizar label existente do {resource_name}'
    
    if re.search(r'oc label ([\w\./-]+)\s+[\w-]+\s+\w+-$', command):
        match = re.search(r'oc label ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Remover label do {resource_name}'
    
    if re.search(r'oc label ([\w\./-]+)\s+[\w-]+', command):
        match = re.search(r'oc label ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Adicionar nova label ao {resource_name}'
    
    # 8. oc annotate
    if re.search(r'oc annotate ([\w\./-]+)\s+[\w-]+.*--overwrite', command):
        match = re.search(r'oc annotate ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Atualizar annotation existente do {resource_name}'
    
    if re.search(r'oc annotate ([\w\./-]+)\s+[\w-]+', command):
        match = re.search(r'oc annotate ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Adicionar annotation ao {resource_name}'
    
    # 9. Comandos administrativos
    if 'oc adm certificate approve' in command:
        return 'Aprovar Certificate Signing Request (CSR) pendente'
    
    if 'oc adm must-gather' in command:
        return 'Coletar dados de diagnóstico completo do cluster'
    
    # 10. oc rollout
    if re.search(r'oc rollout restart ([\w\./-]+)', command):
        match = re.search(r'oc rollout restart ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Reiniciar {resource_name} (recria todos os pods)'
    
    if re.search(r'oc rollout undo ([\w\./-]+)\s+--to-revision', command):
        match = re.search(r'oc rollout undo ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Fazer rollback do {resource_name} para revisão específica'
    
    if re.search(r'oc rollout undo ([\w\./-]+)', command):
        match = re.search(r'oc rollout undo ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Fazer rollback do {resource_name} para revisão anterior'
    
    if re.search(r'oc rollout history ([\w\./-]+)', command):
        match = re.search(r'oc rollout history ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Exibir histórico de revisões do {resource_name}'
    
    if re.search(r'oc rollout status ([\w\./-]+)', command):
        return 'Verificar status do rollout em andamento'
    
    # 11. oc exec
    if 'oc exec' in command and '--' in command:
        return 'Executar comando dentro do pod especificado'
    
    # 12. oc logs
    if 'oc logs' in command and '--previous' in command:
        return 'Exibir logs da instância anterior do container (após crash)'
    
    if 'oc logs' in command and '-l' in command:
        return 'Exibir logs de todos os pods que correspondem ao label'
    
    # 13. oc whoami
    if 'oc whoami -t' in command:
        return 'Exibir o token de autenticação do usuário atual'
    
    if 'oc whoami --show-context' in command:
        return 'Exibir o contexto atual do kubeconfig'
    
    if 'oc whoami --show-console' in command:
        return 'Exibir a URL da console web do cluster'
    
    if 'oc whoami --show-server' in command:
        return 'Exibir a URL do servidor API conectado'
    
    if 'oc whoami' in command:
        return 'Exibir o nome do usuário autenticado atualmente'
    
    # 14. oc project
    if re.search(r'oc project\s+[\w-]+', command):
        return 'Trocar para o projeto especificado'
    
    if 'oc project' in command:
        return 'Exibir o projeto (namespace) atual'
    
    # 15. oc new-project
    if 'oc new-project' in command:
        return 'Criar novo projeto (namespace) no cluster'
    
    # 16. Outros comandos
    if 'oc autoscale' in command:
        return 'Criar Horizontal Pod Autoscaler (HPA) para escalar automaticamente'
    
    if 'oc set image' in command:
        match = re.search(r'oc set image ([\w\./-]+)', command)
        if match:
            resource_name = get_resource_name(match.group(1))
            return f'Atualizar imagem do container no {resource_name}'
    
    if 'oc wait --for=condition=Ready' in command:
        return 'Aguardar recurso ficar no estado Ready'
    
    if 'oc auth can-i' in command:
        return 'Verificar se usuário tem permissão para executar ação específica'
    
    if 'oc config view' in command:
        return 'Exibir configuração atual do kubeconfig'
    
    if 'oc config current-context' in command:
        return 'Exibir o contexto atual do kubeconfig'
    
    if 'oc config get-contexts' in command:
        return 'Listar todos os contextos disponíveis'
    
    if 'oc api-resources' in command:
        return 'Listar todos os recursos da API disponíveis no cluster'
    
    if 'oc api-versions' in command:
        return 'Listar todas as versões de API disponíveis'
    
    if 'oc version' in command:
        return 'Exibir versão do cliente oc e do servidor OpenShift'
    
    if 'oc cluster-info' in command:
        return 'Exibir informações básicas do cluster'
    
    if 'oc status' in command:
        return 'Exibir visão geral dos recursos do projeto atual'
    
    if 'oc apply -f' in command:
        return 'Aplicar configuração do arquivo YAML/JSON ao cluster'
    
    if 'oc create -f' in command:
        return 'Criar novo recurso a partir do arquivo especificado'
    
    if 'cat ~/.kube/config' in command:
        return 'Exibir conteúdo do arquivo de configuração do kubectl/oc'
    
    return None


def process_markdown_file(filepath: Path, dry_run: bool = False) -> Tuple[int, int]:
    """
    Processa um arquivo markdown melhorando comentários genéricos.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Padrão para encontrar blocos de código bash com comentário em negrito
    pattern = r'\*\*([^*]+)\*\*(\n\n```bash[^\n]*\n)(oc [^\n]+)'
    
    total_found = 0
    total_improved = 0
    new_content = content
    
    def replace_comment(match):
        nonlocal total_found, total_improved
        
        current_comment = match.group(1).strip()
        separator = match.group(2)
        command = match.group(3)
        
        total_found += 1
        
        improved_comment = improve_comment(command, current_comment)
        
        if improved_comment and improved_comment != current_comment:
            total_improved += 1
            print(f"\n  Arquivo: {filepath.name}")
            print(f"  Comando: {command[:70]}...")
            print(f"  Antes:   {current_comment}")
            print(f"  Depois:  {improved_comment}")
            
            return f"**{improved_comment}**{separator}{command}"
        
        return match.group(0)
    
    new_content = re.sub(pattern, replace_comment, new_content, flags=re.MULTILINE)
    
    if not dry_run and total_improved > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\n✓ Arquivo atualizado: {filepath}")
    
    return total_found, total_improved


def main():
    parser = argparse.ArgumentParser(
        description='Melhora comentários genéricos em arquivos markdown de comandos OpenShift'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Apenas exibe as mudanças sem salvar os arquivos'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Processa apenas o arquivo especificado'
    )
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    if args.file:
        files_to_process = [Path(args.file)]
    else:
        files_to_process = [
            f for f in repo_root.glob('*.md')
            if f.name not in ['README.md', 'ESTRUTURA.md']
            and re.match(r'^\d{2}-', f.name)
        ]
    
    print(f"{'=' * 80}")
    print(f"Melhorando comentários em {len(files_to_process)} arquivo(s)")
    if args.dry_run:
        print("MODO DRY-RUN: Nenhum arquivo será modificado")
    print(f"{'=' * 80}")
    
    total_files_changed = 0
    grand_total_found = 0
    grand_total_improved = 0
    
    for filepath in sorted(files_to_process):
        found, improved = process_markdown_file(filepath, args.dry_run)
        grand_total_found += found
        grand_total_improved += improved
        
        if improved > 0:
            total_files_changed += 1
    
    print(f"\n{'=' * 80}")
    print(f"RESUMO:")
    print(f"  Arquivos processados:      {len(files_to_process)}")
    print(f"  Arquivos com mudanças:     {total_files_changed}")
    print(f"  Comentários encontrados:   {grand_total_found}")
    print(f"  Comentários melhorados:    {grand_total_improved}")
    print(f"{'=' * 80}")
    
    if args.dry_run:
        print("\nPara aplicar as mudanças, execute sem --dry-run")
    else:
        print("\nConcluído! Arquivos atualizados com sucesso.")
        print("\nPróximos passos:")
        print("  1. Revise as mudanças: git diff")
        print("  2. Execute os testes: ./scripts/test-commands.sh")
        print("  3. Se tudo estiver OK, faça commit das mudanças")


if __name__ == '__main__':
    main()
