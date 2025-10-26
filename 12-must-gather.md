# Must-Gather e Diagnósticos

Este documento contém comandos para coleta de diagnósticos e troubleshooting no OpenShift.

---

## Índice

- [Must-Gather e Diagnósticos](#must-gather-e-diagnósticos)
  - [Índice](#índice)
  - [Must-Gather Básico](#must-gather-básico)
    - [Coletar Dados do Cluster](#coletar-dados-do-cluster)
    - [Coleta por Tempo](#coleta-por-tempo)
  - [Must-Gather Específico](#must-gather-específico)
    - [Must-Gather por Componente](#must-gather-por-componente)
  - [Inspect](#inspect)
    - [Inspecionar Recursos](#inspecionar-recursos)
    - [Múltiplos Recursos](#múltiplos-recursos)
  - [Diagnósticos Rápidos](#diagnósticos-rápidos)
    - [Verificações Básicas](#verificações-básicas)
    - [Coleta Rápida](#coleta-rápida)
  - [Documentação Oficial](#documentação-oficial)
  - [Navegação](#navegação)
---

## Must-Gather Básico

### Coletar Dados do Cluster
```bash ignore-test
# Must-gather padrão (coleta completa dos componentes padrões do OpenShift)
oc adm must-gather
```

```bash ignore-test
# Salvar em diretório específico
oc adm must-gather --dest-dir=/tmp/must-gather
```

```bash ignore-test
# Ver progresso
oc adm must-gather -v=4
```

```bash ignore-test
# Salvar arquivos em um diretório específico
oc adm must-gather --dest-dir=/tmp/must-gather
```

```bash ignore-test
# Ver pods do must-gather
oc get pods -n openshift-must-gather-*
```

### Coleta por Tempo
```bash ignore-test
# Coletar logs das últimas 2 horas
oc adm must-gather --since 2h
```

```bash ignore-test
# Executar o pod do must-gather no node <node-name>
oc adm must-gather --node-name=<node-name>
```

---

## Must-Gather Específico

### Must-Gather por Componente

Algumas vezes é necessário coletar informações de um componente específico (ex.: logging, network, storage, operator). Para as instruções oficiais por componente — incluindo qual imagem usar e quais argumentos são suportados por versão — consulte a KCS da Red Hat:
https://access.redhat.com/solutions/5459251

---

## Inspect

### Inspecionar Recursos
```bash ignore-test
# Inspect de namespace completo
oc adm inspect ns/<namespace> --dest-dir=/tmp/inspect
```

```bash ignore-test
# Captura dado de debugging para todos os
# os projetos dos cluster operators
oc adm inspect clusteroperators --dest-dir=/tmp/inspect
```

```bash ignore-test
# Inspect de nós
oc adm inspect nodes --dest-dir=/tmp/inspect
```

```bash ignore-test
# Inspect de recurso específico
# oc adm inspect <resource-name>/test-app --dest-dir=/tmp/inspect
oc adm inspect deployment/test-app --dest-dir=/tmp/inspect
```

```bash ignore-test
# Inspect com logs
oc adm inspect ns/<namespace> --since=2h --dest-dir=/tmp/inspect
```

### Múltiplos Recursos
```bash ignore-test
# Inspect de vários recursos
oc adm inspect \
  clusteroperators \
  nodes \
  clusterversion \
  --dest-dir=/tmp/inspect
```

```bash ignore-test
# Inspect all-namespaces
oc adm inspect ns -A --dest-dir=/tmp/inspect
```

---

## Diagnósticos Rápidos

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

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support">Support - Gathering data about your cluster</a>
---

---

## Navegação

- [← Anterior: Monitoramento e Logs](11-monitoramento-logs.md)
- [→ Próximo: Troubleshooting de Pods](13-troubleshooting-pods.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
