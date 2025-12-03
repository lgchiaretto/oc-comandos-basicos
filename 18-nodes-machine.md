# Nodes e Machine Config

Este documento contém comandos para gerenciar nodes e configurações de máquina no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Gerenciar Nodes](#gerenciar-nodes)
3. [Machine Config](#machine-config)
4. [Machine Sets](#machine-sets)
5. [Node Maintenance](#node-maintenance)
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## Gerenciar Nodes

### Listar e Verificar
**Listar todos os nodes do cluster**

```bash
oc get nodes
```

**Listar nodes exibindo todas as labels**

```bash
oc get nodes --show-labels
```

**Listar nodes com informações detalhadas**

```bash
oc get nodes -o wide
```

**Descrever node**

```bash ignore-test
oc describe node <node-name>
```

**Ver capacidade e uso**

```bash
oc adm top nodes
```

**Ver versão do node**

```bash ignore-test
oc get node <node-name> -o jsonpath='{.status.nodeInfo.kubeletVersion}'
```

**Listar nodes master**

```bash
oc get nodes -l node-role.kubernetes.io/master
```

**Listar nodes worker**

```bash
oc get nodes -l node-role.kubernetes.io/worker
```

### Labels e Taints
**Adicionar label**

```bash ignore-test
oc label node <node-name> <key>=<value>
```

**Remover label**

```bash ignore-test
oc label node <node-name> <key>-
```

**Exibir detalhes completos do node filtrando por taints**

```bash ignore-test
oc describe node <node-name> | grep Taints
```

**Adicionar taint**

```bash ignore-test
oc adm taint nodes <node-name> key=value:NoSchedule
```

**Remover taint**

```bash ignore-test
oc adm taint nodes <node-name> key:NoSchedule-
```

**Adicionar role label**

```bash ignore-test
oc label node <node-name> node-role.kubernetes.io/<role>=
```

### Drain e Cordon
**Cordon (desabilitar scheduling)**

```bash ignore-test
oc adm cordon <node-name>
```

**Uncordon (habilitar scheduling)**

```bash ignore-test
oc adm uncordon <node-name>
```

**Drain (esvaziar node)**

```bash ignore-test
oc adm drain <node-name>
```

**Drain com flags**

```bash ignore-test
oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

**Drain com grace period**

```bash ignore-test
oc adm drain <node-name> --grace-period=600
```

**Drain forçado (cuidado!)**

```bash ignore-test
oc adm drain <node-name> --force --delete-emptydir-data --ignore-daemonsets
```

### Debug de Nodes
**Debug interativo em node**

```bash ignore-test
oc debug node/<node-name>
```

**No shell de debug, acessar filesystem do host**

```bash
chroot /host
```

**Ver logs do kubelet**

```bash ignore-test
oc adm node-logs <node-name> -u kubelet
```

**Ver logs do CRI-O**

```bash ignore-test
oc adm node-logs <node-name> -u crio
```

**Ver journal do node**

```bash ignore-test
oc adm node-logs <node-name> --tail=100
```

**Executar comando em node**

```bash ignore-test
oc debug node/<node-name> -- chroot /host <comando>
```

---

## Machine Config

### MachineConfigs
**Listar MachineConfigs**

```bash
oc get machineconfigs
```

**Listar MachineConfigs (forma abreviada)**

```bash
oc get mc
```

**Descrever MachineConfig**

```bash ignore-test
oc describe mc <mc-name>
```

**Ver conteúdo**

```bash ignore-test
oc get mc <mc-name> -o yaml
```

**Listar recursos filtrando por Rendered**

```bash
oc get mc | grep rendered
```

### MachineConfigPools
**Listar MachineConfigPools**

```bash
oc get machineconfigpools
```

**Listar MachineConfigPools (forma abreviada)**

```bash
oc get mcp
```

**Status dos pools**

```bash
oc get mcp
```

**Master pool**

```bash
oc get mcp master
```

**Worker pool**

```bash
oc get mcp worker
```

**Descrever pool**

```bash
oc describe mcp worker
```

**Ver progresso de update**

```bash
oc get mcp
```

**Ver MachineConfig atualmente aplicado no pool worker**

```bash
oc get mcp worker -o jsonpath='{.status.configuration.name}'
```

### Criar MachineConfig
* Exemplo: criar arquivo no node

```bash
cat <<EOF | oc apply -f -
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  labels:
    machineconfiguration.openshift.io/role: worker
  name: 99-worker-custom
spec:
  config:
    ignition:
      version: 3.2.0
    storage:
      files:
      - contents:
          source: data:,custom%20config
        mode: 0644
        path: /etc/custom-config
EOF
```

**Adicionar registry inseguro**

```bash ignore-test
cat <<EOF | oc apply -f -
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  labels:
    machineconfiguration.openshift.io/role: worker
  name: 99-worker-insecure-registry
spec:
  config:
    ignition:
      version: 3.2.0
    storage:
      files:
      - contents:
          source: data:text/plain;charset=utf-8;base64,<base64-content>
        mode: 0644
        path: /etc/containers/registries.conf.d/99-insecure.conf
EOF
```

### Pause de Updates
**Pausar MachineConfigPool**

```bash
oc patch mcp worker --type merge -p '{"spec":{"paused":true}}'
```

**Despausar**

```bash
oc patch mcp worker --type merge -p '{"spec":{"paused":false}}'
```

**Ver se está pausado**

```bash
oc get mcp worker -o jsonpath='{.spec.paused}'
```

---

## Machine Sets

### Gerenciar MachineSets
**Listar MachineSets**

```bash
oc get machinesets -n openshift-machine-api
```

**Descrever MachineSet**

```bash ignore-test
oc describe machineset <name> -n openshift-machine-api
```

**Ver réplicas**

```bash ignore-test
oc get machineset <name> -n openshift-machine-api -o jsonpath='{.spec.replicas}'
```

**Escalar MachineSet**

```bash ignore-test
oc scale machineset <name> -n openshift-machine-api --replicas=<N>
```

**Ver Machines**

```bash
oc get machines -n openshift-machine-api
```

**Descrever Machine**

```bash ignore-test
oc describe machine <machine-name> -n openshift-machine-api
```

### Criar MachineSet
**Copiar existente**

```bash ignore-test
oc get machineset <existing> -n openshift-machine-api -o yaml > new-machineset.yaml
```

**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
oc apply -f new-machineset.yaml
```

**Verificar**

```bash
oc get machines -n openshift-machine-api
```

### Deletar Machines
**Deletar Machine (node será removido)**

```bash ignore-test
oc delete machine <machine-name> -n openshift-machine-api
```

**Ver processo**

```bash
oc get machines -n openshift-machine-api
```

**Listar todos os nodes do cluster**

```bash
oc get nodes
```

---

## Node Maintenance

### Atualizar Node
**1. Cordon**

```bash ignore-test
oc adm cordon <node-name>
```

**2. Drain**

```bash ignore-test
oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

**Listar todos os nodes do cluster**

```bash
oc get nodes
```

**5. Uncordon**

```bash ignore-test
oc adm uncordon <node-name>
```

### Reboot de Nodes
**Via debug**

```bash ignore-test
oc debug node/<node-name>
chroot /host
systemctl reboot
```

**Listar todos os nodes do cluster**

```bash
oc get nodes
```

### Remover Node
**1. Drain**

```bash ignore-test
oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data --force
```

**2. Deletar node**

```bash ignore-test
oc delete node <node-name>
```

**3. Se usando Machine, deletar Machine também**

```bash ignore-test
oc delete machine <machine-name> -n openshift-machine-api
```

### Health Checks
**Ver condições do node**

```bash ignore-test
oc get node <node-name> -o json | jq '.status.conditions'
```

**Listar nodes que NÃO estão Ready (com problemas)**

```bash
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Ready" and .status!="True")) | .metadata.name'
```

**Listar nodes com pressão de disco (disco cheio)**

```bash
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="DiskPressure" and .status=="True")) | .metadata.name'
```

**Listar nodes com pressão de memória (memória baixa)**

```bash
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="MemoryPressure" and .status=="True")) | .metadata.name'
```

**Listar nodes com pressão de PIDs (muitos processos)**

```bash
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="PIDPressure" and .status=="True")) | .metadata.name'
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/machine_management">Machine management</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes - Working with nodes</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration">Post-installation configuration</a>
---


## Navegação

- [← Anterior: Cluster Operators](17-cluster-operators.md)
- [→ Próximo: Certificados CSR](19-certificados-csr.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Dezembro 2025
