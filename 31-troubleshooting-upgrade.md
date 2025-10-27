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

```bash ignore-test
# Verificar se tem anotações no node (analise se  currentConfig está ok, verifique se não tem nenhuma anotação do Machine Config Operator)
# Esse é importante se o seu node está há muito tempo em SchedulingDisabled e não continua o upgrade
oc describe node <node-name> | awk '/^Annotations:/ {flag=1} flag && /^[A-Z]/ && !/^Annotations:/ {flag=0} flag'
```

```bash ignore-test
# Verificar se tem pods prendendo o node (analise se tem pods que não são OCP ou pods do OCP que usam algum tipo de PVC)
# Esse é importante se o seu node está há muito tempo em SchedulingDisabled e não continua o upgrade
oc describe node <node-name> | awk '/Non-terminated Pods:/{flag=1;next}/Allocated resources:/{flag=0}flag'
```

```bash ignore-test
# Analise os logs do machine-config-daemon (MCD) do node que esta travado
# substituir <node-name> pelo node travado
oc logs -n openshift-machine-config-operator $(oc get pods -n openshift-machine-config-operator -l k8s-app=machine-config-daemon --field-selector spec.nodeName=<node-name> -o jsonpath='{.items[0].metadata.name}')
```

### Versão e Canal Atual

```bash
# Exibir versão e status de atualização do cluster
oc get clusterversion
```

```bash
# Exibir recurso "version" em formato YAML
oc get clusterversion version -o yaml
```

```bash
# Exibir recurso em formato JSON
oc get clusterversion -o jsonpath='{.items[0].spec.channel}{"\n"}'
```

```bash
# Exibir recurso em formato JSON
oc get clusterversion -o jsonpath='{.items[0].spec.desiredUpdate}{"\n"}'
```

### Status do Upgrade

```bash
# Exibir recurso em formato JSON
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")]}{"\n"}' | jq
```

```bash
# Verificar se há upgrade disponível
oc adm upgrade
```

```bash
# Exibir recurso em formato JSON
oc get clusterversion -o jsonpath='{.items[0].status.history}' | jq
```

```bash
# Exibir recurso em formato JSON
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].message}{"\n"}'
```

### Condições de Saúde

```bash
# Exibir recurso em formato JSON
oc get clusterversion -o json | jq '.items[0].status.conditions'
```

```bash
# Exibir recurso em formato JSON
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Available")]}{"\n"}' | jq
```

```bash
# Exibir recurso em formato JSON
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Failing")]}{"\n"}' | jq
```

```bash
# Exibir recurso em formato JSON
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
# Exibir últimas N linhas dos logs
# oc logs -n <namespace> deployments/cluster-version-operator --tail=100
oc logs -n openshift-cluster-version deployments/cluster-version-operator --tail=100
```

```bash ignore-test
# Acompanhar logs em tempo real do pod
# oc logs -n <namespace> deployments/cluster-version-operator -f
oc logs -n openshift-cluster-version deployments/cluster-version-operator -f
```

```bash
# Verificar recursos do CVO
oc get all -n openshift-cluster-version
```

### Overrides do CVO

```bash
# Exibir recurso "version" em formato JSON
oc get clusterversion version -o json | jq '.spec.overrides'
```

```bash
# Exibir recurso "version" em formato JSON
oc get clusterversion version -o jsonpath='{.spec.overrides[*].name}{"\n"}'
```

```bash ignore-test
# Aplicar JSON patch ao recurso
oc patch clusterversion version --type=json -p '[{"op":"remove","path":"/spec/overrides"}]'
```

---

## Cluster Operators com Problemas

### Status Geral dos Operadores

```bash
# Listar status de todos os cluster operators
oc get co
```

```bash
# Exibir cluster operator em formato JSON
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Available" and .status!="True")) | .metadata.name'
```

```bash
# Exibir cluster operator em formato JSON
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

```bash
# Exibir cluster operator em formato JSON
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
# Exibir cluster operator "authentication" em formato JSON
oc get co authentication -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}{"\n"}'
```

```bash
# Exibir cluster operator "authentication" em formato JSON
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
# Exibir cluster operator "machine-config" em formato YAML
# oc get co <resource-name>config -o yaml
oc get co machine-config -o yaml
```

```bash
# Exibir cluster operator "network" em formato YAML
oc get co network -o yaml
```

---

## Verificação de Nodes

### Status dos Nodes

```bash
# Listar todos os nodes do cluster
oc get nodes
```

```bash
# Nodes que não estão Ready
oc get nodes | grep -v Ready
```

```bash
# Listar nodes exibindo todas as labels
oc get nodes --show-labels
```

```bash ignore-test
# Verificar condições de um node
oc describe node <node-name> | grep -A 10 Conditions
```

### Versões dos Nodes

```bash
# Exibir nodes em formato JSON
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.kubeletVersion}{"\n"}{end}'
```

```bash
# Exibir nodes em formato JSON
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.osImage}{"\n"}{end}'
```

```bash
# Listar nodes com informações detalhadas
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
# Exibir recurso "master" em formato YAML
oc get mcp master -o yaml
```

```bash
# Exibir recurso "worker" em formato YAML
oc get mcp worker -o yaml
```

```bash
# Exibir recurso em formato JSON
oc get mcp -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Updating" and .status=="True")) | .metadata.name'
```

```bash
# Exibir recurso em formato JSON
oc get mcp -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

### Progresso da Atualização dos MCPs

```bash
# Exibir recurso "worker" em formato JSON
oc get mcp worker -o jsonpath='Updated: {.status.updatedMachineCount}/{.status.machineCount}{"\n"}Degraded: {.status.degradedMachineCount}{"\n"}'
```

```bash
# Exibir recurso "master" em formato JSON
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
# Exibir recurso "worker" em formato JSON
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
# Exibir últimas N linhas dos logs
# oc logs -n <namespace> -l app=openshift-kube-apiserver --tail=100
oc logs -n openshift-kube-apiserver -l app=openshift-kube-apiserver --tail=100
```

```bash
# Exibir últimas N linhas dos logs
# oc logs -n <namespace> -l app=etcd --tail=100
oc logs -n openshift-etcd -l app=etcd --tail=100
```

```bash
# Exibir últimas N linhas dos logs
# oc logs -n <namespace> -l k8s-app=machine-config-operator --tail=100
oc logs -n openshift-machine-config-operator -l k8s-app=machine-config-operator --tail=100
```

```bash
# Exibir últimas N linhas dos logs
# oc logs -n <namespace> -l k8s-app=machine-config-daemon --tail=50
oc logs -n openshift-machine-config-operator -l k8s-app=machine-config-daemon --tail=50
```

### Events do Cluster

```bash
# Listar eventos de todos os namespaces do cluster
oc get events -A --sort-by='.lastTimestamp' | tail -50
```

```bash
# Listar eventos de todos os namespaces do cluster
oc get events -A --field-selector type=Warning
```

```bash
# Listar eventos ordenados por campo específico
oc get events -n openshift-cluster-version --sort-by='.lastTimestamp'
```

### Must-Gather para Upgrade

```bash ignore-test
# Coletar dados de diagnóstico em diretório específico
oc adm must-gather --dest-dir=/tmp/must-gather-upgrade
```

```bash ignore-test
# Coletar dados de diagnóstico em diretório específico
oc adm must-gather --image=$(oc adm release info --image-for=network-tools) --dest-dir=/tmp/must-gather-network
```

```bash ignore-test
# Coletar dados de diagnóstico em diretório específico
oc adm must-gather --image=$(oc adm release info --image-for=etcd) --dest-dir=/tmp/must-gather-etcd
```

---

## Condições de Bloqueio

### Verificar Bloqueios de Upgrade

```bash
# Exibir recurso em formato JSON
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Upgradeable")]}{"\n"}' | jq
```

```bash
# Exibir cluster operator em formato JSON
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Upgradeable" and .status=="False")) | .metadata.name'
```

```bash
# Exibir cluster operator em formato JSON
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Upgradeable" and .status=="False")) | {name: .metadata.name, reason: .status.conditions[] | select(.type=="Upgradeable") | .reason, message: .status.conditions[] | select(.type=="Upgradeable") | .message}'
```

### Recursos que Impedem Upgrade

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep -E 'Error|CrashLoopBackOff|ImagePullBackOff'
```

```bash
# Listar persistent volume claim de todos os namespaces do cluster
oc get pvc -A | grep Pending
```

```bash
# Exibir nodes em formato JSON
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Ready" and .status!="True")) | .metadata.name'
```

```bash ignore-test
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep Evicted
```

### Resource Quota e Limits

```bash
# Listar recurso de todos os namespaces do cluster
oc get resourcequotas -A
```

```bash
# Listar recurso de todos os namespaces do cluster
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
# Deletar o pods especificado
oc delete pods -A --field-selector=status.phase=Failed
```

```bash ignore-test
# Deletar o recurso especificado
oc delete jobs -A --field-selector=status.successful=1
```

---

## Checklist de Troubleshooting

### 1. Verificações Iniciais

```bash
# Exibir versão e status de atualização do cluster
oc get clusterversion
```

```bash
# Listar status de todos os cluster operators
oc get co
```

```bash
# Listar todos os nodes do cluster
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
# Exibir últimas N linhas dos logs
# oc logs -n <namespace> deployment/cluster-version-operator --tail=200
oc logs -n openshift-cluster-version deployment/cluster-version-operator --tail=200
```

```bash ignore-test
# Exibir cluster operator "authentication" em formato YAML
oc get co authentication -o yaml
```

```bash ignore-test
# Logs de pods específicos
oc logs -n <namespace> <pod-name> --tail=100
```

```bash
# Listar eventos de todos os namespaces do cluster
oc get events -A --sort-by='.lastTimestamp' | tail -100
```

### 3. Verificação de Recursos

```bash
# Capacidade dos nodes
# oc adm top <resource-name>
oc adm top nodes
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep -v Running | grep -v Completed
```

```bash
# Exibir detalhes completos do nodes
oc describe nodes | grep -A 5 "Allocated resources"
```

### 4. Ações Corretivas Comuns

```bash ignore-test
# Aprovar Certificate Signing Request (CSR)
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
watch 'oc get clusterversion'
```

```bash ignore-test
# Monitorar cluster operators
watch 'oc get co'
```

```bash ignore-test
# Monitorar nodes
watch 'oc get nodes'
```

```bash ignore-test
# Monitorar MCPs
watch 'oc get mcp'
```

```bash ignore-test
# Monitorar progresso geral
watch -n 10 'echo "=== CLUSTER VERSION ===" && oc get clusterversion && echo "\n=== OPERATORS ===" && oc get co | grep -v "True.*False.*False" && echo "\n=== MCPS ===" && oc get mcp && echo "\n=== NODES ===" && oc get nodes'
```
```bash ignore-test
# Monitorar cluster version
watch 'oc get clusterversion'
```
```bash ignore-test
# Monitorar cluster operators
watch 'oc get co'
```

# Monitorar nodes
```bash ignore-test
watch 'oc get nodes'
```

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
# Listar todos os Persistent Volumes do cluster
oc get pv
```

```bash
# Listar persistent volume claim de todos os namespaces do cluster
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
