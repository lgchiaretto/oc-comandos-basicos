#!/usr/bin/env python3
"""
Script para melhorar os comentários dos comandos bash nos arquivos markdown.

Este script:
1. Le todos os arquivos .md (exceto README, ESTRUTURA, INICIO-RAPIDO)
2. Identifica blocos de código bash
3. Melhora os comentários para serem mais claros e descritivos
4. Mantém a estrutura do código intacta
"""

import re
import os
import sys
from pathlib import Path

def improve_comment(comment, command):
    """
    Melhora um comentário baseado no comando.
    
    Args:
        comment: Comentário original
        command: Comando bash a ser executado
    
    Returns:
        Comentário melhorado
    """
    # Remove espaços extras
    comment = comment.strip()
    
    # Se é comentário de template/placeholder, manter original
    if '<' in comment and '>' in comment and any(x in comment for x in ['oc ', 'substituir', 'nome']):
        return comment
    
    # Se já começa com "Exemplo", manter
    if comment.startswith("Exemplo"):
        return comment
    
    # Comentários descritivos longos e específicos devem ser mantidos
    if len(comment) > 50 and any(x in comment.lower() for x in ['importante', 'cuidado', 'atenção', 'note', 'obs:', 'analise']):
        return comment
    
    # Padrões genéricos que precisam de melhoria
    generic_patterns = [
        r'^(Listar|Ver|Criar|Deletar|Editar|Adicionar|Remover|Atualizar|Aplicar)',
        r'^(Login|Logout|Descrever|Verificar|Trocar|Executar)',
        r'^(Coletar|Salvar|Exportar|Importar|Filtrar|Buscar)',
    ]
    
    # Melhorias específicas baseadas em comandos comuns
    improvements = {
        'oc get pods': 'Listar todos os pods do namespace atual',
        'oc get pods -A': 'Listar todos os pods de todos os namespaces do cluster',
        'oc get pods -o wide': 'Listar pods com informações adicionais (node, IP, etc)',
        'oc get pods --show-labels': 'Listar pods mostrando todas as labels associadas',
        'oc get projects': 'Listar todos os projetos do cluster',
        'oc projects': 'Listar projetos aos quais você tem acesso',
        'oc whoami': 'Exibir o nome do usuário autenticado atualmente',
        'oc whoami -t': 'Exibir o token de autenticação do usuário atual',
        'oc whoami --show-context': 'Exibir o contexto atual do kubeconfig',
        'oc whoami --show-console': 'Exibir a URL da console web do cluster',
        'oc whoami --show-server': 'Exibir a URL do servidor API conectado',
        'oc get nodes': 'Listar todos os nodes do cluster',
        'oc get events': 'Listar eventos do namespace atual',
        'oc get all': 'Listar todos os recursos principais do namespace',
        'oc status': 'Exibir visão geral dos recursos do projeto atual',
        'oc status --suggest': 'Exibir status com sugestões de ações',
        'oc version': 'Exibir versão do cliente oc e do servidor OpenShift',
        'oc cluster-info': 'Exibir informações básicas do cluster',
        'oc get clusteroperators': 'Listar status de todos os cluster operators',
        'oc get co': 'Listar status de todos os cluster operators',
        'oc get clusterversion': 'Exibir versão e status de atualização do cluster',
        'oc get quota': 'Listar quotas de recursos do namespace atual',
        'oc describe quota': 'Exibir detalhes das quotas configuradas',
        'oc get limitrange': 'Listar limit ranges configurados no namespace',
        'oc describe limitrange': 'Exibir detalhes dos limit ranges',
        'oc get hpa': 'Listar Horizontal Pod Autoscalers configurados',
        'oc get routes': 'Listar todas as routes expostas no namespace',
        'oc get svc': 'Listar todos os services do namespace atual',
        'oc get services': 'Listar todos os services do namespace atual',
        'oc get deployment': 'Listar todos os deployments do namespace',
        'oc get is': 'Listar todas as ImageStreams do projeto',
        'oc get bc': 'Listar todas as BuildConfigs do projeto',
        'oc get builds': 'Listar todos os builds do projeto',
        'oc get sa': 'Listar todas as ServiceAccounts do namespace',
        'oc get secrets': 'Listar todos os secrets do namespace atual',
        'oc get cm': 'Listar todos os ConfigMaps do namespace',
        'oc get configmap': 'Listar todos os ConfigMaps do namespace',
        'oc get pv': 'Listar todos os Persistent Volumes do cluster',
        'oc get pvc': 'Listar todos os Persistent Volume Claims do namespace',
        'oc get networkpolicy': 'Listar políticas de rede configuradas no namespace',
        'oc get machinesets': 'Listar todos os MachineSets configurados',
        'oc get machines': 'Listar todas as Machines (VMs) do cluster',
        'oc get csr': 'Listar Certificate Signing Requests pendentes',
        'oc api-resources': 'Listar todos os recursos da API disponíveis no cluster',
        'oc api-versions': 'Listar todas as versões de API disponíveis',
        'oc config view': 'Exibir configuração atual do kubeconfig',
        'oc config current-context': 'Exibir o contexto atual do kubeconfig',
        'oc config get-contexts': 'Listar todos os contextos disponíveis',
        'oc get replicasets': 'Listar todos os ReplicaSets do namespace',
        'oc get rs': 'Listar todos os ReplicaSets do namespace',
        'oc get rolebindings': 'Listar vinculações de roles no namespace atual',
        'oc get roles': 'Listar roles customizados do namespace',
        'oc get templates -n openshift': 'Listar templates disponíveis no namespace openshift',
        'oc project': 'Exibir o projeto (namespace) atual',
        'cat ~/.kube/config': 'Exibir conteúdo do arquivo de configuração do kubectl/oc',
    }
    
    # Procurar por correspondência exata primeiro
    cmd_clean = command.strip()
    if cmd_clean in improvements:
        return improvements[cmd_clean]
    
    # Melhorar comentários baseados em padrões do comando
    if 'oc get' in command:
        if '-A' in command or '--all-namespaces' in command:
            resource = extract_resource(command)
            return f'Listar {resource} de todos os namespaces do cluster'
        
        if '-o wide' in command:
            resource = extract_resource(command)
            return f'Listar {resource} com informações detalhadas'
        
        if '--show-labels' in command:
            resource = extract_resource(command)
            return f'Listar {resource} exibindo todas as labels'
        
        if '--sort-by' in command:
            resource = extract_resource(command)
            return f'Listar {resource} ordenados por campo específico'
        
        if '--field-selector' in command:
            if 'status.phase!=Running' in command:
                return 'Listar pods que não estão em estado Running'
            if 'status.phase=Pending' in command:
                return 'Listar pods em estado Pending (aguardando)'
            if 'status.phase=Failed' in command:
                return 'Listar pods que falharam'
            if 'type=Warning' in command:
                return 'Listar apenas eventos do tipo Warning'
            resource = extract_resource(command)
            return f'Listar {resource} filtrados por campo específico'
        
        if '-l ' in command or '--selector' in command:
            resource = extract_resource(command)
            return f'Listar {resource} filtrados por label'
        
        if '-o json' in command:
            resource = extract_resource(command)
            # Tentar extrair nome específico do recurso
            resource_name = extract_resource_name(command)
            if resource_name:
                return f'Exibir {resource} "{resource_name}" em formato JSON'
            return f'Exibir {resource} em formato JSON'
        
        if '-o yaml' in command:
            resource = extract_resource(command)
            # Tentar extrair nome específico do recurso
            resource_name = extract_resource_name(command)
            if resource_name:
                return f'Exibir {resource} "{resource_name}" em formato YAML'
            return f'Exibir {resource} em formato YAML'
        
        if '-o jsonpath' in command:
            return 'Extrair campo específico usando JSONPath'
        
        if '-o custom-columns' in command:
            resource = extract_resource(command)
            return f'Listar {resource} com colunas customizadas'
    
    if 'oc describe' in command:
        resource = extract_resource(command)
        return f'Exibir detalhes completos do {resource}'
    
    if 'oc delete' in command:
        if '--grace-period=0' in command or '--force' in command:
            resource = extract_resource(command)
            return f'Deletar {resource} forçadamente (sem período de espera)'
        if '--cascade=foreground' in command:
            resource = extract_resource(command)
            return f'Deletar {resource} e aguardar exclusão de recursos dependentes'
        if '-l ' in command or '--selector' in command:
            resource = extract_resource(command)
            return f'Deletar {resource} que correspondem ao seletor de label'
        resource = extract_resource(command)
        return f'Deletar o {resource} especificado'
    
    if 'oc create' in command:
        if 'job' in command:
            return 'Criar novo Job para execução única de tarefa'
        if 'cronjob' in command:
            return 'Criar novo CronJob para execução agendada'
        if 'route edge' in command:
            return 'Criar route com terminação TLS edge (TLS terminado no router)'
        if 'route passthrough' in command:
            return 'Criar route passthrough (TLS vai direto ao pod)'
        if 'route reencrypt' in command:
            return 'Criar route reencrypt (TLS terminado e re-encriptado)'
        resource = extract_resource(command)
        return f'Criar novo {resource}'
    
    if 'oc new-project' in command:
        if '--description' in command or '--display-name' in command:
            return 'Criar novo projeto com descrição e nome de exibição'
        if '--node-selector' in command:
            return 'Criar projeto com node selector para agendar pods'
        return 'Criar novo projeto (namespace) no cluster'
    
    if 'oc new-app' in command:
        if 'https://' in command or 'git@' in command:
            return 'Criar aplicação a partir de repositório Git'
        if '-e ' in command:
            return 'Criar aplicação com variáveis de ambiente'
        if '--template' in command:
            return 'Criar aplicação a partir de template'
        if '--strategy' in command:
            return 'Criar aplicação especificando estratégia de build'
        if '--name' in command:
            return 'Criar aplicação com nome customizado'
        return 'Criar nova aplicação a partir de imagem ou código fonte'
    
    if 'oc project' in command and 'new-project' not in command:
        if len(command.split()) > 2:
            return 'Trocar para o projeto especificado'
        return 'Exibir o projeto atual'
    
    if 'oc logs' in command:
        if '-f' in command or '--follow' in command:
            return 'Acompanhar logs em tempo real do pod'
        if '--previous' in command:
            return 'Exibir logs da instância anterior do container (após crash)'
        if '--tail' in command:
            return 'Exibir últimas N linhas dos logs'
        if '--since' in command:
            return 'Exibir logs a partir de um período de tempo'
        if '-l ' in command:
            return 'Exibir logs de todos os pods que correspondem ao label'
        if ' -c ' in command:
            return 'Exibir logs de container específico do pod'
        return 'Exibir logs do pod especificado'
    
    if 'oc exec' in command:
        if '-it' in command:
            return 'Executar comando interativo dentro do pod'
        if ' -c ' in command:
            return 'Executar comando em container específico do pod'
        return 'Executar comando dentro do pod especificado'
    
    if 'oc rsh' in command:
        return 'Abrir shell interativo dentro do pod'
    
    if 'oc cp' in command:
        if 'oc cp /' in command or 'oc cp .' in command:
            return 'Copiar arquivo/diretório da máquina local para o pod'
        return 'Copiar arquivo entre máquina local e pod'
    
    if 'oc rsync' in command:
        return 'Sincronizar diretórios entre máquina local e pod (requer rsync no pod)'
    
    if 'oc scale' in command:
        if '--replicas=0' in command:
            return 'Escalar deployment para zero (parar todos os pods)'
        return 'Ajustar número de réplicas do deployment/replicaset'
    
    if 'oc rollout' in command:
        if 'restart' in command:
            return 'Reiniciar deployment (recria todos os pods)'
        if 'undo' in command:
            if '--to-revision' in command:
                return 'Fazer rollback para revisão específica'
            return 'Fazer rollback para revisão anterior do deployment'
        if 'status' in command:
            return 'Verificar status do rollout em andamento'
        if 'history' in command:
            if '--revision' in command:
                return 'Exibir detalhes de revisão específica'
            return 'Exibir histórico de revisões do deployment'
        if 'pause' in command:
            return 'Pausar rollout do deployment (impede novas atualizações)'
        if 'resume' in command:
            return 'Retomar rollout pausado do deployment'
    
    if 'oc expose' in command:
        if 'service' in command:
            if '--hostname' in command:
                return 'Criar route com hostname customizado para o service'
            if '--path' in command:
                return 'Criar route com path específico para o service'
            return 'Criar route para expor service externamente'
        if 'deployment' in command:
            return 'Criar service expondo portas do deployment'
        return 'Expor recurso criando service'
    
    if 'oc set image' in command:
        return 'Atualizar imagem do container no deployment/pod'
    
    if 'oc set env' in command:
        return 'Definir/atualizar variáveis de ambiente no recurso'
    
    if 'oc set resources' in command:
        return 'Definir/atualizar requests e limits de recursos'
    
    if 'oc adm must-gather' in command:
        if '--dest-dir' in command:
            return 'Coletar dados de diagnóstico em diretório específico'
        if '--since' in command:
            return 'Coletar logs a partir de período específico'
        if '--node-name' in command:
            return 'Executar must-gather em node específico'
        return 'Coletar dados de diagnóstico completo do cluster'
    
    if 'oc adm inspect' in command:
        if 'clusteroperators' in command:
            return 'Coletar informações de debug de todos os cluster operators'
        if 'nodes' in command:
            return 'Coletar informações de debug de todos os nodes'
        if 'ns/' in command or 'namespace' in command:
            return 'Coletar informações de debug do namespace'
        return 'Inspecionar e coletar informações de recursos específicos'
    
    if 'oc label' in command:
        if '--overwrite' in command:
            return 'Atualizar label existente com novo valor'
        if command.rstrip().endswith('-'):
            return 'Remover label do recurso'
        return 'Adicionar nova label ao recurso'
    
    if 'oc annotate' in command:
        if '--overwrite' in command:
            return 'Atualizar annotation existente com novo valor'
        return 'Adicionar annotation ao recurso'
    
    if 'oc patch' in command:
        if '--type=merge' in command:
            return 'Aplicar merge patch ao recurso (mescla alterações)'
        if '--type=json' in command:
            return 'Aplicar JSON patch ao recurso'
        if '--type=strategic' in command:
            return 'Aplicar strategic merge patch ao recurso'
        return 'Aplicar modificação parcial ao recurso usando patch'
    
    if 'oc edit' in command:
        return 'Abrir editor para modificar recurso interativamente'
    
    if 'oc apply' in command:
        if '-f' in command:
            return 'Aplicar configuração do arquivo YAML/JSON ao cluster'
        return 'Aplicar configuração ao cluster'
    
    if 'oc wait' in command:
        if 'condition=Ready' in command:
            return 'Aguardar pod ficar no estado Ready'
        if 'condition=available' in command:
            return 'Aguardar deployment ficar disponível'
        if '--timeout' in command:
            return 'Aguardar condição com timeout específico'
        return 'Aguardar condição específica do recurso'
    
    if 'oc auth can-i' in command:
        return 'Verificar se usuário tem permissão para executar ação específica'
    
    if 'oc adm policy' in command:
        if 'add-role-to-user' in command:
            return 'Adicionar role ao usuário no projeto/cluster'
        if 'remove-role-from-user' in command:
            return 'Remover role do usuário'
        if 'add-cluster-role-to-user' in command:
            return 'Adicionar cluster role ao usuário'
        if 'who-can' in command:
            return 'Verificar quem tem permissão para executar ação'
    
    if 'oc autoscale' in command:
        return 'Criar Horizontal Pod Autoscaler (HPA) para escalar automaticamente'
    
    if 'oc run' in command:
        if '--rm' in command and '-it' in command:
            return 'Criar pod temporário interativo (removido ao sair)'
        if '--restart=Never' in command:
            return 'Criar pod único (não recriado)'
        return 'Criar e executar pod'
    
    if 'oc debug' in command:
        if '--image' in command:
            return 'Criar pod de debug com imagem customizada'
        return 'Criar cópia de pod para debug interativo'
    
    if 'oc adm certificate approve' in command:
        return 'Aprovar Certificate Signing Request (CSR)'
    
    if 'oc extract' in command:
        return 'Extrair conteúdo de secret/configmap para arquivos'
    
    if 'oc set data' in command:
        return 'Atualizar dados em configmap ou secret'
    
    # Se já é claro e específico, manter
    if len(comment) > 30 and not any(re.match(pat, comment) for pat in generic_patterns):
        return comment
    
    # Melhorar comentários muito genéricos
    if comment in ['Exemplo', 'Exemplo prático']:
        # Tentar inferir do comando
        if 'new-project' in command:
            return 'Exemplo: Criar projeto com configurações customizadas'
        if 'new-app' in command:
            return 'Exemplo: Deploy de aplicação com parâmetros'
        return comment + ' de uso do comando'
    
    # Retornar comentário melhorado ou original
    return comment


def extract_resource(command):
    """
    Extrai o nome do recurso de um comando oc.
    
    Args:
        command: Comando oc completo
    
    Returns:
        Nome do recurso ou 'recurso'
    """
    # Mapeamento de abreviações para nomes completos
    resource_map = {
        'po': 'pod',
        'pods': 'pods',
        'svc': 'service',
        'deploy': 'deployment',
        'deployments': 'deployments',
        'rs': 'replicaset',
        'rc': 'replicationcontroller',
        'ds': 'daemonset',
        'sts': 'statefulset',
        'job': 'job',
        'cj': 'cronjob',
        'cm': 'configmap',
        'secret': 'secret',
        'ing': 'ingress',
        'pv': 'persistent volume',
        'pvc': 'persistent volume claim',
        'sc': 'storageclass',
        'ns': 'namespace',
        'no': 'node',
        'sa': 'serviceaccount',
        'role': 'role',
        'rb': 'rolebinding',
        'clusterrole': 'cluster role',
        'crb': 'clusterrolebinding',
        'pdb': 'poddisruptionbudget',
        'hpa': 'horizontal pod autoscaler',
        'project': 'projeto',
        'projects': 'projetos',
        'route': 'route',
        'routes': 'routes',
        'bc': 'buildconfig',
        'build': 'build',
        'is': 'imagestream',
        'dc': 'deploymentconfig',
        'co': 'cluster operator',
        'clusteroperator': 'cluster operator',
        'clusteroperators': 'cluster operators',
        'machine': 'machine',
        'machines': 'machines',
        'machineset': 'machineset',
        'machinesets': 'machinesets',
        'node': 'node',
        'nodes': 'nodes',
        'csr': 'certificate signing request',
        'endpoints': 'endpoints',
        'networkpolicy': 'network policy',
        'event': 'evento',
        'events': 'eventos',
        'quota': 'quota',
        'limitrange': 'limit range',
        'resourcequota': 'resource quota',
    }
    
    parts = command.split()
    if len(parts) > 2:
        resource_part = parts[2].split('/')[0] if '/' in parts[2] else parts[2]
        return resource_map.get(resource_part, 'recurso')
    
    return 'recurso'


def extract_resource_name(command):
    """
    Extrai o nome específico de um recurso de um comando oc.
    
    Args:
        command: Comando oc completo
    
    Returns:
        Nome específico do recurso ou None
    """
    # Padrão: oc get/describe/delete <tipo> <nome> ...
    # Exemplo: oc get pod my-pod -o yaml
    match = re.search(r'oc\s+(?:get|describe|delete|edit)\s+\w+\s+([a-zA-Z0-9][-a-zA-Z0-9./]*)', command)
    if match:
        name = match.group(1)
        # Ignorar flags
        if name.startswith('-'):
            return None
        # Ignorar patterns comuns de flags/opções
        if name in ['all', 'pods', 'services', 'routes', 'deployments']:
            return None
        return name
    return None


def process_markdown_file(filepath):
    """
    Processa um arquivo markdown melhorando os comentários dos comandos bash.
    
    Args:
        filepath: Caminho do arquivo markdown
    
    Returns:
        Tupla (modified, new_content) - Se foi modificado e o novo conteúdo
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Padrão para encontrar blocos de código bash
    # Captura: ```bash\n# comentário\ncomando\n```
    pattern = re.compile(
        r'```bash(?:\s+ignore-test)?\n((?:#[^\n]*\n)*)(.*?)(?=\n```)',
        re.MULTILINE | re.DOTALL
    )
    
    modified = False
    new_content = content
    
    for match in pattern.finditer(content):
        comments_block = match.group(1)
        command_block = match.group(2).strip()
        
        if not comments_block or not command_block:
            continue
        
        # Processar cada linha de comentário
        comment_lines = comments_block.strip().split('\n')
        improved_comments = []
        seen_comments = set()  # Evitar duplicatas
        
        # Pegar todas as linhas de comando para melhor contexto
        command_lines = [line.strip() for line in command_block.split('\n') if line.strip() and not line.strip().startswith('#')]
        first_command = command_lines[0] if command_lines else ''
        
        # Determinar se temos comentários template (com placeholders)
        has_template = any('<' in line and '>' in line for line in command_lines)
        
        for i, comment_line in enumerate(comment_lines):
            if comment_line.startswith('#'):
                original_comment = comment_line[1:].strip()
                
                # Se é um comentário de template/placeholder, manter original
                if has_template and (i < len(command_lines)) and ('<' in command_lines[i] or '>' in command_lines[i]):
                    improved_comments.append(comment_line)
                    continue
                
                improved = improve_comment(original_comment, first_command)
                
                # Evitar duplicatas consecutivas
                if improved not in seen_comments or i == 0:
                    if improved != original_comment:
                        improved_comments.append(f'# {improved}')
                        modified = True
                    else:
                        improved_comments.append(comment_line)
                    seen_comments.add(improved)
            else:
                improved_comments.append(comment_line)
        
        if modified:
            old_block = match.group(0)
            new_block = f"```bash{' ignore-test' if 'ignore-test' in old_block else ''}\n"
            new_block += '\n'.join(improved_comments)
            new_block += f'\n{command_block}'
            
            new_content = new_content.replace(old_block, new_block)
    
    return modified, new_content


def main():
    """Função principal."""
    # Diretório raiz do projeto
    root_dir = Path(__file__).parent.parent
    
    # Arquivos para ignorar
    ignore_files = [
        'README.md',
        'ESTRUTURA.md', 
        'INICIO-RAPIDO.md',
    ]
    
    # Encontrar todos os arquivos .md
    md_files = sorted(root_dir.glob('*.md'))
    
    files_modified = 0
    total_files = 0
    
    print("🔧 Melhorando comentários dos comandos bash...\n")
    
    for md_file in md_files:
        if md_file.name in ignore_files:
            continue
        
        total_files += 1
        print(f"Processando: {md_file.name}...", end=' ')
        
        try:
            modified, new_content = process_markdown_file(md_file)
            
            if modified:
                # Fazer backup
                backup_file = md_file.with_suffix('.md.bak')
                md_file.rename(backup_file)
                
                # Escrever novo conteúdo
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("✅ Atualizado")
                files_modified += 1
                
                # Remover backup se tudo deu certo
                backup_file.unlink()
            else:
                print("⏭️  Sem mudanças")
        
        except Exception as e:
            print(f"❌ Erro: {e}")
            continue
    
    print(f"\n📊 Resumo:")
    print(f"   Total de arquivos processados: {total_files}")
    print(f"   Arquivos modificados: {files_modified}")
    print(f"   Arquivos sem mudanças: {total_files - files_modified}")
    
    if files_modified > 0:
        print(f"\n✨ Comentários melhorados com sucesso!")
        print(f"💡 Revise as mudanças com: git diff")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
