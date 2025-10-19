# 📊 Monitoramento e Logs

Este documento contém comandos para monitoramento, métricas e logs no OpenShift.

---

## 📋 Índice

1. [Logs](#logs)
2. [Eventos](#eventos)
3. [Métricas e Top](#métricas-e-top)
4. [Prometheus e Alertas](#prometheus-e-alertas)

---

## 📝 Logs

### Logs de Pods
```bash
# Ver logs de pod
oc logs <nome-do-pod>

# Seguir logs em tempo real
oc logs -f <nome-do-pod>

# Logs de container específico
oc logs <nome-do-pod> -c <nome-do-container>

# Últimas N linhas
oc logs <nome-do-pod> --tail=100

# Logs desde tempo específico
oc logs <nome-do-pod> --since=1h
oc logs <nome-do-pod> --since-time=2024-01-01T00:00:00Z

# Logs anteriores (pod crashado)
oc logs <nome-do-pod> --previous
oc logs <nome-do-pod> -p

# Todos os pods de um deployment
oc logs deployment/<nome-do-deployment>

# Logs com timestamps
oc logs <nome-do-pod> --timestamps
```

### Logs do Cluster
```bash
# Logs de node específico
oc adm node-logs <nome-do-node>

# Logs do journal
oc adm node-logs <nome-do-node> -u kubelet

# Logs do CRI-O
oc adm node-logs <nome-do-node> -u crio
```

---

## 🔔 Eventos

### Visualizar Eventos
```bash
# Todos os eventos
oc get events

# Eventos ordenados por tempo
oc get events --sort-by='.lastTimestamp'

# Eventos de um namespace específico
oc get events -n <namespace>

# Todos os namespaces
oc get events -A

# Eventos de um recurso específico
oc get events --field-selector involvedObject.name=<nome-do-pod>

# Eventos de warnings
oc get events --field-selector type=Warning

# Eventos recentes (última hora)
oc get events --field-selector involvedObject.kind=Pod --sort-by='.lastTimestamp' | tail -20

# Watch events em tempo real
oc get events -w
```

---

## 📈 Métricas e Top

### Uso de Recursos
```bash
# Top nodes (CPU e memória)
oc adm top nodes

# Top nodes com labels
oc adm top nodes --selector=<label>

# Top pods
oc adm top pods

# Top pods de todos namespaces
oc adm top pods -A

# Top pods com containers
oc adm top pods --containers

# Ordenar por CPU
oc adm top pods --sort-by=cpu

# Ordenar por memória
oc adm top pods --sort-by=memory

# Top de um pod específico
oc adm top pod <nome-do-pod>
```

### Métricas Detalhadas
```bash
# Ver uso atual vs requests/limits
oc describe node <nome-do-node> | grep -A 5 "Allocated resources"

# Ver uso de todos os pods
oc get pods -o json | jq -r '.items[] | "\(.metadata.name) CPU:\(.spec.containers[0].resources.requests.cpu) MEM:\(.spec.containers[0].resources.requests.memory)"'
```

---

## 🔥 Prometheus e Alertas

### Acessar Prometheus
```bash
# Ver route do Prometheus
oc get route -n openshift-monitoring

# Ver alertas ativos
oc get prometheusrule -A

# Ver configuração do Prometheus
oc get configmap cluster-monitoring-config -n openshift-monitoring -o yaml

# Ver pods do monitoring
oc get pods -n openshift-monitoring
```

### Configurar Monitoring
```bash
# Habilitar monitoring para user workloads
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

# Ver status do monitoring
oc get clusteroperator monitoring
```

### ServiceMonitor
```bash
# Listar ServiceMonitors
oc get servicemonitor -A

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

---

## 📖 Navegação

- [← Anterior: Registry](10-registry-imagens.md)
- [→ Próximo: Must-Gather](12-must-gather.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
