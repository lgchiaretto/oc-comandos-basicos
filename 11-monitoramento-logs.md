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
**Exibir logs do pod especificado**

```bash
oc logs my-pod
```

**Acompanhar logs em tempo real do pod**

```bash ignore-test
oc logs -f my-pod
```

**Exibir logs de container específico do pod**

```bash
oc logs my-pod -c my-container
```

**Exibir últimas N linhas dos logs**

```bash
oc logs my-pod --tail=100
```

**Exibir logs a partir de um período de tempo**

```bash
oc logs my-pod --since=1h
```

**Exibir logs a partir de uma data/hora específica**

```bash
oc logs my-pod --since-time=2025-01-01T00:00:00Z
```

**Exibir logs da instância anterior do container (após crash)**

```bash ignore-test
oc logs my-pod --previous
```

**Exibir logs da instância anterior do container (forma abreviada)**

```bash ignore-test
oc logs my-pod -p
```

**Exibir logs do pod especificado**

```bash
oc logs deployment/test-app
```

**Exibir logs do pod especificado**

```bash
oc logs my-pod --timestamps
```

### Logs do Cluster
**Logs de node específico**

```bash ignore-test
oc adm node-logs <nome-do-node>
```

**Logs do journal**

```bash ignore-test
oc adm node-logs <nome-do-node> -u kubelet
```

**Logs do CRI-O**

```bash ignore-test
oc adm node-logs <nome-do-node> -u crio
```

---

## Eventos

### Visualizar Eventos
**Listar eventos do namespace atual**

```bash
oc get events
```

**Listar eventos ordenados por campo específico**

```bash
oc get events --sort-by='.lastTimestamp'
```

**Eventos de um namespace específico**

```bash ignore-test
oc get events -n <namespace>
```

**Listar eventos de todos os namespaces do cluster**

```bash
oc get events -A
```

**Listar eventos filtrados por campo específico**

```bash
oc get events --field-selector involvedObject.name=my-pod
```

**Listar eventos filtrados por campo específico**

```bash
oc get events --field-selector type=Warning
```

**Listar eventos ordenados por campo específico**

```bash
oc get events --field-selector involvedObject.kind=Pod --sort-by='.lastTimestamp' | tail -20
```

**Listar eventos do namespace atual**

```bash
oc get events
```

---

## Métricas e Top

### Uso de Recursos
**Top nodes (CPU e memória)**

```bash
oc adm top nodes
```

**Top nodes com labels**

```bash ignore-test
oc adm top nodes --selector=node-role.kubernetes.io/worker=""
```

**Top pods**

```bash ignore-test
oc adm top pods
```

**Top pods de todos namespaces**

```bash ignore-test
oc adm top pods -A
```

**Top pods com containers**

```bash ignore-test
oc adm top pods --containers
```

**Ordenar por CPU**

```bash ignore-test
oc adm top pods --sort-by=cpu
```

**Ordenar por memória**

```bash ignore-test
oc adm top pods --sort-by=memory
```

**Top de um pod específico**

```bash ignore-test
oc adm top pod my-pod
```

### Métricas Detalhadas
**Exibir detalhes completos do node filtrando por Allocated resources**

```bash ignore-test
oc describe node <nome-do-node> | grep -A 5 "Allocated resources"
```

**Exibir pods em formato JSON completo**

```bash ignore-test
oc get pods -o json | jq -r '.items[] | "\(.metadata.name) CPU:\(.spec.containers[0].resources.requests.cpu) MEM:\(.spec.containers[0].resources.requests.memory)"'
```

---

## Prometheus e Alertas

### Acessar Prometheus
**Ver route do Prometheus**

```bash
oc get route -n openshift-monitoring
```

**Listar prometheusrule de todos os namespaces do cluster**

```bash
oc get prometheusrule -A
```

**Ver pods do monitoring**

```bash
oc get pods -n openshift-monitoring
```

### Configurar Monitoring
**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash
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

**Exibir recurso "cluster-monitoring-config" em formato YAML**

```bash ignore-test
oc get configmap cluster-monitoring-config -n openshift-monitoring -o yaml
```

**Ver status do monitoring**

```bash
oc get clusteroperator monitoring
```

### ServiceMonitor
**Listar servicemonitor de todos os namespaces do cluster**

```bash
oc get servicemonitor -A
```

**Criar ServiceMonitor para app**

```bash ignore-test
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


## Navegação

- [← Anterior: Registry](10-registry-imagens.md)
- [→ Próximo: Must-Gather](12-must-gather.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Dezembro 2025
