# Monitoramento e Logs

Este documento contém comandos para monitoramento, métricas e logs no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Logs](#logs)
3. [Eventos](#eventos)
4. [Métricas e Top](#métricas-e-top)
5. [Prometheus e Alertas](#prometheus-e-alertas)
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## Logs

### Logs de Pods
```bash
# Exibir logs do pod especificado
oc logs my-pod
```

```bash ignore-test
# Acompanhar logs em tempo real do pod
oc logs -f my-pod
```

```bash
# Exibir logs de container específico do pod
# oc logs my-pod -c <container-name>
oc logs my-pod -c my-container
```

```bash
# Exibir últimas N linhas dos logs
oc logs my-pod --tail=100
```

```bash
# Exibir logs a partir de um período de tempo
oc logs my-pod --since=1h
oc logs my-pod --since-time=2025-01-01T00:00:00Z
```

```bash ignore-test
# Exibir logs da instância anterior do container (após crash)
oc logs my-pod --previous
oc logs my-pod -p
```

```bash
# Exibir logs do pod especificado
# oc logs deployment/<deployment-name>
oc logs deployment/test-app
```

```bash
# Exibir logs do pod especificado
oc logs my-pod --timestamps
```

### Logs do Cluster
```bash ignore-test
# Logs de node específico
oc adm node-logs <nome-do-node>
```

```bash ignore-test
# Logs do journal
oc adm node-logs <nome-do-node> -u kubelet
```

```bash ignore-test
# Logs do CRI-O
oc adm node-logs <nome-do-node> -u crio
```

---

## Eventos

### Visualizar Eventos
```bash
# Listar eventos do namespace atual
oc get events
```

```bash
# Listar eventos ordenados por campo específico
oc get events --sort-by='.lastTimestamp'
```

```bash ignore-test
# Eventos de um namespace específico
oc get events -n <namespace>
```

```bash
# Listar eventos de todos os namespaces do cluster
oc get events -A
```

```bash
# Listar eventos filtrados por campo específico
oc get events --field-selector involvedObject.name=my-pod
```

```bash
# Listar apenas eventos do tipo Warning
oc get events --field-selector type=Warning
```

```bash
# Listar eventos ordenados por campo específico
oc get events --field-selector involvedObject.kind=Pod --sort-by='.lastTimestamp' | tail -20
```

```bash
# Listar eventos do namespace atual
oc get events
```

---

## Métricas e Top

### Uso de Recursos
```bash
# Top nodes (CPU e memória)
# oc adm top <resource-name>
oc adm top nodes
```

```bash ignore-test
# Top nodes com labels
oc adm top nodes --selector=node-role.kubernetes.io/worker=""
```

```bash ignore-test
# Top pods
# oc adm top <resource-name>
oc adm top pods
```

```bash ignore-test
# Top pods de todos namespaces
oc adm top pods -A
```

```bash ignore-test
# Top pods com containers
oc adm top pods --containers
```

```bash ignore-test
# Ordenar por CPU
oc adm top pods --sort-by=cpu
```

```bash ignore-test
# Ordenar por memória
oc adm top pods --sort-by=memory
```

```bash ignore-test
# Top de um pod específico
# oc adm top <resource-name> my-pod
oc adm top pod my-pod
```

### Métricas Detalhadas
```bash ignore-test
# Ver uso atual vs requests/limits
oc describe node <nome-do-node> | grep -A 5 "Allocated resources"
```

```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o json | jq -r '.items[] | "\(.metadata.name) CPU:\(.spec.containers[0].resources.requests.cpu) MEM:\(.spec.containers[0].resources.requests.memory)"'
```

---

## Prometheus e Alertas

### Acessar Prometheus
```bash
# Ver route do Prometheus
oc get route -n openshift-monitoring
```

```bash
# Listar recurso de todos os namespaces do cluster
oc get prometheusrule -A
```

```bash
# Ver pods do monitoring
oc get pods -n openshift-monitoring
```

### Configurar Monitoring
```bash
# Aplicar configuração do arquivo YAML/JSON ao cluster
cat <<EOF | oc apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-monitoring-config
  namespace: openshift-monitoring
data:
  config.yaml: |
    enableUserWorkload: true
EOF
```

```bash ignore-test
# Exibir recurso "cluster-monitoring-config" em formato YAML
# oc get configmap <configmap-name> -n <namespace> -o yaml
oc get configmap cluster-monitoring-config -n openshift-monitoring -o yaml
```

```bash
# Ver status do monitoring
# oc get clusteroperator <resource-name>
oc get clusteroperator monitoring
```

### ServiceMonitor
```bash
# Listar recurso de todos os namespaces do cluster
oc get servicemonitor -A
```

```bash ignore-test
# Criar ServiceMonitor para app
cat <<EOF | oc apply -f -
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: <app-monitor>
spec:
  endpoints:
  - port: metrics
    interval: 30s
  selector:
    matchLabels:
      app: <nome-do-app>
EOF
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/monitoring">Monitoring - Monitoring overview</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/logging">Logging</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes</a>
---

---

## Navegação

- [← Anterior: Registry](10-registry-imagens.md)
- [→ Próximo: Must-Gather](12-must-gather.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
