# ⚙️ Cluster Operators

Este documento contém comandos para gerenciar e diagnosticar Cluster Operators no OpenShift.

---

## 📋 Índice

1. [Verificar Status](#verificar-status)
2. [Troubleshooting](#troubleshooting)
3. [Operadores Principais](#operadores-principais)
4. [OLM (Operator Lifecycle Manager)](#olm-operator-lifecycle-manager)

---

## 🔍 Verificar Status

### Status Geral
```bash
# Listar todos os Cluster Operators
oc get clusteroperators
oc get co

# Ver versões
oc get co -o custom-columns=NAME:.metadata.name,VERSION:.status.versions[0].version

# Operators com problema (não Available)
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Available" and .status!="True")) | .metadata.name'

# Operators Degraded
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'

# Operators Progressing
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Progressing" and .status=="True")) | .metadata.name'

# Watch operators
oc get co -w
```

### Status Detalhado
```bash
# Descrever Cluster Operator
oc describe co <nome-do-operator>

# Ver condições
oc get co <nome> -o jsonpath='{.status.conditions[*].type}{"\n"}{.status.conditions[*].status}'

# Ver mensagem de erro
oc get co <nome> -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}'

# Ver versão
oc get co <nome> -o jsonpath='{.status.versions[0].version}'

# Ver related objects
oc get co <nome> -o jsonpath='{.status.relatedObjects}'
```

---

## 🔧 Troubleshooting

### Diagnosticar Problemas
```bash
# Ver pods do operator
oc get co <nome> -o jsonpath='{.status.relatedObjects[?(@.resource=="namespaces")].name}' | xargs -I {} oc get pods -n {}

# Logs do operator
oc logs -n <namespace-do-operator> <pod-name>

# Eventos relacionados
oc get events -n <namespace-do-operator> --sort-by='.lastTimestamp'

# Ver deployment do operator
oc get deploy -n <namespace-do-operator>

# Descrever deployment
oc describe deploy -n <namespace-do-operator> <deploy-name>
```

### Forçar Reconciliation
```bash
# Adicionar annotation para forçar reconcile
oc annotate co/<nome> --overwrite operator.openshift.io/refresh="$(date +%s)"

# Restart do operator (deletar pod)
oc delete pod -n <namespace-do-operator> <pod-name>

# Ver progresso
oc get co/<nome> -w
```

### Must-Gather de Operadores
```bash
# Must-gather específico para operadores
oc adm must-gather --dest-dir=/tmp/must-gather

# Ver logs dos operators no must-gather
cd /tmp/must-gather
find . -name "*operator*" -type d
```

---

## ⚡ Operadores Principais

### Authentication Operator
```bash
# Status
oc get co authentication

# Pods
oc get pods -n openshift-authentication

# Configuração OAuth
oc get oauth cluster -o yaml

# Logs
oc logs -n openshift-authentication-operator <pod-name>
```

### Ingress Operator
```bash
# Status
oc get co ingress

# IngressControllers
oc get ingresscontroller -n openshift-ingress-operator

# Pods do router
oc get pods -n openshift-ingress

# Logs do router
oc logs -n openshift-ingress -l app=router

# Configuração
oc describe ingresscontroller default -n openshift-ingress-operator
```

### Network Operator
```bash
# Status
oc get co network

# Configuração de rede
oc get network.config.openshift.io cluster -o yaml

# Pods de rede (OVN)
oc get pods -n openshift-ovn-kubernetes

# Pods de rede (SDN)
oc get pods -n openshift-sdn

# Logs
oc logs -n openshift-network-operator <pod-name>
```

### DNS Operator
```bash
# Status
oc get co dns

# DNS pods
oc get pods -n openshift-dns

# Configuração DNS
oc get dns.operator/default -o yaml

# Logs
oc logs -n openshift-dns <dns-pod>
```

### Image Registry Operator
```bash
# Status
oc get co image-registry

# Configuração
oc get configs.imageregistry.operator.openshift.io/cluster -o yaml

# Pods
oc get pods -n openshift-image-registry

# Ver storage config
oc get configs.imageregistry.operator.openshift.io/cluster -o jsonpath='{.spec.storage}'
```

### Storage Operator
```bash
# Status
oc get co storage

# CSI Drivers
oc get csidrivers

# CSI Nodes
oc get csinodes

# Storage classes
oc get sc
```

### Monitoring Operator
```bash
# Status
oc get co monitoring

# Pods de monitoring
oc get pods -n openshift-monitoring

# Configuração
oc get configmap cluster-monitoring-config -n openshift-monitoring -o yaml

# Prometheus
oc get prometheus -n openshift-monitoring

# Alertmanager
oc get alertmanager -n openshift-monitoring
```

---

## 🎯 OLM (Operator Lifecycle Manager)

### Gerenciar Operadores Instalados
```bash
# Listar subscriptions
oc get subscriptions -A

# Listar ClusterServiceVersions (CSVs)
oc get csv -A

# Ver operadores instalados
oc get operators -A

# InstallPlans
oc get installplans -A

# CatalogSources
oc get catalogsources -n openshift-marketplace

# OperatorGroups
oc get operatorgroups -A
```

### Instalar Operadores
```bash
# Ver operators disponíveis
oc get packagemanifests -n openshift-marketplace

# Buscar operator específico
oc get packagemanifests -n openshift-marketplace | grep <nome>

# Ver channels disponíveis
oc describe packagemanifest <nome> -n openshift-marketplace

# Criar subscription
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: <operator-name>
  namespace: <namespace>
spec:
  channel: <channel>
  name: <operator-name>
  source: redhat-operators
  sourceNamespace: openshift-marketplace
EOF

# Ver progresso da instalação
oc get csv -n <namespace> -w
```

### Troubleshoot Operadores OLM
```bash
# Ver status da subscription
oc describe subscription <nome> -n <namespace>

# Ver CSV
oc describe csv <csv-name> -n <namespace>

# Ver install plan
oc get installplan -n <namespace>

# Aprovar install plan manual
oc patch installplan <nome> -n <namespace> --type merge -p '{"spec":{"approved":true}}'

# Logs do OLM
oc logs -n openshift-operator-lifecycle-manager <olm-operator-pod>

# Catalog operator logs
oc logs -n openshift-operator-lifecycle-manager <catalog-operator-pod>
```

### Atualizar Operadores
```bash
# Ver versão atual
oc get csv -n <namespace>

# Approval automático ou manual
oc get subscription <nome> -n <namespace> -o jsonpath='{.spec.installPlanApproval}'

# Mudar para manual
oc patch subscription <nome> -n <namespace> --type merge -p '{"spec":{"installPlanApproval":"Manual"}}'

# Mudar para automatic
oc patch subscription <nome> -n <namespace> --type merge -p '{"spec":{"installPlanApproval":"Automatic"}}'

# Ver install plans pendentes
oc get installplan -n <namespace> -o json | jq -r '.items[] | select(.spec.approved==false) | .metadata.name'
```

---

## 📖 Navegação

- [← Anterior: Segurança e RBAC](16-seguranca-rbac.md)
- [→ Próximo: Nodes e Machine](18-nodes-machine.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
