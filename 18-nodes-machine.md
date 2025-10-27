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
```markdown
**Ação:** Listar todos os nodes do cluster
```

```bash
oc get nodes
```

```markdown
**Ação:** Listar nodes exibindo todas as labels
```

```bash
oc get nodes --show-labels
```

```markdown
**Ação:** Listar nodes com informações detalhadas
```

```bash
oc get nodes -o wide
```

```markdown
**Ação:** Descrever node
```

```bash ignore-test
oc describe node <node-name>
```

```markdown
**Ação:** Ver capacidade e uso
**Exemplo:** `oc adm top <resource-name>`
```

```bash
oc adm top nodes
```

```markdown
**Ação:** Ver versão do node
```

```bash ignore-test
oc get node <node-name> -o jsonpath='{.status.nodeInfo.kubeletVersion}'
```

```markdown
**Ação:** Listar nodes filtrados por label
```

```bash
oc get nodes -l node-role.kubernetes.io/master
oc get nodes -l node-role.kubernetes.io/worker
```

### Labels e Taints
```markdown
**Ação:** Adicionar label
```

```bash ignore-test
oc label node <node-name> <key>=<value>
```

```markdown
**Ação:** Remover label
```

```bash ignore-test
oc label node <node-name> <key>-
```

```markdown
**Ação:** Ver taints
```

```bash ignore-test
oc describe node <node-name> | grep Taints
```

```markdown
**Ação:** Adicionar taint
```

```bash ignore-test
oc adm taint nodes <node-name> key=value:NoSchedule
```

```markdown
**Ação:** Remover taint
```

```bash ignore-test
oc adm taint nodes <node-name> key:NoSchedule-
```

```markdown
**Ação:** Adicionar role label
```

```bash ignore-test
oc label node <node-name> node-role.kubernetes.io/<role>=
```

### Drain e Cordon
```markdown
**Ação:** Cordon (desabilitar scheduling)
```

```bash ignore-test
oc adm cordon <node-name>
```

```markdown
**Ação:** Uncordon (habilitar scheduling)
```

```bash ignore-test
oc adm uncordon <node-name>
```

```markdown
**Ação:** Drain (esvaziar node)
```

```bash ignore-test
oc adm drain <node-name>
```

```markdown
**Ação:** Drain com flags
```

```bash ignore-test
oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

```markdown
**Ação:** Drain com grace period
```

```bash ignore-test
oc adm drain <node-name> --grace-period=600
```

```markdown
**Ação:** Drain forçado (cuidado!)
```

```bash ignore-test
oc adm drain <node-name> --force --delete-emptydir-data --ignore-daemonsets
```

### Debug de Nodes
```markdown
**Ação:** Debug interativo em node
```

```bash ignore-test
oc debug node/<node-name>
```

```markdown
**Ação:** No shell de debug, acessar filesystem do host
```

```bash
chroot /host
```

```markdown
**Ação:** Ver logs do kubelet
```

```bash ignore-test
oc adm node-logs <node-name> -u kubelet
```

```markdown
**Ação:** Ver logs do CRI-O
```

```bash ignore-test
oc adm node-logs <node-name> -u crio
```

```markdown
**Ação:** Ver journal do node
```

```bash ignore-test
oc adm node-logs <node-name> --tail=100
```

```markdown
**Ação:** Executar comando em node
```

```bash ignore-test
oc debug node/<node-name> -- chroot /host <comando>
```

---

## Machine Config

### MachineConfigs
```markdown
**Ação:** Listar MachineConfigs
```

```bash
oc get machineconfigs
oc get mc
```

```markdown
**Ação:** Descrever MachineConfig
```

```bash ignore-test
oc describe mc <mc-name>
```

```markdown
**Ação:** Ver conteúdo
```

```bash ignore-test
oc get mc <mc-name> -o yaml
```

```markdown
**Ação:** MachineConfigs renderizados
```

```bash
oc get mc | grep rendered
```

### MachineConfigPools
```markdown
**Ação:** Listar MachineConfigPools
```

```bash
oc get machineconfigpools
oc get mcp
```

```markdown
**Ação:** Status dos pools
```

```bash
oc get mcp
```

```markdown
**Ação:** Master pool
**Exemplo:** `oc get mcp <resource-name>`
```

```bash
oc get mcp master
```

```markdown
**Ação:** Worker pool
**Exemplo:** `oc get mcp <resource-name>`
```

```bash
oc get mcp worker
```

```markdown
**Ação:** Descrever pool
```

```bash ignore-test
oc describe mcp <pool-name>
```

```markdown
**Ação:** Ver progresso de update
```

```bash
oc get mcp
```

```markdown
**Ação:** Ver qual MC está sendo aplicado
```

```bash ignore-test
oc get mcp <pool-name> -o jsonpath='{.status.configuration.name}'
```

### Criar MachineConfig
```markdown
* Exemplo: criar arquivo no node
```

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

```markdown
* Exemplo: adicionar registry inseguro
```

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
```markdown
**Ação:** Pausar MachineConfigPool
```

```bash ignore-test
oc patch mcp <pool-name> --type merge -p '{"spec":{"paused":true}}'
```

```markdown
**Ação:** Despausar
```

```bash ignore-test
oc patch mcp <pool-name> --type merge -p '{"spec":{"paused":false}}'
```

```markdown
**Ação:** Ver se está pausado
```

```bash ignore-test
oc get mcp <pool-name> -o jsonpath='{.spec.paused}'
```

---

## Machine Sets

### Gerenciar MachineSets
```markdown
**Ação:** Listar MachineSets
```

```bash
oc get machinesets -n openshift-machine-api
```

```markdown
**Ação:** Descrever MachineSet
```

```bash ignore-test
oc describe machineset <name> -n openshift-machine-api
```

```markdown
**Ação:** Ver réplicas
```

```bash ignore-test
oc get machineset <name> -n openshift-machine-api -o jsonpath='{.spec.replicas}'
```

```markdown
**Ação:** Escalar MachineSet
```

```bash ignore-test
oc scale machineset <name> -n openshift-machine-api --replicas=<N>
```

```markdown
**Ação:** Ver Machines
```

```bash
oc get machines -n openshift-machine-api
```

```markdown
**Ação:** Descrever Machine
```

```bash ignore-test
oc describe machine <machine-name> -n openshift-machine-api
```

### Criar MachineSet
```markdown
**Ação:** Copiar existente
```

```bash ignore-test
oc get machineset <existing> -n openshift-machine-api -o yaml > new-machineset.yaml
```

```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash ignore-test
oc apply -f new-machineset.yaml
```

```markdown
**Ação:** Verificar
```

```bash
oc get machines -n openshift-machine-api
```

### Deletar Machines
```markdown
**Ação:** Deletar Machine (node será removido)
```

```bash ignore-test
oc delete machine <machine-name> -n openshift-machine-api
```

```markdown
**Ação:** Ver processo
```

```bash
oc get machines -n openshift-machine-api
```

```markdown
**Ação:** Listar todos os nodes do cluster
```

```bash
oc get nodes
```

---

## Node Maintenance

### Atualizar Node
```markdown
**Ação:** 1. Cordon
```

```bash ignore-test
oc adm cordon <node-name>
```

```markdown
**Ação:** 2. Drain
```

```bash ignore-test
oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

```bash
# 3. Aplicar updates (MachineConfig ou manual)
# Node vai reiniciar automaticamente se MachineConfig mudou
```
```markdown
**Ação:** Listar todos os nodes do cluster
```

```bash
oc get nodes
```

```markdown
**Ação:** 5. Uncordon
```

```bash ignore-test
oc adm uncordon <node-name>
```

### Reboot de Nodes
```markdown
**Ação:** Via debug
```

```bash ignore-test
oc debug node/<node-name>
chroot /host
systemctl reboot
```

```markdown
**Ação:** Listar todos os nodes do cluster
```

```bash
oc get nodes
```

### Remover Node
```markdown
**Ação:** 1. Drain
```

```bash ignore-test
oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data --force
```

```markdown
**Ação:** 2. Deletar node
```

```bash ignore-test
oc delete node <node-name>
```

```markdown
**Ação:** 3. Se usando Machine, deletar Machine também
```

```bash ignore-test
oc delete machine <machine-name> -n openshift-machine-api
```

### Health Checks
```markdown
**Ação:** Ver condições do node
```

```bash ignore-test
oc get node <node-name> -o json | jq '.status.conditions'
```

```markdown
**Ação:** Exibir nodes em formato JSON
```

```bash ignore-test
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Ready" and .status!="True")) | .metadata.name'
```

```markdown
**Ação:** Exibir nodes em formato JSON
```

```bash ignore-test
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="DiskPressure" and .status=="True")) | .metadata.name'
```

```markdown
**Ação:** Exibir nodes em formato JSON
```

```bash ignore-test
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="MemoryPressure" and .status=="True")) | .metadata.name'
```

```markdown
**Ação:** Exibir nodes em formato JSON
```

```bash ignore-test
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="PIDPressure" and .status=="True")) | .metadata.name'
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/machine_management">Machine management</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes - Working with nodes</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration">Post-installation configuration</a>
---

---

## Navegação

- [← Anterior: Cluster Operators](17-cluster-operators.md)
- [→ Próximo: Certificados CSR](19-certificados-csr.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
