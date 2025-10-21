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
```

```bash
# Ver versões
oc get co -o custom-columns=NAME:.metadata.name,VERSION:.status.versions[0].version
```

```bash
# Operators com problema (não Available)
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Available" and .status!="True")) | .metadata.name'
```

```bash
# Operators Degraded
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

```bash
# Operators Progressing
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Progressing" and .status=="True")) | .metadata.name'
```

```bash
# Watch operators
oc get co
```

### Status Detalhado
```bash
# Descrever Cluster Operator
oc describe co <nome-do-operator>
```

```bash
# Ver condições
oc get co test-app -o jsonpath='{.status.conditions[*].type}{"\n"}{.status.conditions[*].status}'
```

```bash
# Ver mensagem de erro
oc get co test-app -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}'
```

```bash
# Ver versão
oc get co test-app -o jsonpath='{.status.versions[0].version}'
```

```bash
# Ver related objects
oc get co test-app -o jsonpath='{.status.relatedObjects}'
```

---

## 🔧 Troubleshooting

### Diagnosticar Problemas
```bash
# Ver pods do operator
oc get co test-app -o jsonpath='{.status.relatedObjects[?(@.resource=="namespaces")].name}' | xargs -I {} oc get pods -n {}
```

```bash
# Logs do operator
oc logs -n <namespace-do-operator> <pod-name>
```

```bash
# Eventos relacionados
oc get events -n <namespace-do-operator> --sort-by='.lastTimestamp'
```

```bash
# Ver deployment do operator
oc get deploy -n <namespace-do-operator>
```

```bash
# Descrever deployment
oc describe deploy -n <namespace-do-operator> <deploy-name>
```

### Forçar Reconciliation
```bash
# Adicionar annotation para forçar reconcile
oc annotate co/test-app --overwrite operator.openshift.io/refresh="$(date +%s)"
```

```bash
# Restart do operator (deletar pod)
oc delete pod -n <namespace-do-operator> <pod-name>
```

```bash
# Ver progresso
oc get co/test-app
```

### Must-Gather de Operadores
```bash
# Must-gather específico para operadores
oc adm must-gather --dest-dir=/tmp/must-gather
```

```bash
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
```

```bash
# Pods
oc get pods -n openshift-authentication
```

```bash
# Configuração OAuth
oc get oauth cluster -o yaml
```

```bash
# Logs
oc logs -n openshift-authentication-operator <pod-name>
```

### Ingress Operator
```bash
# Status
oc get co ingress
```

```bash
# IngressControllers
oc get ingresscontroller -n openshift-ingress-operator
```

```bash
# Pods do router
oc get pods -n openshift-ingress
```

```bash
# Logs do router
oc logs -n openshift-ingress -l app=router
```

```bash
# Configuração
oc describe ingresscontroller default -n openshift-ingress-operator
```

### Network Operator
```bash
# Status
oc get co network
```

```bash
# Configuração de rede
oc get network.config.openshift.io cluster -o yaml
```

```bash
# Pods de rede (OVN)
oc get pods -n openshift-ovn-kubernetes
```

```bash
# Pods de rede (SDN)
oc get pods -n openshift-sdn
```

```bash
# Logs
oc logs -n openshift-network-operator <pod-name>
```

### DNS Operator
```bash
# Status
oc get co dns
```

```bash
# DNS pods
oc get pods -n openshift-dns
```

```bash
# Configuração DNS
oc get dns.operator/default -o yaml
```

```bash
# Logs
oc logs -n openshift-dns <dns-pod>
```

### Image Registry Operator
```bash
# Status
oc get co image-registry
```

```bash
# Configuração
oc get configs.imageregistry.operator.openshift.io/cluster -o yaml
```

```bash
# Pods
oc get pods -n openshift-image-registry
```

```bash
# Ver storage config
oc get configs.imageregistry.operator.openshift.io/cluster -o jsonpath='{.spec.storage}'
```

### Storage Operator
```bash
# Status
oc get co storage
```

```bash
# CSI Drivers
oc get csidrivers
```

```bash
# CSI Nodes
oc get csinodes
```

```bash
# Storage classes
oc get sc
```

### Monitoring Operator
```bash
# Status
oc get co monitoring
```

```bash
# Pods de monitoring
oc get pods -n openshift-monitoring
```

```bash
# Configuração
oc get configmap cluster-monitoring-config -n openshift-monitoring -o yaml
```

```bash
# Prometheus
oc get prometheus -n openshift-monitoring
```

```bash
# Alertmanager
oc get alertmanager -n openshift-monitoring
```

---

## 🎯 OLM (Operator Lifecycle Manager)

### Gerenciar Operadores Instalados
```bash
# Listar subscriptions
oc get subscriptions -A
```

```bash
# Listar ClusterServiceVersions (CSVs)
oc get csv -A
```

```bash
# Ver operadores instalados
oc get operators -A
```

```bash
# InstallPlans
oc get installplans -A
```

```bash
# CatalogSources
oc get catalogsources -n openshift-marketplace
```

```bash
# OperatorGroups
oc get operatorgroups -A
```

### Instalar Operadores
```bash
# Ver operators disponíveis
oc get packagemanifests -n openshift-marketplace
```

```bash
# Buscar operator específico
oc get packagemanifests -n openshift-marketplace | grep test-app
```

```bash
# Ver channels disponíveis
oc describe packagemanifest test-app -n openshift-marketplace
```

```bash
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
```

```bash
# Ver progresso da instalação
oc get csv -n <namespace>
```

### Troubleshoot Operadores OLM
```bash
# Ver status da subscription
oc describe subscription test-app -n <namespace>
```

```bash
# Ver CSV
oc describe csv <csv-name> -n <namespace>
```

```bash
# Ver install plan
oc get installplan -n <namespace>
```

```bash
# Aprovar install plan manual
oc patch installplan test-app -n <namespace> --type merge -p '{"spec":{"approved":true}}'
```

```bash
# Logs do OLM
oc logs -n openshift-operator-lifecycle-manager <olm-operator-pod>
```

```bash
# Catalog operator logs
oc logs -n openshift-operator-lifecycle-manager <catalog-operator-pod>
```

### Atualizar Operadores
```bash
# Ver versão atual
oc get csv -n <namespace>
```

```bash
# Approval automático ou manual
oc get subscription test-app -n <namespace> -o jsonpath='{.spec.installPlanApproval}'
```

```bash
# Mudar para manual
oc patch subscription test-app -n <namespace> --type merge -p '{"spec":{"installPlanApproval":"Manual"}}'
```

```bash
# Mudar para automatic
oc patch subscription test-app -n <namespace> --type merge -p '{"spec":{"installPlanApproval":"Automatic"}}'
```

```bash
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
