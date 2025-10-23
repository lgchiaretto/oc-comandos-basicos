# 🔍 Must-Gather e Diagnósticos

Este documento contém comandos para coleta de diagnósticos e troubleshooting no OpenShift.

---

## 📋 Índice

1. [Must-Gather Básico](#must-gather-básico)
2. [Must-Gather Específico](#must-gather-específico)
3. [Análise de Logs](#análise-de-logs)
4. [Inspect](#inspect)

---

## 🩺 Must-Gather Básico

### Coletar Dados do Cluster
```bash
# Must-gather padrão (coleta completa)
oc adm must-gather
```

```bash
# Salvar em diretório específico
oc adm must-gather --dest-dir=/tmp/must-gather
```

```bash
# Ver progresso
oc adm must-gather --dest-dir=/tmp/must-gather -v=4
```

```bash
# Must-gather em background
oc adm must-gather --dest-dir=/tmp/must-gather &
```

```bash
# Ver pods do must-gather
oc get pods -n openshift-must-gather-*
```

### Coleta por Tempo
```bash
# Coletar logs das últimas 2 horas
oc adm must-gather -- /usr/bin/gather --since 2h
```

```bash ignore-test
# Coletar apenas logs específicos
oc adm must-gather --node-name=<node-name>
```

---

## 🎯 Must-Gather Específico

### Must-Gather por Componente
```bash
# Must-gather de rede (SDN/OVN)
oc adm must-gather --image=quay.io/openshift/origin-must-gather -- /usr/bin/gather_network
```

```bash
# Must-gather de storage
oc adm must-gather --image=registry.redhat.io/odf4/ocs-must-gather-rhel8:latest
```

```bash
# Must-gather de logging
oc adm must-gather --image=registry.redhat.io/openshift-logging/cluster-logging-rhel8-operator:latest
```

```bash
# Must-gather de Service Mesh
oc adm must-gather --image=registry.redhat.io/openshift-service-mesh/istio-must-gather-rhel8:latest
```

```bash
# Must-gather de operadores
oc adm must-gather --image=registry.redhat.io/openshift4/ose-must-gather:latest -- /usr/bin/gather_audit_logs
```

### Múltiplas Imagens
```bash
# Coletar de múltiplos componentes
oc adm must-gather \
  --image=registry.redhat.io/openshift4/ose-must-gather:latest \
  --image=registry.redhat.io/odf4/ocs-must-gather-rhel8:latest
```

---

## 📂 Análise de Logs

### Estrutura do Must-Gather
```bash
# Explorar estrutura
tree /tmp/must-gather
```

```bash ignore-test
# Ver logs de namespace específico
cd /tmp/must-gather/namespaces/<namespace>/
```

```bash ignore-test
# Ver logs de pods
cat /tmp/must-gather/namespaces/<namespace>/pods/<pod>/logs/current.log
```

```bash
# Ver eventos
cat /tmp/must-gather/cluster-scoped-resources/core/events.yaml
```

### Buscar Problemas
```bash
# Buscar erros
grep -r "error" /tmp/must-gather/
```

```bash
# Buscar warnings
grep -r "warning" /tmp/must-gather/
```

```bash
# Buscar crashes
grep -r "crash\|panic\|fatal" /tmp/must-gather/
```

```bash
# Buscar OOMKilled
grep -r "OOMKilled" /tmp/must-gather/
```

```bash
# Ver todos os eventos de erro
cat /tmp/must-gather/cluster-scoped-resources/core/events.yaml | grep -i error
```

---

## 🔬 Inspect

### Inspecionar Recursos
```bash ignore-test
# Inspect de namespace completo
oc adm inspect ns/<namespace> --dest-dir=/tmp/inspect
```

```bash
# Inspect de tipo de recurso
oc adm inspect clusteroperators --dest-dir=/tmp/inspect
```

```bash
# Inspect de nós
oc adm inspect nodes --dest-dir=/tmp/inspect
```

```bash
# Inspect de recurso específico
oc adm inspect deployment/test-app --dest-dir=/tmp/inspect
```

```bash ignore-test
# Inspect com logs
oc adm inspect ns/<namespace> --since=2h --dest-dir=/tmp/inspect
```

### Múltiplos Recursos
```bash
# Inspect de vários recursos
oc adm inspect \
  clusteroperators \
  nodes \
  clusterversion \
  --dest-dir=/tmp/inspect
```

```bash
# Inspect all-namespaces
oc adm inspect ns --all-namespaces --dest-dir=/tmp/inspect
```

---

## 🛠️ Diagnósticos Rápidos

### Verificações Básicas
```bash
# Status geral do cluster
oc get clusteroperators
oc get nodes
oc get clusterversion
```

```bash
# Pods com problema
oc get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded
```

```bash ignore-test
# Pods recentemente reiniciados
oc get pods -A --sort-by='.status.containerStatuses[0].restartCount' | tail -20
```

```bash
# Ver últimos eventos de erro
oc get events -A --field-selector type=Warning --sort-by='.lastTimestamp' | tail -20
```

```bash ignore-test
# Nodes com problemas
oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Ready" and .status!="True")) | .metadata.name'
```

### Coleta Rápida
```bash
# Script de diagnóstico rápido
cat > /tmp/quick-diag.sh << 'EOF'
#!/bin/bash
echo "=== Cluster Version ==="
oc get clusterversion
echo -e "\n=== Cluster Operators ==="
oc get co
echo -e "\n=== Nodes ==="
oc get nodes
echo -e "\n=== Degraded Pods ==="
oc get pods -A --field-selector=status.phase!=Running
echo -e "\n=== Recent Warnings ==="
oc get events -A --field-selector type=Warning --sort-by='.lastTimestamp' | tail -20
EOF
```

```bash
chmod +x /tmp/quick-diag.sh
/tmp/quick-diag.sh > /tmp/cluster-status.txt
```

---

## 📖 Navegação

- [← Anterior: Monitoramento e Logs](11-monitoramento-logs.md)
- [→ Próximo: Troubleshooting de Pods](13-troubleshooting-pods.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
