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
```markdown
**Ação:** Exibir logs do pod especificado
```

```bash
oc logs my-pod
```

```markdown
**Ação:** Acompanhar logs em tempo real do pod
```

```bash ignore-test
oc logs -f my-pod
```

```markdown
**Ação:** Exibir logs de container específico do pod
**Exemplo:** `oc logs my-pod -c <container-name>`
```

```bash
oc logs my-pod -c my-container
```

```markdown
**Ação:** Exibir últimas N linhas dos logs
```

```bash
oc logs my-pod --tail=100
```

```markdown
**Ação:** Exibir logs a partir de um período de tempo
```

```bash
oc logs my-pod --since=1h
oc logs my-pod --since-time=2025-01-01T00:00:00Z
```

```markdown
**Ação:** Exibir logs da instância anterior do container (após crash)
```

```bash ignore-test
oc logs my-pod --previous
oc logs my-pod -p
```

```markdown
**Ação:** Exibir logs do pod especificado
**Exemplo:** `oc logs deployment/<deployment-name>`
```

```bash
oc logs deployment/test-app
```

```markdown
**Ação:** Exibir logs do pod especificado
```

```bash
oc logs my-pod --timestamps
```

### Logs do Cluster
```markdown
**Ação:** Logs de node específico
```

```bash ignore-test
oc adm node-logs <nome-do-node>
```

```markdown
**Ação:** Logs do journal
```

```bash ignore-test
oc adm node-logs <nome-do-node> -u kubelet
```

```markdown
**Ação:** Logs do CRI-O
```

```bash ignore-test
oc adm node-logs <nome-do-node> -u crio
```

---

## Eventos

### Visualizar Eventos
```markdown
**Ação:** Listar eventos do namespace atual
```

```bash
oc get events
```

```markdown
**Ação:** Listar eventos ordenados por campo específico
```

```bash
oc get events --sort-by='.lastTimestamp'
```

```markdown
**Ação:** Eventos de um namespace específico
```

```bash ignore-test
oc get events -n <namespace>
```

```markdown
**Ação:** Listar eventos de todos os namespaces do cluster
```

```bash
oc get events -A
```

```markdown
**Ação:** Listar eventos filtrados por campo específico
```

```bash
oc get events --field-selector involvedObject.name=my-pod
```

```markdown
**Ação:** Listar apenas eventos do tipo Warning
```

```bash
oc get events --field-selector type=Warning
```

```markdown
**Ação:** Listar eventos ordenados por campo específico
```

```bash
oc get events --field-selector involvedObject.kind=Pod --sort-by='.lastTimestamp' | tail -20
```

```markdown
**Ação:** Listar eventos do namespace atual
```

```bash
oc get events
```

---

## Métricas e Top

### Uso de Recursos
```markdown
**Ação:** Top nodes (CPU e memória)
**Exemplo:** `oc adm top <resource-name>`
```

```bash
oc adm top nodes
```

```markdown
**Ação:** Top nodes com labels
```

```bash ignore-test
oc adm top nodes --selector=node-role.kubernetes.io/worker=""
```

```markdown
**Ação:** Top pods
**Exemplo:** `oc adm top <resource-name>`
```

```bash ignore-test
oc adm top pods
```

```markdown
**Ação:** Top pods de todos namespaces
```

```bash ignore-test
oc adm top pods -A
```

```markdown
**Ação:** Top pods com containers
```

```bash ignore-test
oc adm top pods --containers
```

```markdown
**Ação:** Ordenar por CPU
```

```bash ignore-test
oc adm top pods --sort-by=cpu
```

```markdown
**Ação:** Ordenar por memória
```

```bash ignore-test
oc adm top pods --sort-by=memory
```

```markdown
**Ação:** Top de um pod específico
**Exemplo:** `oc adm top <resource-name> my-pod`
```

```bash ignore-test
oc adm top pod my-pod
```

### Métricas Detalhadas
```markdown
**Ação:** Ver uso atual vs requests/limits
```

```bash ignore-test
oc describe node <nome-do-node> | grep -A 5 "Allocated resources"
```

```markdown
**Ação:** Exibir pods em formato JSON
```

```bash ignore-test
oc get pods -o json | jq -r '.items[] | "\(.metadata.name) CPU:\(.spec.containers[0].resources.requests.cpu) MEM:\(.spec.containers[0].resources.requests.memory)"'
```

---

## Prometheus e Alertas

### Acessar Prometheus
```markdown
**Ação:** Ver route do Prometheus
```

```bash
oc get route -n openshift-monitoring
```

```markdown
**Ação:** Listar recurso de todos os namespaces do cluster
```

```bash
oc get prometheusrule -A
```

```markdown
**Ação:** Ver pods do monitoring
```

```bash
oc get pods -n openshift-monitoring
```

### Configurar Monitoring
```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

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

```markdown
**Ação:** Exibir recurso "cluster-monitoring-config" em formato YAML
**Exemplo:** `oc get configmap <configmap-name> -n <namespace> -o yaml`
```

```bash ignore-test
oc get configmap cluster-monitoring-config -n openshift-monitoring -o yaml
```

```markdown
**Ação:** Ver status do monitoring
**Exemplo:** `oc get clusteroperator <resource-name>`
```

```bash
oc get clusteroperator monitoring
```

### ServiceMonitor
```markdown
**Ação:** Listar recurso de todos os namespaces do cluster
```

```bash
oc get servicemonitor -A
```

```markdown
**Ação:** Criar ServiceMonitor para app
```

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

---

## Navegação

- [← Anterior: Registry](10-registry-imagens.md)
- [→ Próximo: Must-Gather](12-must-gather.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
