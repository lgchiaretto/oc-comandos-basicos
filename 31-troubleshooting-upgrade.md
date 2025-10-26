# 31 - Troubleshooting de Upgrade do Cluster

Comandos para diagnosticar e resolver problemas durante upgrades do OpenShift Container Platform

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

# Verificar detalhes completos da versão
oc get clusterversion version -o yaml

# Verificar canal de atualização configurado
oc get clusterversion -o jsonpath='{.items[0].spec.channel}{"\n"}'

# Verificar versão desejada (target)
oc get clusterversion -o jsonpath='{.items[0].spec.desiredUpdate}{"\n"}'
```

### Status do Upgrade

```bash
# Verificar progresso do upgrade
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")]}{"\n"}' | jq

# Verificar se há upgrade disponível
oc adm upgrade

# Histórico de upgrades
oc get clusterversion -o jsonpath='{.items[0].status.history}' | jq

# Verificar percentual de conclusão
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].message}{"\n"}'
```

### Condições de Saúde

```bash
# Verificar todas as condições do cluster version
oc get clusterversion -o json | jq '.items[0].status.conditions'

# Verificar condição Available
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Available")]}{"\n"}' | jq

# Verificar condição Failing
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Failing")]}{"\n"}' | jq

# Verificar condição RetrieveUpdatesFailing
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="RetrieveUpdatesFailing")]}{"\n"}' | jq
```

---

## Cluster Version Operator

### Status do CVO

```bash
# Verificar pod do Cluster Version Operator
oc get pods -n openshift-cluster-version

# Logs do CVO
oc logs -n openshift-cluster-version deployments/cluster-version-operator --tail=100

# Logs do CVO em tempo real
oc logs -n openshift-cluster-version deployments/cluster-version-operator -f

# Verificar recursos do CVO
oc get all -n openshift-cluster-version
```

### Overrides do CVO

```bash
# Verificar se há operadores com override (pausados)
oc get clusterversion version -o json | jq '.spec.overrides'

# Listar operadores em override
oc get clusterversion version -o jsonpath='{.spec.overrides[*].name}{"\n"}'

# Remover override de um operador específico
# CUIDADO: Só faça isso se souber o que está fazendo
# oc patch clusterversion version --type=json -p '[{"op":"remove","path":"/spec/overrides"}]'
```

---

## Cluster Operators com Problemas

### Status Geral dos Operadores

```bash
# Listar todos os cluster operators
oc get co

# Operadores que não estão Available
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Available" and .status!="True")) | .metadata.name'

# Operadores que estão Degraded
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'

# Operadores que estão Progressing
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Progressing" and .status=="True")) | .metadata.name'

# Operadores com problemas (resumo)
oc get co | grep -v "True.*False.*False"
```

### Análise Detalhada de Operadores

```bash
# Verificar detalhes de um operador específico
oc get co <operator-name> -o yaml

# Exemplo: Verificar authentication operator
oc get co authentication -o yaml

# Mensagens de erro de um operador
oc get co <operator-name> -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}{"\n"}'

# Versão atual vs desejada de um operador
oc get co <operator-name> -o jsonpath='Atual: {.status.versions[0].version}{"\n"}Desejada: {.status.desiredVersion}{"\n"}'
```

### Operadores Críticos para Upgrade

```bash
# Verificar operadores essenciais
for op in kube-apiserver kube-controller-manager kube-scheduler openshift-apiserver etcd; do
  echo "=== $op ==="
  oc get co $op -o jsonpath='{.status.conditions[?(@.type=="Available")].status}{" - "}{.status.conditions[?(@.type=="Degraded")].status}{"\n"}'
done

# Verificar Machine Config Operator
oc get co machine-config -o yaml

# Verificar Network Operator
oc get co network -o yaml
```

---

## Verificação de Nodes

### Status dos Nodes

```bash
# Listar todos os nodes
oc get nodes

# Nodes que não estão Ready
oc get nodes | grep -v Ready

# Verificar labels dos nodes
oc get nodes --show-labels

# Verificar condições de um node
oc describe node <node-name> | grep -A 10 Conditions
```

### Versões dos Nodes

```bash
# Verificar versões do kubelet em cada node
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.kubeletVersion}{"\n"}{end}'

# Verificar OS dos nodes
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.osImage}{"\n"}{end}'

# Nodes que ainda não foram atualizados
oc get nodes -o wide
```

---

## Machine Config Pools

### Status dos MCPs

```bash
# Listar Machine Config Pools
oc get mcp

# Verificar MCP master
oc get mcp master -o yaml

# Verificar MCP worker
oc get mcp worker -o yaml

# MCPs que estão atualizando
oc get mcp -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Updating" and .status=="True")) | .metadata.name'

# MCPs que estão degraded
oc get mcp -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

### Progresso da Atualização dos MCPs

```bash
# Verificar progresso de atualização dos workers
oc get mcp worker -o jsonpath='Updated: {.status.updatedMachineCount}/{.status.machineCount}{"\n"}Degraded: {.status.degradedMachineCount}{"\n"}'

# Verificar progresso de atualização dos masters
oc get mcp master -o jsonpath='Updated: {.status.updatedMachineCount}/{.status.machineCount}{"\n"}Degraded: {.status.degradedMachineCount}{"\n"}'

# Listar machines que ainda não foram atualizadas
oc get machines -n openshift-machine-api
```

### Machine Configs

```bash
# Listar todas as machine configs
oc get mc

# Verificar machine config atual do pool
oc get mcp worker -o jsonpath='{.status.configuration.name}{"\n"}'

# Comparar machine configs
oc get mc <mc-name> -o yaml
```

---

## Certificados e CSRs

### Pending CSRs

```bash
# Listar CSRs pendentes
oc get csr | grep Pending

# Aprovar todos os CSRs pendentes (nodes em upgrade)
oc get csr -o name | xargs oc adm certificate approve

# Aprovar CSRs pendentes individualmente
oc get csr | grep Pending | awk '{print $1}' | xargs -I {} oc adm certificate approve {}

# Verificar detalhes de um CSR
oc describe csr <csr-name>
```

### Certificados do Cluster

```bash
# Verificar certificados dos API servers
oc get secrets -n openshift-kube-apiserver | grep certificate

# Verificar validade dos certificados
oc get secrets -n openshift-kube-apiserver -o json | jq -r '.items[] | select(.type=="kubernetes.io/tls") | .metadata.name'

# Verificar certificados do etcd
oc get secrets -n openshift-etcd | grep etcd
```

---

## Logs e Diagnósticos

### Logs dos Componentes Críticos

```bash
# Logs do kube-apiserver
oc logs -n openshift-kube-apiserver -l app=openshift-kube-apiserver --tail=100

# Logs do etcd
oc logs -n openshift-etcd -l app=etcd --tail=100

# Logs do machine-config-operator
oc logs -n openshift-machine-config-operator -l k8s-app=machine-config-operator --tail=100

# Logs do machine-config-daemon (MCD)
oc logs -n openshift-machine-config-operator -l k8s-app=machine-config-daemon --tail=50
```

### Events do Cluster

```bash
# Events recentes de todos os namespaces
oc get events -A --sort-by='.lastTimestamp' | tail -50

# Events relacionados a upgrade
oc get events -A | grep -i upgrade

# Events de warning
oc get events -A --field-selector type=Warning

# Events de um namespace específico
oc get events -n openshift-cluster-version --sort-by='.lastTimestamp'
```

### Must-Gather para Upgrade

```bash
# Coletar must-gather para análise de upgrade
oc adm must-gather --dest-dir=/tmp/must-gather-upgrade

# Must-gather com foco em network (se suspeitar de problemas de rede)
oc adm must-gather --image=$(oc adm release info --image-for=network-tools) --dest-dir=/tmp/must-gather-network

# Must-gather para etcd
oc adm must-gather --image=$(oc adm release info --image-for=etcd) --dest-dir=/tmp/must-gather-etcd
```

---

## Condições de Bloqueio

### Verificar Bloqueios de Upgrade

```bash
# Verificar se há upgradeable=false
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Upgradeable")]}{"\n"}' | jq

# Listar operadores que bloqueiam upgrade
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Upgradeable" and .status=="False")) | .metadata.name'

# Verificar razão do bloqueio
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Upgradeable" and .status=="False")) | {name: .metadata.name, reason: .status.conditions[] | select(.type=="Upgradeable") | .reason, message: .status.conditions[] | select(.type=="Upgradeable") | .message}'
```

### Recursos que Impedem Upgrade

```bash
# Verificar pods em estado ruim
oc get pods -A | grep -E 'Error|CrashLoopBackOff|ImagePullBackOff'

# Verificar PVCs não vinculados
oc get pvc -A | grep Pending

# Verificar nodes com problemas
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Ready" and .status!="True")) | .metadata.name'

# Verificar se há pods evicted
oc get pods -A | grep Evicted
```

### Resource Quota e Limits

```bash
# Verificar resource quotas que podem estar bloqueando
oc get resourcequotas -A

# Verificar limit ranges
oc get limitranges -A

# Verificar uso de recursos nos nodes
oc adm top nodes
```

---

## Recovery de Upgrade

### Pausar/Retomar Upgrade

```bash ignore-test
# CUIDADO: Pausar upgrade (não recomendado, apenas em emergências)
# oc patch clusterversion version --type=merge -p '{"spec":{"overrides":[{"kind":"Deployment","group":"apps","name":"cluster-version-operator","namespace":"openshift-cluster-version","unmanaged":true}]}}'

# Verificar se o upgrade está pausado
oc get clusterversion -o jsonpath='{.spec.overrides}{"\n"}' | jq
```

### Rollback (Não Suportado Oficialmente)

```bash ignore-test
# ATENÇÃO: OpenShift não suporta rollback oficial de upgrades
# Se o upgrade falhar, a opção é corrigir os problemas e continuar

# Verificar histórico para entender o estado anterior
oc get clusterversion -o jsonpath='{.status.history}' | jq

# Em casos extremos, restaurar etcd de backup (requer procedimento específico)
# Consulte a documentação oficial da Red Hat
```

### Forçar Reconciliação

```bash
# Forçar reconciliação do cluster version
oc patch clusterversion version --type=merge -p '{"spec":{"desiredUpdate":null}}'

# Reiniciar o CVO
oc delete pod -n openshift-cluster-version -l app=cluster-version-operator

# Forçar reconciliação de um operador específico
oc delete pod -n <operator-namespace> -l <operator-label>
```

### Limpeza de Recursos Problemáticos

```bash
# Remover pods failed/evicted
oc delete pods -A --field-selector=status.phase=Failed

# Remover completed jobs antigos
oc delete jobs -A --field-selector=status.successful=1

# Limpar CSRs negados
oc get csr -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Denied")) | .metadata.name' | xargs oc delete csr
```

---

## Checklist de Troubleshooting

### 1. Verificações Iniciais

```bash
# Status geral do cluster
oc get clusterversion
oc get co
oc get nodes
oc get mcp

# Verificar se há operadores degraded
oc get co | grep -i false

# Verificar CSRs pendentes
oc get csr | grep Pending
```

### 2. Análise de Logs

```bash
# CVO logs
oc logs -n openshift-cluster-version deployment/cluster-version-operator --tail=200

# Operador com problema
oc get co <operator-name> -o yaml
oc logs -n <namespace> <pod-name> --tail=100

# Events recentes
oc get events -A --sort-by='.lastTimestamp' | tail -100
```

### 3. Verificação de Recursos

```bash
# Capacidade dos nodes
oc adm top nodes

# Pods com problemas
oc get pods -A | grep -v Running | grep -v Completed

# Verificar se há recursos suficientes
oc describe nodes | grep -A 5 "Allocated resources"
```

### 4. Ações Corretivas Comuns

```bash
# Aprovar CSRs pendentes
oc get csr -o name | xargs oc adm certificate approve

# Reiniciar pods problemáticos
oc delete pod -n <namespace> <pod-name>

# Verificar e corrigir MCPs
oc get mcp
oc describe mcp <mcp-name>

# Limpar recursos desnecessários
oc delete pods -A --field-selector=status.phase=Failed
oc delete pods -A --field-selector=status.phase=Succeeded
```

---

## Comandos de Monitoramento Contínuo

### Watch em Tempo Real

```bash
# Monitorar cluster version
watch -n 5 'oc get clusterversion'

# Monitorar cluster operators
watch -n 5 'oc get co'

# Monitorar nodes
watch -n 5 'oc get nodes'

# Monitorar MCPs
watch -n 5 'oc get mcp'

# Monitorar progresso geral
watch -n 10 'echo "=== CLUSTER VERSION ===" && oc get clusterversion && echo "\n=== OPERATORS ===" && oc get co | grep -v "True.*False.*False" && echo "\n=== MCPS ===" && oc get mcp && echo "\n=== NODES ===" && oc get nodes'
```

### Monitoramento de Métricas

```bash
# Verificar uso de CPU/Memory nos nodes
watch -n 30 'oc adm top nodes'

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
