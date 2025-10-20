# 🖥️ Nodes e Machine Config

Este documento contém comandos para gerenciar nodes e configurações de máquina no OpenShift.

---

## 📋 Índice

1. [Gerenciar Nodes](#gerenciar-nodes)
2. [Machine Config](#machine-config)
3. [Machine Sets](#machine-sets)
4. [Node Maintenance](#node-maintenance)

---

## 🖥️ Gerenciar Nodes

### Listar e Verificar
```bash
# Listar nodes
oc get nodes
```

```bash
# Com labels
oc get nodes --show-labels
```

```bash
# Wide output
oc get nodes -o wide
```

```bash
# Descrever node
oc describe node <node-name>
```

```bash
# Ver capacidade e uso
oc adm top nodes
```

```bash
# Ver versão do node
oc get node <node-name> -o jsonpath='{.status.nodeInfo.kubeletVersion}'
```

```bash
# Nodes por role
oc get nodes -l node-role.kubernetes.io/master
oc get nodes -l node-role.kubernetes.io/worker
```

### Labels e Taints
```bash
# Adicionar label
oc label node <node-name> <key>=<value>
```

```bash
# Remover label
oc label node <node-name> <key>-
```

```bash
# Ver taints
oc describe node <node-name> | grep Taints
```

```bash
# Adicionar taint
oc adm taint nodes <node-name> key=value:NoSchedule
```

```bash
# Remover taint
oc adm taint nodes <node-name> key:NoSchedule-
```

```bash
# Adicionar role label
oc label node <node-name> node-role.kubernetes.io/<role>=
```

### Drain e Cordon
```bash
# Cordon (desabilitar scheduling)
oc adm cordon <node-name>
```

```bash
# Uncordon (habilitar scheduling)
oc adm uncordon <node-name>
```

```bash
# Drain (esvaziar node)
oc adm drain <node-name>
```

```bash
# Drain com flags
oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

```bash
# Drain com grace period
oc adm drain <node-name> --grace-period=600
```

```bash
# Drain forçado (cuidado!)
oc adm drain <node-name> --force --delete-emptydir-data --ignore-daemonsets
```

### Debug de Nodes
```bash
# Debug interativo em node
oc debug node/<node-name>
```

```bash
# No shell de debug, acessar filesystem do host
chroot /host
```

```bash
# Ver logs do kubelet
oc adm node-logs <node-name> -u kubelet
```

```bash
# Ver logs do CRI-O
oc adm node-logs <node-name> -u crio
```

```bash
# Ver journal do node
oc adm node-logs <node-name> --tail=100
```

```bash
# Executar comando em node
oc debug node/<node-name> -- chroot /host <comando>
```

---

## ⚙️ Machine Config

### MachineConfigs
```bash
# Listar MachineConfigs
oc get machineconfigs
oc get mc
```

```bash
# Descrever MachineConfig
oc describe mc <mc-name>
```

```bash
# Ver conteúdo
oc get mc <mc-name> -o yaml
```

```bash
# MachineConfigs renderizados
oc get mc | grep rendered
```

### MachineConfigPools
```bash
# Listar MachineConfigPools
oc get machineconfigpools
oc get mcp
```

```bash
# Status dos pools
oc get mcp
```

```bash
# Master pool
oc get mcp master
```

```bash
# Worker pool
oc get mcp worker
```

```bash
# Descrever pool
oc describe mcp <pool-name>
```

```bash
# Ver progresso de update
oc get mcp
```

```bash
# Ver qual MC está sendo aplicado
oc get mcp <pool-name> -o jsonpath='{.status.configuration.name}'
```

### Criar MachineConfig
```bash
# Exemplo: criar arquivo no node
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

```bash
# Exemplo: adicionar registry inseguro
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
```bash
# Pausar MachineConfigPool
oc patch mcp <pool-name> --type merge -p '{"spec":{"paused":true}}'
```

```bash
# Despausar
oc patch mcp <pool-name> --type merge -p '{"spec":{"paused":false}}'
```

```bash
# Ver se está pausado
oc get mcp <pool-name> -o jsonpath='{.spec.paused}'
```

---

## 🏭 Machine Sets

### Gerenciar MachineSets
```bash
# Listar MachineSets
oc get machinesets -n openshift-machine-api
```

```bash
# Descrever MachineSet
oc describe machineset <name> -n openshift-machine-api
```

```bash
# Ver réplicas
oc get machineset <name> -n openshift-machine-api -o jsonpath='{.spec.replicas}'
```

```bash
# Escalar MachineSet
oc scale machineset <name> -n openshift-machine-api --replicas=<N>
```

```bash
# Ver Machines
oc get machines -n openshift-machine-api
```

```bash
# Descrever Machine
oc describe machine <machine-name> -n openshift-machine-api
```

### Criar MachineSet
```bash
# Copiar existente
oc get machineset <existing> -n openshift-machine-api -o yaml > new-machineset.yaml
```

```bash
# Editar e aplicar
# Mudar: nome, replicas, availability zone, etc
oc apply -f new-machineset.yaml
```

```bash
# Verificar
oc get machines -n openshift-machine-api
```

### Deletar Machines
```bash
# Deletar Machine (node será removido)
oc delete machine <machine-name> -n openshift-machine-api
```

```bash
# Ver processo
oc get machines -n openshift-machine-api
```

```bash
# Ver nodes
oc get nodes
```

---

## 🔧 Node Maintenance

### Atualizar Node
```bash
# 1. Cordon
oc adm cordon <node-name>
```

```bash
# 2. Drain
oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

```bash
# 3. Aplicar updates (MachineConfig ou manual)
# Node vai reiniciar automaticamente se MachineConfig mudou
```

```bash
# 4. Aguardar node voltar
oc get nodes
```

```bash
# 5. Uncordon
oc adm uncordon <node-name>
```

### Reboot de Nodes
```bash
# Via debug
oc debug node/<node-name>
chroot /host
systemctl reboot
```

```bash
# Aguardar
oc get nodes
```

### Remover Node
```bash
# 1. Drain
oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data --force
```

```bash
# 2. Deletar node
oc delete node <node-name>
```

```bash
# 3. Se usando Machine, deletar Machine também
oc delete machine <machine-name> -n openshift-machine-api
```

### Health Checks
```bash
# Ver condições do node
oc get node <node-name> -o json | jq '.status.conditions'
```

```bash
# Verificar Ready
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Ready" and .status!="True")) | .metadata.name'
```

```bash
# Ver disk pressure
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="DiskPressure" and .status=="True")) | .metadata.name'
```

```bash
# Ver memory pressure
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="MemoryPressure" and .status=="True")) | .metadata.name'
```

```bash
# Ver PID pressure
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="PIDPressure" and .status=="True")) | .metadata.name'
```

---

## 📖 Navegação

- [← Anterior: Cluster Operators](17-cluster-operators.md)
- [→ Próximo: Certificados CSR](19-certificados-csr.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
