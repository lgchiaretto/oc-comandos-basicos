# Guia Completo de Comandos do OpenShift

Este é um guia abrangente de comandos do OpenShift (OCP) organizado por categoria, incluindo comandos básicos e avançados para troubleshooting e administração.

---

## Início Rápido

**Novo no OpenShift?** Comece com o [**Guia de Início Rápido**](INICIO-RAPIDO.md) que contém os 20 comandos mais utilizados!

---

## Como Usar Este Guia

### Para Iniciantes
Comece pelos documentos essenciais (1-6) para entender os conceitos básicos do OpenShift.

### Para Administradores
Foque nos documentos de administração avançada (17-22) e troubleshooting (13-15).

### Para DevOps
Concentre-se em Build/CI/CD (9-10), aplicações (3) e observabilidade (11-12).

### Para Troubleshooting
Vá direto para os documentos de troubleshooting (13-15, 31), must-gather (12) e segurança (16).

---

## Categorias de Comandos

### Por Recurso
- **Pods**: Documentos 4, 13
- **Deployments**: Documento 5
- **Services**: Documento 6
- **Storage**: Documentos 8, 15
- **Nodes**: Documento 18

### Por Função
- **Criação**: Documentos 2, 3, 7, 9
- **Troubleshooting**: Documentos 13, 14, 15, 31
- **Monitoramento**: Documentos 11, 12
- **Segurança**: Documento 16

### Por Nível
- **Básico**: Documentos 1-6
- **Intermediário**: Documentos 7-12
- **Avançado**: Documentos 13-22
- **Expert**: Documentos 23-31

---

## Importante

> **Nota**: Sempre teste comandos destrutivos (delete, drain, etc.) em ambientes não produtivos antes de executar em produção.

---

## Índice de Documentos

### Comandos Essenciais
1. [**Autenticação e Configuração**](01-autenticacao-configuracao.md)
   - Login/Logout
   - Configuração do cliente
   - Contextos e namespaces

2. [**Projetos**](02-projetos.md)
   - Criar, listar e gerenciar projetos
   - Node selectors
   - Quotas e limits

3. [**Aplicações**](03-aplicacoes.md)
   - Criar aplicações
   - Gerenciar deployments
   - Build e deploy

### Recursos e Workloads
4. [**Pods e Containers**](04-pods-containers.md)
   - Listar e descrever pods
   - Executar comandos
   - Debug e troubleshooting

5. [**Deployments e Scaling**](05-deployments-scaling.md)
   - Deployments e ReplicaSets
   - Scaling manual e automático
   - Rollouts e rollbacks

6. [**Services e Routes**](06-services-routes.md)
   - Services e endpoints
   - Routes e ingress
   - TLS e certificados

### Configuração
7. [**ConfigMaps e Secrets**](07-configmaps-secrets.md)
   - Criar e gerenciar ConfigMaps
   - Secrets e credenciais
   - Injeção em pods

8. [**Storage**](08-storage.md)
   - PV e PVC
   - Storage Classes
   - Volumes e montagens

### Build e CI/CD
9. [**Builds e ImageStreams**](09-builds-images.md)
   - Build configs
   - ImageStreams
   - Source-to-Image (S2I)

10. [**Registry e Imagens**](10-registry-imagens.md)
    - Registry interno
    - Mirror de imagens
    - Catalog mirror

### Observabilidade
11. [**Monitoramento e Logs**](11-monitoramento-logs.md)
    - Logs de pods e builds
    - Eventos
    - Métricas (top)

12. [**Must-Gather e Diagnóstico**](12-must-gather.md)
    - Coleta de dados
    - Must-gather para diferentes operadores
    - Inspecionar namespaces

### Troubleshooting
13. [**Troubleshooting de Pods**](13-troubleshooting-pods.md)
    - Debug de pods
    - Problemas comuns
    - OOMKilled e crashes

14. [**Troubleshooting de Rede**](14-troubleshooting-rede.md)
    - Conectividade
    - DNS
    - Services e routes

15. [**Troubleshooting de Storage**](15-troubleshooting-storage.md)
    - PVC stuck
    - Permissões
    - Storage classes

### Segurança e RBAC
16. [**Segurança e RBAC**](16-seguranca-rbac.md)
    - Service Accounts
    - Roles e RoleBindings
    - Security Context Constraints (SCC)
    - Permissões e políticas

### Administração Avançada
17. [**Cluster Operators**](17-cluster-operators.md)
    - Status dos operators
    - Troubleshooting
    - Versões

18. [**Nodes e Machine Config**](18-nodes-machine.md)
    - Gerenciar nodes
    - Cordon e drain
    - MachineConfig e MachineSets

19. [**Certificados e CSR**](19-certificados-csr.md)
    - Aprovar CSRs
    - Troubleshooting de certificados
    - Comandos em batch

20. [**Cluster Networking**](20-cluster-networking.md)
    - Network Policies
    - Ingress/Egress
    - SDN troubleshooting

21. [**Cluster Version e Updates**](21-cluster-version-updates.md)
    - Verificar versão do cluster
    - Atualizar cluster
    - Histórico de updates

22. [**ETCD Backup**](22-etcd-backup.md)
    - Backup de etcd
    - Restore de etcd
    - Disaster recovery

### Comandos Utilitários
23. [**Comandos Customizados com AWK, jq e GREP**](23-comandos-customizados.md)
    - Scripts com awk
    - Filtros com jq
    - Pipes complexos
    - Automação

24. [**Field Selectors e Filtros**](24-field-selectors.md)
    - Field selectors avançados
    - Filtros complexos
    - Combinações

25. [**Formatação de Output**](25-output-formatacao.md)
    - JSONPath
    - Custom columns
    - YAML e JSON

26. [**Templates e Manifests**](26-templates-manifests.md)
    - Templates de aplicação
    - Kustomize
    - Helm charts
    - Manifests YAML

### Operações e Manutenção
27. [**Backup e Disaster Recovery**](27-backup-disaster-recovery.md)
    - Exportar recursos
    - Backup de aplicações
    - Disaster recovery

28. [**Patch e Edit**](28-patch-edit.md)
    - Patch de recursos
    - Labels e annotations
    - Merge strategies

29. [**Jobs e CronJobs**](29-jobs-cronjobs.md)
    - Criar jobs
    - Agendar tarefas
    - Troubleshooting

30. [**Operators e Operandos**](30-operators-operandos.md)
    - Operator Lifecycle Manager
    - Instalar operators
    - Troubleshooting

31. [**Troubleshooting de Upgrade do Cluster**](31-troubleshooting-upgrade.md)
    - Verificação de estado do upgrade
    - Cluster Version Operator
    - Cluster Operators com problemas
    - Machine Config Pools
    - Recovery de upgrade

---

## Busca Rápida por Comando

### Comandos Mais Usados

| Comando | Descrição |
|---------|-----------|
| `oc get pods -A \| grep -Ev "Running\|Completed"` | Listar pods com problemas |
| `oc get csr -o name \| xargs oc adm certificate approve` | Aprovar todos os CSRs pendentes |
| `oc get co \| grep -v "True.*False.*False"` | Ver cluster operators com problemas |
| `oc adm must-gather` | Must-gather básico |
| `oc logs <pod> --previous` | Ver logs de um pod crasheado |
| `oc debug node/<node-name>` | Debug de um node |
| `oc get events --field-selector type=Warning` | Listar eventos de erro |

---

## Dicas Gerais

### Watch Commands
```bash
# Ver pods em tempo real
watch -n 2 oc get pods

# Ver eventos em tempo real
oc get events --watch
```

### Comandos de Aprovação em Batch
```bash
# Aprovar todos os CSRs pendentes
oc get csr | grep Pending | awk '{print $1}' | xargs oc adm certificate approve

# Deletar pods com erro
oc get pods -A | grep Error | awk '{print $1" "$2}' | xargs -n2 sh -c 'oc delete pod $1 -n $0'
```

---

## Estrutura do Projeto

Este repositório está organizado em módulos de documentação numerados (01-31), cada um focado em um aspecto específico do OpenShift. Cada documento contém:

- Comandos básicos e avançados
- Exemplos práticos testados
- Dicas de troubleshooting
- Casos de uso reais

### Suíte de Testes Automatizados

O projeto inclui uma suíte completa de testes para validar todos os comandos documentados:

- **`tests/`**: Módulos de teste individuais para cada documento
- **`scripts/test-commands.sh`**: Script principal para executar os testes
- **`lib/common.sh`**: Funções compartilhadas para os testes

Para mais informações sobre os testes, consulte [`scripts/README.md`](scripts/README.md).

---

## Recursos Adicionais

- **Documentação Oficial**: https://docs.redhat.com/en/documentation/openshift_container_platform/
- **OpenShift CLI (oc) Reference**: https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html

---

## Contribuindo

Este guia é baseado em experiência prática e comandos reais testados em produção. Se você tiver sugestões ou novos comandos úteis, sinta-se à vontade para contribuir!

### Como Contribuir
1. Adicione ou modifique comandos nos documentos apropriados
2. Atualize os testes correspondentes em `tests/XX-topic/test.sh`
3. Execute a suíte de testes: `./scripts/test-commands.sh`
4. Submeta um pull request

---

## Navegação

- **Início Rápido**: [Top 20 Comandos →](INICIO-RAPIDO.md)
- **Primeiro Documento**: [Autenticação e Configuração →](01-autenticacao-configuracao.md)

---

**Última atualização**: Outubro 2025  
**Versão do OpenShift**: 4.19  
**Compatível com**: OpenShift 4.x
