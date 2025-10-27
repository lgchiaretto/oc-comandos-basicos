# Cluster Operators

Este documento contém comandos para gerenciar e diagnosticar Cluster Operators no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Verificar Status](#verificar-status)
3. [Troubleshooting](#troubleshooting)
4. [Operadores Principais](#operadores-principais)
5. [OLM (Operator Lifecycle Manager)](#olm-(operator-lifecycle-manager))
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## Verificar Status

### Status Geral
```bash
# Listar status de todos os cluster operators
oc get clusteroperators
oc get co
```

```bash
# Listar cluster operator com colunas customizadas
oc get co -o custom-columns=NAME:.metadata.name,VERSION:.status.versions[0].version
```

```bash
# Exibir cluster operator em formato JSON
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Available" and .status!="True")) | .metadata.name'
```

```bash
# Exibir cluster operator em formato JSON
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

```bash
# Exibir cluster operator em formato JSON
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Progressing" and .status=="True")) | .metadata.name'
```

```bash ignore-test
# Watch operators
watch oc get co
```

### Status Detalhado
```bash
# Exibir detalhes completos do cluster operator
# oc describe co <resource-name>
oc describe co authentication
```

```bash
# Exibir cluster operator "authentication" em formato JSON
# oc get co <resource-name>app -o jsonpath='{.status.conditions[*].type}{"\n"}{.status.conditions[*].status}'
oc get co authentication -o jsonpath='{.status.conditions[*].type}{"\n"}{.status.conditions[*].status}'
```

```bash
# Exibir cluster operator "authentication" em formato JSON
# oc get co <resource-name>app -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}'
oc get co authentication -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}'
```

```bash
# Exibir cluster operator "authentication" em formato JSON
# oc get co <resource-name>app -o jsonpath='{.status.versions[0].version}'
oc get co authentication -o jsonpath='{.status.versions[0].version}'
```

```bash
# Exibir cluster operator "authentication" em formato JSON
# oc get co <resource-name>app -o jsonpath='{.status.relatedObjects}'
oc get co authentication -o jsonpath='{.status.relatedObjects}'
```

---

## Troubleshooting

### Diagnosticar Problemas
```bash ignore-test
# Exibir cluster operator "authentication" em formato JSON
# oc get co <resource-name>app -o jsonpath='{.status.relatedObjects[?(@.resource=="namespaces")].name}' | xargs -I {} oc get pods -n {}
oc get co authentication -o jsonpath='{.status.relatedObjects[?(@.resource=="namespaces")].name}' | xargs -I {} oc get pods -n {}
```

```bash ignore-test
# Logs do operator
oc logs -n <namespace-do-operator> <pod-name>
```

```bash ignore-test
# Eventos relacionados
oc get events -n <namespace-do-operator> --sort-by='.lastTimestamp'
```

```bash ignore-test
# Ver deployment do operator
oc get deploy -n <namespace-do-operator>
```

```bash ignore-test
# Descrever deployment
oc describe deploy -n <namespace-do-operator> <deploy-name>
```

### Forçar Reconciliation
```bash
# Atualizar annotation existente com novo valor
oc annotate co/authentication --overwrite operator.openshift.io/refresh="$(date +%s)"
```

```bash ignore-test
# Restart do operator (deletar pod)
oc delete pod -n <namespace-do-operator> <pod-name>
```

```bash
# Ver progresso
oc get co/authentication
```

### Must-Gather de Operadores
```bash ignore-test
# Coletar dados de diagnóstico em diretório específico
oc adm must-gather --dest-dir=/tmp/must-gather
```

```bash ignore-test
# Ver logs dos operators no must-gather
cd /tmp/must-gather
find . -name "*operator*" -type d
```

---

## Operadores Principais

### Authentication Operator
```bash
# Status
# oc get co <resource-name>
oc get co authentication
```

```bash
# Pods
oc get pods -n openshift-authentication
```

```bash
# Exibir recurso "cluster" em formato YAML
oc get oauth cluster -o yaml
```

```bash ignore-test
# Logs
oc logs -n openshift-authentication-operator <pod-name>
```

### Ingress Operator
```bash
# Status
# oc get co <resource-name>
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
# Exibir logs de todos os pods que correspondem ao label
# oc logs -n <namespace> -l ingresscontroller.operator.openshift.io/deployment-ingresscontroller=default
oc logs -n openshift-ingress -l ingresscontroller.operator.openshift.io/deployment-ingresscontroller=default
```

```bash
# Exibir detalhes completos do recurso
# oc describe ingresscontroller default -n <namespace>
oc describe ingresscontroller default -n openshift-ingress-operator
```

### Network Operator
```bash
# Status
# oc get co <resource-name>
oc get co network
```

```bash
# Exibir recurso em formato YAML
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

```bash ignore-test
# Logs operator network
oc logs -n openshift-network-operator <pod-name>
```

### DNS Operator
```bash
# Status
# oc get co <resource-name>
oc get co dns
```

```bash
# DNS pods
oc get pods -n openshift-dns
```

```bash
# Exibir recurso em formato YAML
oc get dns.operator/default -o yaml
```

```bash ignore-test
# Logs
oc logs -n openshift-dns <dns-pod>
```

### Image Registry Operator
```bash
# Status
# oc get co <resource-name>
oc get co image-registry
```

```bash
# Exibir recurso em formato YAML
oc get configs.imageregistry.operator.openshift.io/cluster -o yaml
```

```bash
# Pods
oc get pods -n openshift-image-registry
```

```bash
# Exibir recurso em formato JSON
oc get configs.imageregistry.operator.openshift.io/cluster -o jsonpath='{.spec.storage}'
```

### Storage Operator
```bash
# Status
# oc get co <resource-name>
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
# oc get co <resource-name>
oc get co monitoring
```

```bash
# Pods de monitoring
oc get pods -n openshift-monitoring
```

```bash ignore-test
# Exibir recurso "cluster-monitoring-config" em formato YAML
# oc get configmap <configmap-name> -n <namespace> -o yaml
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

## OLM (Operator Lifecycle Manager)

### Gerenciar Operadores Instalados
```bash
# Listar recurso de todos os namespaces do cluster
oc get subscriptions -A
```

```bash
# Listar recurso de todos os namespaces do cluster
oc get csv -A
```

```bash
# Listar recurso de todos os namespaces do cluster
oc get operators -A
```

```bash
# Listar recurso de todos os namespaces do cluster
oc get installplans -A
```

```bash
# CatalogSources
oc get catalogsources -n openshift-marketplace
```

```bash
# Listar recurso de todos os namespaces do cluster
oc get operatorgroups -A
```

### Instalar Operadores
```bash
# Ver operators disponíveis
oc get packagemanifests -n openshift-marketplace
```

```bash ignore-test
# Buscar operator específico
oc get packagemanifests -n openshift-marketplace | grep odf-operator
```

```bash
# Exibir detalhes completos do recurso
# oc describe packagemanifest <resource-name>app -n <namespace>
oc describe packagemanifest odf-operator -n openshift-marketplace
```

```bash ignore-test
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

```bash ignore-test
# Ver progresso da instalação
oc get csv -n <namespace>
```

### Troubleshoot Operadores OLM
```bash
# Exibir detalhes completos do recurso
# oc describe subscription -n <namespace>   local-storage-operator
oc describe subscription -n openshift-local-storage   local-storage-operator
```

```bash ignore-test
# Ver CSV
oc describe csv <csv-name> -n <namespace>
```

```bash ignore-test
# Ver install plan
oc get installplan -n <namespace>
```

```bash ignore-test
# Aprovar install plan manual
oc patch installplan test-app -n <namespace> --type merge -p '{"spec":{"approved":true}}'
```

```bash ignore-test
# Logs do OLM
oc logs -n openshift-operator-lifecycle-manager <olm-operator-pod>
```

```bash ignore-test
# Catalog operator logs
oc logs -n openshift-operator-lifecycle-manager <catalog-operator-pod>
```

### Atualizar Operadores
```bash ignore-test
# Ver versão atual
oc get csv -n <namespace>
```

```bash
# Exibir recurso em formato JSON
oc get subscription  -n openshift-local-storage   local-storage-operator -o jsonpath='{.spec.installPlanApproval}'
```

```bash ignore-test
# Mudar para manual
oc patch subscription test-app -n <namespace> --type merge -p '{"spec":{"installPlanApproval":"Manual"}}'
```

```bash ignore-test
# Mudar para automatic
oc patch subscription test-app -n <namespace> --type merge -p '{"spec":{"installPlanApproval":"Automatic"}}'
```

```bash ignore-test
# Ver install plans pendentes
oc get installplan -n <namespace> -o json | jq -r '.items[] | select(.spec.approved==false) | .metadata.name'
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators">Operators - Understanding Operators</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators">Operators - Cluster Operators</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators">Operator Lifecycle Manager</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration">Post-installation configuration</a>
---

---

## Navegação

- [← Anterior: Segurança e RBAC](16-seguranca-rbac.md)
- [→ Próximo: Nodes e Machine](18-nodes-machine.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
