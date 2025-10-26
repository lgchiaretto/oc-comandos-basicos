# Guia Completo de Comandos do OpenShift

Este é um guia abrangente de comandos do OpenShift (OCP) organizado por categoria, incluindo comandos básicos e avançados para troubleshooting e administração.

---

## Como Usar Este Guia

### Para Iniciantes
Comece pelos documentos essenciais (1-6) para entender os conceitos básicos do OpenShift.

### Para Administradores
Foque nos documentos de administração avançada (19-22) e troubleshooting (13-15).

### Para DevOps
Concentre-se em Build/CI/CD (9-10), aplicações (3) e observabilidade (11-12).

### Para Troubleshooting
Vá direto para os documentos de troubleshooting (13-15) e must-gather (12).

---

## Categorias de Comandos

### Por Recurso
- **Pods**: Documentos 4, 13
- **Deployments**: Documento 5
- **Services**: Documento 6
- **Storage**: Documentos 8, 15
- **Nodes**: Documento 20

### Por Função
- **Criação**: Documentos 2, 3, 7, 9
- **Troubleshooting**: Documentos 13, 14, 15
- **Monitoramento**: Documentos 11, 12
- **Segurança**: Documentos 16, 17, 18

### Por Nível
- **Básico**: Documentos 1-6
- **Intermediário**: Documentos 7-12
- **Avançado**: Documentos 13-22
- **Expert**: Documentos 23-30

---

## Importante

> **Nota**: Sempre teste comandos destrutivos (delete, drain, etc.) em ambientes não produtivos antes de executar em produção.
> 
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
   - Templates de projeto

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
16. [**Usuários e Permissões**](16-usuarios-permissoes.md)
    - Service Accounts
    - Roles e RoleBindings
    - RBAC

17. [**Grupos e LDAP**](17-grupos-ldap.md)
    - Criar grupos
    - Sincronização LDAP/AD
    - Whitelist

18. [**Security Context Constraints**](18-scc.md)
    - Listar SCCs
    - Adicionar SCCs
    - Troubleshooting SCC

### Administração Avançada
19. [**Cluster Operators**](19-cluster-operators.md)
    - Status dos operators
    - Troubleshooting
    - Versões

20. [**Nodes e Machines**](20-nodes-machines.md)
    - Gerenciar nodes
    - Cordon e drain
    - MachineConfig e MachineSets

21. [**Certificate Signing Requests**](21-csr.md)
    - Aprovar CSRs
    - Troubleshooting de certificados
    - Comandos em batch

22. [**Networking Avançado**](22-networking.md)
    - Network Policies
    - Ingress/Egress
    - SDN troubleshooting

### Comandos Utilitários
23. [**Comandos Customizados com AWK, JQ e GREP**](23-comandos-customizados.md)
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

26. [**Templates**](26-templates.md)
    - Templates de aplicação
    - Templates de projeto
    - Templates de login

### Operações e Manutenção
27. [**Backup e Restore**](27-backup-restore.md)
    - Exportar recursos
    - Backup de etcd
    - Disaster recovery

28. [**Patch e Updates**](28-patch-updates.md)
    - Patch de recursos
    - Labels e annotations
    - Merge strategies

29. [**Jobs e CronJobs**](29-jobs-cronjobs.md)
    - Criar jobs
    - Agendar tarefas
    - Troubleshooting

30. [**Operators e OLM**](30-operators-olm.md)
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

```bash
# Listar pods com problemas
oc get pods -A | grep -E -v "Running|Completed"

# Aprovar todos os CSRs pendentes
oc get csr -o name | xargs oc adm certificate approve

# Ver cluster operators com problemas
oc get co | grep -v "True.*False.*False"

# Must-gather básico
oc adm must-gather

# Ver logs de um pod crasheado
oc logs <pod> --previous

# Debug de um node
oc debug node/<node-name>

# Listar eventos de erro
oc get events --field-selector type=Warning
```

---

## Dicas Gerais

### Watch Commands
```bash
# Ver pods em tempo real
watch -n 2 oc get pods

# Ver eventos em tempo real
oc get events --watch
```

---

## Recursos Adicionais

- **Documentação Oficial**: https://docs.redhat.com/en/documentation/openshift_container_platform/

---

## Contribuindo

Este guia é baseado em experiência prática e comandos reais. Se você tiver sugestões ou novos comandos úteis, sinta-se à vontade para contribuir!

---

## Navegação

- **Próximo**: [Autenticação e Configuração →](01-autenticacao-configuracao.md)
- **Ver todos os documentos**: Lista acima

---

**Última atualização**: Outubro 2025
**Versão do OpenShift**: 4.19
