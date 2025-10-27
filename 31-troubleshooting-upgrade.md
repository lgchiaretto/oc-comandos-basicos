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

### Verificar motivo dos nodes não sairem de SchedulingDisabled

**Ação:** Verificar se tem anotações no node (analise se  currentConfig está ok, verifique se não tem nenhuma anotação do Machine Config Operator)
* Esse é importante se o seu node está há muito tempo em SchedulingDisabled e não continua o upgrade

```bash ignore-test
oc describe node <node-name> | awk '/^Annotations:/ {flag=1} flag && /^[A-Z]/ && !/^Annotations:/ {flag=0} flag'
```

**Ação:** Verificar se tem pods prendendo o node (analise se tem pods que não são OCP ou pods do OCP que usam algum tipo de PVC)
* Esse é importante se o seu node está há muito tempo em SchedulingDisabled e não continua o upgrade

```bash ignore-test
oc describe node <node-name> | awk '/Non-terminated Pods:/{flag=1;next}/Allocated resources:/{flag=0}flag'
```

**Ação:** Analise os logs do machine-config-daemon (MCD) do node que esta travado
* substituir <node-name> pelo node travado

```bash ignore-test
oc logs -n openshift-machine-config-operator $(oc get pods -n openshift-machine-config-operator -l k8s-app=machine-config-daemon --field-selector spec.nodeName=<node-name> -o jsonpath='{.items[0].metadata.name}')
```

### Versão e Canal Atual

**Ação:** Exibir versão e status de atualização do cluster

```bash
oc get clusterversion
```

**Ação:** Exibir recurso "version" em formato YAML

```bash
oc get clusterversion version -o yaml
```

**Ação:** Exibir recurso em formato JSON

```bash
oc get clusterversion -o jsonpath='{.items[0].spec.channel}{"\n"}'
```

**Ação:** Exibir recurso em formato JSON

```bash
oc get clusterversion -o jsonpath='{.items[0].spec.desiredUpdate}{"\n"}'
```

### Status do Upgrade

**Ação:** Exibir recurso em formato JSON

```bash
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")]}{"\n"}' | jq
```

**Ação:** Verificar se há upgrade disponível

```bash
oc adm upgrade
```

**Ação:** Exibir recurso em formato JSON

```bash
oc get clusterversion -o jsonpath='{.items[0].status.history}' | jq
```

**Ação:** Exibir recurso em formato JSON

```bash
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].message}{"\n"}'
```

### Condições de Saúde

**Ação:** Exibir recurso em formato JSON

```bash
oc get clusterversion -o json | jq '.items[0].status.conditions'
```

**Ação:** Exibir recurso em formato JSON

```bash
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Available")]}{"\n"}' | jq
```

**Ação:** Exibir recurso em formato JSON

```bash
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Failing")]}{"\n"}' | jq
```

**Ação:** Exibir recurso em formato JSON

```bash
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="RetrieveUpdatesFailing")]}{"\n"}' | jq
```

---

## Cluster Version Operator

### Status do CVO

**Ação:** Verificar pod do Cluster Version Operator

```bash
oc get pods -n openshift-cluster-version
```

**Ação:** Exibir últimas N linhas dos logs
**Exemplo:** `oc logs -n <namespace> deployments/cluster-version-operator --tail=100`

```bash
oc logs -n openshift-cluster-version deployments/cluster-version-operator --tail=100
```

**Ação:** Acompanhar logs em tempo real do pod
**Exemplo:** `oc logs -n <namespace> deployments/cluster-version-operator -f`

```bash ignore-test
oc logs -n openshift-cluster-version deployments/cluster-version-operator -f
```

**Ação:** Verificar recursos do CVO

```bash
oc get all -n openshift-cluster-version
```

### Overrides do CVO

**Ação:** Exibir recurso "version" em formato JSON

```bash
oc get clusterversion version -o json | jq '.spec.overrides'
```

**Ação:** Exibir recurso "version" em formato JSON

```bash
oc get clusterversion version -o jsonpath='{.spec.overrides[*].name}{"\n"}'
```

**Ação:** Aplicar JSON patch ao recurso

```bash ignore-test
oc patch clusterversion version --type=json -p '[{"op":"remove","path":"/spec/overrides"}]'
```

---

## Cluster Operators com Problemas

### Status Geral dos Operadores

**Ação:** Listar status de todos os cluster operators

```bash
oc get co
```

**Ação:** Exibir cluster operator em formato JSON

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Available" and .status!="True")) | .metadata.name'
```

**Ação:** Exibir cluster operator em formato JSON

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

**Ação:** Exibir cluster operator em formato JSON

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Progressing" and .status=="True")) | .metadata.name'
```

**Ação:** Operadores com problemas (resumo)

```bash
oc get co | grep -v "True.*False.*False"
```

### Análise Detalhada de Operadores

* Exemplo: Verificar authentication operator

```bash
oc get co authentication -o yaml
```

**Ação:** Exibir cluster operator "authentication" em formato JSON

```bash
oc get co authentication -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}{"\n"}'
```

**Ação:** Exibir cluster operator "authentication" em formato JSON

```bash
oc get co authentication -o jsonpath='Atual: {.status.versions[0].version}{"\n"}Desejada: {.status.desiredVersion}{"\n"}'
```

### Operadores Críticos para Upgrade

**Ação:** Verificar operadores essenciais

```bash
for op in kube-apiserver kube-controller-manager kube-scheduler openshift-apiserver etcd machine-config; do
  echo "=== $op ==="
  oc get co $op -o jsonpath='{"Available: "}{.status.conditions[?(@.type=="Available")].status}{" - Progressing: "}{.status.conditions[?(@.type=="Progressing")].status}{" - Degraded: "}{.status.conditions[?(@.type=="Degraded")].status}{"\n"}'
done
```

**Ação:** Exibir cluster operator "machine-config" em formato YAML
**Exemplo:** `oc get co <resource-name>config -o yaml`

```bash
oc get co machine-config -o yaml
```

**Ação:** Exibir cluster operator "network" em formato YAML

```bash
oc get co network -o yaml
```

---

## Verificação de Nodes

### Status dos Nodes

**Ação:** Listar todos os nodes do cluster

```bash
oc get nodes
```

**Ação:** Nodes que não estão Ready

```bash
oc get nodes | grep -v Ready
```

**Ação:** Listar nodes exibindo todas as labels

```bash
oc get nodes --show-labels
```

**Ação:** Verificar condições de um node

```bash ignore-test
oc describe node <node-name> | grep -A 10 Conditions
```

### Versões dos Nodes

**Ação:** Exibir nodes em formato JSON

```bash
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.kubeletVersion}{"\n"}{end}'
```

**Ação:** Exibir nodes em formato JSON

```bash
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.osImage}{"\n"}{end}'
```

**Ação:** Listar nodes com informações detalhadas

```bash
oc get nodes -o wide
```

---

## Machine Config Pools

### Status dos MCPs

**Ação:** Listar Machine Config Pools

```bash
oc get mcp
```

**Ação:** Exibir recurso "master" em formato YAML

```bash
oc get mcp master -o yaml
```

**Ação:** Exibir recurso "worker" em formato YAML

```bash
oc get mcp worker -o yaml
```

**Ação:** Exibir recurso em formato JSON

```bash
oc get mcp -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Updating" and .status=="True")) | .metadata.name'
```

**Ação:** Exibir recurso em formato JSON

```bash
oc get mcp -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

### Progresso da Atualização dos MCPs

**Ação:** Exibir recurso "worker" em formato JSON

```bash
oc get mcp worker -o jsonpath='Updated: {.status.updatedMachineCount}/{.status.machineCount}{"\n"}Degraded: {.status.degradedMachineCount}{"\n"}'
```

**Ação:** Exibir recurso "master" em formato JSON

```bash
oc get mcp master -o jsonpath='Updated: {.status.updatedMachineCount}/{.status.machineCount}{"\n"}Degraded: {.status.degradedMachineCount}{"\n"}'
```

**Ação:** Listar machines que ainda não foram atualizadas

```bash
oc get machines -n openshift-machine-api
```

### Machine Configs

**Ação:** Listar todas as machine configs

```bash
oc get mc
```

**Ação:** Exibir recurso "worker" em formato JSON

```bash
oc get mcp worker -o jsonpath='{.status.configuration.name}{"\n"}'
```

**Ação:** Comparar machine configs

```bash ignore-test
oc get mc <mc-name> -o yaml
```

---

## Logs e Diagnósticos

### Logs dos Componentes Críticos

**Ação:** Exibir últimas N linhas dos logs
**Exemplo:** `oc logs -n <namespace> -l app=openshift-kube-apiserver --tail=100`

```bash
oc logs -n openshift-kube-apiserver -l app=openshift-kube-apiserver --tail=100
```

**Ação:** Exibir últimas N linhas dos logs
**Exemplo:** `oc logs -n <namespace> -l app=etcd --tail=100`

```bash
oc logs -n openshift-etcd -l app=etcd --tail=100
```

**Ação:** Exibir últimas N linhas dos logs
**Exemplo:** `oc logs -n <namespace> -l k8s-app=machine-config-operator --tail=100`

```bash
oc logs -n openshift-machine-config-operator -l k8s-app=machine-config-operator --tail=100
```

**Ação:** Exibir últimas N linhas dos logs
**Exemplo:** `oc logs -n <namespace> -l k8s-app=machine-config-daemon --tail=50`

```bash
oc logs -n openshift-machine-config-operator -l k8s-app=machine-config-daemon --tail=50
```

### Events do Cluster

**Ação:** Listar eventos de todos os namespaces do cluster

```bash
oc get events -A --sort-by='.lastTimestamp' | tail -50
```

**Ação:** Listar eventos de todos os namespaces do cluster

```bash
oc get events -A --field-selector type=Warning
```

**Ação:** Listar eventos ordenados por campo específico

```bash
oc get events -n openshift-cluster-version --sort-by='.lastTimestamp'
```

### Must-Gather para Upgrade

**Ação:** Coletar dados de diagnóstico em diretório específico

```bash ignore-test
oc adm must-gather --dest-dir=/tmp/must-gather-upgrade
```

**Ação:** Coletar dados de diagnóstico em diretório específico

```bash ignore-test
oc adm must-gather --image=$(oc adm release info --image-for=network-tools) --dest-dir=/tmp/must-gather-network
```

**Ação:** Coletar dados de diagnóstico em diretório específico

```bash ignore-test
oc adm must-gather --image=$(oc adm release info --image-for=etcd) --dest-dir=/tmp/must-gather-etcd
```

---

## Condições de Bloqueio

### Verificar Bloqueios de Upgrade

**Ação:** Exibir recurso em formato JSON

```bash
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Upgradeable")]}{"\n"}' | jq
```

**Ação:** Exibir cluster operator em formato JSON

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Upgradeable" and .status=="False")) | .metadata.name'
```

**Ação:** Exibir cluster operator em formato JSON

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Upgradeable" and .status=="False")) | {name: .metadata.name, reason: .status.conditions[] | select(.type=="Upgradeable") | .reason, message: .status.conditions[] | select(.type=="Upgradeable") | .message}'
```

### Recursos que Impedem Upgrade

**Ação:** Listar pods de todos os namespaces do cluster

```bash
oc get pods -A | grep -E 'Error|CrashLoopBackOff|ImagePullBackOff'
```

**Ação:** Listar persistent volume claim de todos os namespaces do cluster

```bash
oc get pvc -A | grep Pending
```

**Ação:** Exibir nodes em formato JSON

```bash
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Ready" and .status!="True")) | .metadata.name'
```

**Ação:** Listar pods de todos os namespaces do cluster

```bash ignore-test
oc get pods -A | grep Evicted
```

### Resource Quota e Limits

**Ação:** Listar recurso de todos os namespaces do cluster

```bash
oc get resourcequotas -A
```

**Ação:** Listar recurso de todos os namespaces do cluster

```bash
oc get limitranges -A
```

**Ação:** Verificar uso de recursos nos nodes
**Exemplo:** `oc adm top <resource-name>`

```bash
oc adm top nodes
```

---

## Recovery de Upgrade

O processo de upgrade não possui uma função de recovery ou rollback.

Uma vez iniciado, o upgrade deve ser finalizado.

Em caso de falha, não tente reverter o processoee o procedimento correto é abrir imediatamente um chamado de suporte na Red Hat para tratar o incidente.
        
### Limpeza de Recursos Problemáticos

**Ação:** Deletar o pods especificado

```bash ignore-test
oc delete pods -A --field-selector=status.phase=Failed
```

**Ação:** Deletar o recurso especificado

```bash ignore-test
oc delete jobs -A --field-selector=status.successful=1
```

---

## Checklist de Troubleshooting

### 1. Verificações Iniciais

**Ação:** Exibir versão e status de atualização do cluster

```bash
oc get clusterversion
```

**Ação:** Listar status de todos os cluster operators

```bash
oc get co
```

**Ação:** Listar todos os nodes do cluster

```bash
oc get nodes
```

**Ação:** Verificar machine config pools

```bash
oc get mcp
```

**Ação:** Verificar se há operadores degraded

```bash
oc get co | grep -i false
```

### 2. Análise de Logs

**Ação:** Exibir últimas N linhas dos logs
**Exemplo:** `oc logs -n <namespace> deployment/cluster-version-operator --tail=200`

```bash
oc logs -n openshift-cluster-version deployment/cluster-version-operator --tail=200
```

**Ação:** Exibir cluster operator "authentication" em formato YAML

```bash ignore-test
oc get co authentication -o yaml
```

**Ação:** Logs de pods específicos

```bash ignore-test
oc logs -n <namespace> <pod-name> --tail=100
```

**Ação:** Listar eventos de todos os namespaces do cluster

```bash
oc get events -A --sort-by='.lastTimestamp' | tail -100
```

### 3. Verificação de Recursos

**Ação:** Capacidade dos nodes
**Exemplo:** `oc adm top <resource-name>`

```bash
oc adm top nodes
```

**Ação:** Listar pods de todos os namespaces do cluster

```bash
oc get pods -A | grep -v Running | grep -v Completed
```

**Ação:** Exibir detalhes completos do nodes

```bash
oc describe nodes | grep -A 5 "Allocated resources"
```

### 4. Ações Corretivas Comuns

**Ação:** Aprovar Certificate Signing Request (CSR)

```bash ignore-test
oc get csr -o name | xargs oc adm certificate approve
```

**Ação:** Reiniciar pods problemáticos

```bash ignore-test
oc delete pod -n <namespace> <pod-name>
```

**Ação:** Verificar MCPs

```bash
oc get mcp
```

**Ação:** Descrever MCP específico

```bash ignore-test
oc describe mcp <mcp-name>
```

### Watch em Tempo Real

**Ação:** Monitorar cluster version

```bash ignore-test
watch 'oc get clusterversion'
```

**Ação:** Monitorar cluster operators

```bash ignore-test
watch 'oc get co'
```

**Ação:** Monitorar nodes

```bash ignore-test
watch 'oc get nodes'
```

**Ação:** Monitorar MCPs

```bash ignore-test
watch 'oc get mcp'
```

**Ação:** Monitorar progresso geral

```bash ignore-test
watch -n 10 'echo "=== CLUSTER VERSION ===" && oc get clusterversion && echo "\n=== OPERATORS ===" && oc get co | grep -v "True.*False.*False" && echo "\n=== MCPS ===" && oc get mcp && echo "\n=== NODES ===" && oc get nodes'
```
**Ação:** Monitorar cluster version

```bash ignore-test
watch 'oc get clusterversion'
```
**Ação:** Monitorar cluster operators

```bash ignore-test
watch 'oc get co'
```

# Monitorar nodes
```bash ignore-test
watch 'oc get nodes'
```

### Monitoramento de Métricas

**Ação:** Verificar uso de CPU/Memory nos nodes

```bash ignore-test
watch -n 30 'oc adm top nodes'
```

**Ação:** Verificar pods com maior uso de recursos

```bash
oc adm top pods -A --sort-by=memory
```

**Ação:** Listar todos os Persistent Volumes do cluster

```bash
oc get pv
```

**Ação:** Listar persistent volume claim de todos os namespaces do cluster

```bash
oc get pvc -A
```

# Verificar pods com maior uso de recursos

```bash
oc adm top pods -A --sort-by=memory
```

# Verificar storage

```bash
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
