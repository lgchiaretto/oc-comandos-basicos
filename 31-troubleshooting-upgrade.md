# 31 - Troubleshooting de Upgrade do Cluster

Comandos para diagnosticar e resolver problemas durante upgrades do OpenShift Container Platform. A grande maioria dos problemas de upgrade ocorrem durante o reboot dos nodes no momento em que o Machine Config Operator é atualizado e os nodes do cluster são reiniciados para aplicar a nova versão.

---

## Índice

1. [Verificação de Estado do Upgrade](#verificação-de-estado-do-upgrade)
2. [Cluster Version Operator](#cluster-version-operator)
3. [Cluster Operators com Problemas](#cluster-operators-com-problemas)
4. [Verificação de Nodes](#verificação-de-nodes)
5. [Machine Config Pools](#machine-config-pools)
6. [Certificados e CSRs](#certificados-e-csrs)
7. [Logs e Diagnósticos](#logs-e-diagnósticos)
8. [Condições de Bloqueio](#condições-de-bloqueio)
9. [Recovery de Upgrade](#recovery-de-upgrade)

---

## Verificação de Estado do Upgrade

### Versão e Canal Atual

```bash
# Verificar versão atual do cluster
oc get clusterversion
```

```bash
# Verificar detalhes completos da versão
oc get clusterversion version -o yaml
```

```bash
# Verificar canal de atualização configurado
oc get clusterversion -o jsonpath='{.items[0].spec.channel}{"\n"}'
```

```bash
# Verificar versão desejada (target)
oc get clusterversion -o jsonpath='{.items[0].spec.desiredUpdate}{"\n"}'
```

### Status do Upgrade

```bash
# Verificar progresso do upgrade
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")]}{"\n"}' | jq
```

```bash
# Verificar se há upgrade disponível
oc adm upgrade
```

```bash
# Histórico de upgrades
oc get clusterversion -o jsonpath='{.items[0].status.history}' | jq
```

```bash
# Verificar percentual de conclusão
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].message}{"\n"}'
```

### Condições de Saúde

```bash
# Verificar todas as condições do cluster version
oc get clusterversion -o json | jq '.items[0].status.conditions'
```

```bash
# Verificar condição Available
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Available")]}{"\n"}' | jq
```

```bash
# Verificar condição Failing
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Failing")]}{"\n"}' | jq
```

```bash
# Verificar condição RetrieveUpdatesFailing
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="RetrieveUpdatesFailing")]}{"\n"}' | jq
```

---

## Cluster Version Operator

### Status do CVO

```bash
# Verificar pod do Cluster Version Operator
oc get pods -n openshift-cluster-version
```

```bash
# Logs do CVO
# oc logs -n <namespace> deployments/cluster-version-operator --tail=100
oc logs -n openshift-cluster-version deployments/cluster-version-operator --tail=100
```

```bash ignore-test
# Logs do CVO em tempo real
# oc logs -n <namespace> deployments/cluster-version-operator -f
oc logs -n openshift-cluster-version deployments/cluster-version-operator -f
```

```bash
# Verificar recursos do CVO
oc get all -n openshift-cluster-version
```

### Overrides do CVO

```bash
# Verificar se há operadores com override (pausados)
oc get clusterversion version -o json | jq '.spec.overrides'
```

```bash
# Listar operadores em override
oc get clusterversion version -o jsonpath='{.spec.overrides[*].name}{"\n"}'
```

```bash ignore-test
# Remover override de um operador específico
# CUIDADO: Só faça isso se souber o que está fazendo
oc patch clusterversion version --type=json -p '[{"op":"remove","path":"/spec/overrides"}]'
```

---

## Cluster Operators com Problemas

### Status Geral dos Operadores

```bash
# Listar todos os cluster operators
oc get co
```

```bash
# Operadores que não estão Available
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Available" and .status!="True")) | .metadata.name'
```

```bash
# Operadores que estão Degraded
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

```bash
# Operadores que estão Progressing
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Progressing" and .status=="True")) | .metadata.name'
```

```bash
# Operadores com problemas (resumo)
oc get co | grep -v "True.*False.*False"
```

### Análise Detalhada de Operadores

```bash
# Exemplo: Verificar authentication operator
oc get co authentication -o yaml
```

```bash
# Mensagens de erro de um operador
oc get co authentication -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}{"\n"}'
```

```bash
# Versão atual vs desejada de um operador
oc get co authentication -o jsonpath='Atual: {.status.versions[0].version}{"\n"}Desejada: {.status.desiredVersion}{"\n"}'
```

### Operadores Críticos para Upgrade

```bash
# Verificar operadores essenciais
for op in kube-apiserver kube-controller-manager kube-scheduler openshift-apiserver etcd machine-config; do
  echo "=== $op ==="
  oc get co $op -o jsonpath='{"Available: "}{.status.conditions[?(@.type=="Available")].status}{" - Progressing: "}{.status.conditions[?(@.type=="Progressing")].status}{" - Degraded: "}{.status.conditions[?(@.type=="Degraded")].status}{"\n"}'
done
```

```bash
# Verificar Machine Config Operator
# oc get co <resource-name>config -o yaml
oc get co machine-config -o yaml
```

```bash
# Verificar Network Operator
oc get co network -o yaml
```

---

## Verificação de Nodes

### Status dos Nodes

```bash
# Listar todos os nodes
oc get nodes
```

```bash
# Nodes que não estão Ready
oc get nodes | grep -v Ready
```

```bash
# Verificar labels dos nodes
oc get nodes --show-labels
```

```bash ignore-test
# Verificar condições de um node
oc describe node <node-name> | grep -A 10 Conditions
```

```bash ignore-test
# Verificar se tem anotações no node (analise se  currentConfig está ok, verifique se não tem nenhuma anotação do Machine Config Operator)
# Esse é importante se o seu node está há muito tempo em SchedulingDisabled e não continua o upgrade
oc describe node <node-name> | awk '/^Annotations:/ {flag=1} flag && /^[A-Z]/ && !/^Annotations:/ {flag=0} flag'
```

### Versões dos Nodes

```bash
# Verificar versões do kubelet em cada node
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.kubeletVersion}{"\n"}{end}'
```

```bash
# Verificar OS dos nodes
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.osImage}{"\n"}{end}'
```

```bash
# Nodes que ainda não foram atualizados
oc get nodes -o wide
```

---

## Machine Config Pools

### Status dos MCPs

```bash
# Listar Machine Config Pools
oc get mcp
```

```bash
# Verificar MCP master
oc get mcp master -o yaml
```

```bash
# Verificar MCP worker
oc get mcp worker -o yaml
```

```bash
# MCPs que estão atualizando
oc get mcp -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Updating" and .status=="True")) | .metadata.name'
```

```bash
# MCPs que estão degraded
oc get mcp -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

### Progresso da Atualização dos MCPs

```bash
# Verificar progresso de atualização dos workers
oc get mcp worker -o jsonpath='Updated: {.status.updatedMachineCount}/{.status.machineCount}{"\n"}Degraded: {.status.degradedMachineCount}{"\n"}'
```

```bash
# Verificar progresso de atualização dos masters
oc get mcp master -o jsonpath='Updated: {.status.updatedMachineCount}/{.status.machineCount}{"\n"}Degraded: {.status.degradedMachineCount}{"\n"}'
```

```bash
# Listar machines que ainda não foram atualizadas
oc get machines -n openshift-machine-api
```

### Machine Configs

```bash
# Listar todas as machine configs
oc get mc
```

```bash
# Verificar machine config atual do pool
oc get mcp worker -o jsonpath='{.status.configuration.name}{"\n"}'
```

```bash ignore-test
# Comparar machine configs
oc get mc <mc-name> -o yaml
```

---

## Logs e Diagnósticos

### Logs dos Componentes Críticos

```bash
# Logs do kube-apiserver
# oc logs -n <namespace> -l app=openshift-kube-apiserver --tail=100
oc logs -n openshift-kube-apiserver -l app=openshift-kube-apiserver --tail=100
```

```bash
# Logs do etcd
# oc logs -n <namespace> -l app=etcd --tail=100
oc logs -n openshift-etcd -l app=etcd --tail=100
```

```bash
# Logs do machine-config-operator
# oc logs -n <namespace> -l k8s-app=machine-config-operator --tail=100
oc logs -n openshift-machine-config-operator -l k8s-app=machine-config-operator --tail=100
```

```bash
# Logs do machine-config-daemon (MCD)
# oc logs -n <namespace> -l k8s-app=machine-config-daemon --tail=50
oc logs -n openshift-machine-config-operator -l k8s-app=machine-config-daemon --tail=50
```

### Events do Cluster

```bash
# Events recentes de todos os namespaces
oc get events -A --sort-by='.lastTimestamp' | tail -50
```

```bash
# Events de warning
oc get events -A --field-selector type=Warning
```

```bash
# Events de um namespace específico
oc get events -n openshift-cluster-version --sort-by='.lastTimestamp'
```

### Must-Gather para Upgrade

```bash ignore-test
# Coletar must-gather para análise de upgrade
oc adm must-gather --dest-dir=/tmp/must-gather-upgrade
```

```bash ignore-test
# Must-gather com foco em network (se suspeitar de problemas de rede)
oc adm must-gather --image=$(oc adm release info --image-for=network-tools) --dest-dir=/tmp/must-gather-network
```

```bash ignore-test
# Must-gather para etcd
oc adm must-gather --image=$(oc adm release info --image-for=etcd) --dest-dir=/tmp/must-gather-etcd
```

---

## Condições de Bloqueio

### Verificar Bloqueios de Upgrade

```bash
# Verificar se há upgradeable=false
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Upgradeable")]}{"\n"}' | jq
```

```bash
# Listar operadores que bloqueiam upgrade
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Upgradeable" and .status=="False")) | .metadata.name'
```

```bash
# Verificar razão do bloqueio
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Upgradeable" and .status=="False")) | {name: .metadata.name, reason: .status.conditions[] | select(.type=="Upgradeable") | .reason, message: .status.conditions[] | select(.type=="Upgradeable") | .message}'
```

### Recursos que Impedem Upgrade

```bash
# Verificar pods em estado ruim
oc get pods -A | grep -E 'Error|CrashLoopBackOff|ImagePullBackOff'
```

```bash
# Verificar PVCs não vinculados
oc get pvc -A | grep Pending
```

```bash
# Verificar nodes com problemas
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Ready" and .status!="True")) | .metadata.name'
```

```bash ignore-test
# Verificar se há pods evicted
oc get pods -A | grep Evicted
```

### Resource Quota e Limits

```bash
# Verificar resource quotas que podem estar bloqueando
oc get resourcequotas -A
```

```bash
# Verificar limit ranges
oc get limitranges -A
```

```bash
# Verificar uso de recursos nos nodes
# oc adm top <resource-name>
oc adm top nodes
```

---

## Recovery de Upgrade

O processo de upgrade não possui uma função de recovery ou rollback.

Uma vez iniciado, o upgrade deve ser finalizado.

Em caso de falha, não tente reverter o processoee o procedimento correto é abrir imediatamente um chamado de suporte na Red Hat para tratar o incidente.
        
### Limpeza de Recursos Problemáticos

```bash ignore-test
# Remover pods failed/evicted
oc delete pods -A --field-selector=status.phase=Failed
```

```bash ignore-test
# Remover completed jobs antigos
oc delete jobs -A --field-selector=status.successful=1
```

---

## Checklist de Troubleshooting

### 1. Verificações Iniciais

```bash
# Status geral do cluster
oc get clusterversion
```

```bash
# Verificar cluster operators
oc get co
```

```bash
# Verificar nodes
oc get nodes
```

```bash
# Verificar machine config pools
oc get mcp
```

```bash
# Verificar se há operadores degraded
oc get co | grep -i false
```

### 2. Análise de Logs

```bash
# CVO logs
# oc logs -n <namespace> deployment/cluster-version-operator --tail=200
oc logs -n openshift-cluster-version deployment/cluster-version-operator --tail=200
```

```bash ignore-test
# Operador com problema
oc get co authentication -o yaml
```

```bash ignore-test
# Logs de pods específicos
oc logs -n <namespace> <pod-name> --tail=100
```

```bash
# Events recentes
oc get events -A --sort-by='.lastTimestamp' | tail -100
```

### 3. Verificação de Recursos

```bash
# Capacidade dos nodes
# oc adm top <resource-name>
oc adm top nodes
```

```bash
# Pods com problemas
oc get pods -A | grep -v Running | grep -v Completed
```

```bash
# Verificar se há recursos suficientes
oc describe nodes | grep -A 5 "Allocated resources"
```

### 4. Ações Corretivas Comuns

```bash ignore-test
# Aprovar CSRs pendentes
oc get csr -o name | xargs oc adm certificate approve
```

```bash ignore-test
# Reiniciar pods problemáticos
oc delete pod -n <namespace> <pod-name>
```

```bash
# Verificar MCPs
oc get mcp
```

```bash ignore-test
# Descrever MCP específico
oc describe mcp <mcp-name>
```

### Watch em Tempo Real

```bash ignore-test
# Monitorar cluster version
watch -n 5 'oc get clusterversion'
```

```bash ignore-test
# Monitorar cluster operators
watch -n 5 'oc get co'
```

```bash ignore-test
# Monitorar nodes
watch -n 5 'oc get nodes'
```

```bash ignore-test
# Monitorar MCPs
watch -n 5 'oc get mcp'
```

```bash ignore-test
# Monitorar progresso geral
watch -n 10 'echo "=== CLUSTER VERSION ===" && oc get clusterversion && echo "\n=== OPERATORS ===" && oc get co | grep -v "True.*False.*False" && echo "\n=== MCPS ===" && oc get mcp && echo "\n=== NODES ===" && oc get nodes'
```onitorar cluster version
watch -n 5 'oc get clusterversion'

# Monitorar cluster operators
watch -n 5 'oc get co'

# Monitorar nodes
watch -n 5 'oc get nodes'
### Monitoramento de Métricas

```bash ignore-test
# Verificar uso de CPU/Memory nos nodes
watch -n 30 'oc adm top nodes'
```

```bash
# Verificar pods com maior uso de recursos
oc adm top pods -A --sort-by=memory
```

```bash
# Verificar persistent volumes
oc get pv
```

```bash
# Verificar persistent volume claims
oc get pvc -A
```ch -n 30 'oc adm top nodes'

# Verificar pods com maior uso de recursos
oc adm top pods -A --sort-by=memory

# Verificar storage
oc get pv
oc get pvc -A
```

---

## Referências

- [Red Hat OpenShift Upgrades](https://docs.openshift.com/container-platform/latest/updating/index.html)
- [Troubleshooting Upgrades](https://docs.openshift.com/container-platform/latest/updating/troubleshooting-updates.html)
- [Understanding Cluster Version Operator](https://docs.openshift.com/container-platform/latest/updating/understanding_updates/understanding-update-channels-releases.html)

---

**Última atualização**: Outubro 2025  
**Versão**: OpenShift 4.x

[⬅️ Voltar para: 30 - Operators e Operandos](30-operators-operandos.md) | [🏠 Início](README.md)
