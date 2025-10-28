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
**Listar status de todos os cluster operators**

```bash
oc get clusteroperators
oc get co
```

**Listar cluster operator com colunas customizadas**

```bash
oc get co -o custom-columns=NAME:.metadata.name,VERSION:.status.versions[0].version
```

**Exibir cluster operator em formato JSON completo**

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Available" and .status!="True")) | .metadata.name'
```

**Exibir cluster operator em formato JSON completo**

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

**Exibir cluster operator em formato JSON completo**

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Progressing" and .status=="True")) | .metadata.name'
```

**Watch operators**

```bash ignore-test
watch oc get co
```

### Status Detalhado
**Exibir detalhes completos do cluster operator**

```bash
oc describe co authentication
```

**Exibir cluster operator "authentication" em formato JSON**

```bash
oc get co authentication -o jsonpath='{.status.conditions[*].type}{"\n"}{.status.conditions[*].status}'
```

**Exibir cluster operator "authentication" em formato JSON**

```bash
oc get co authentication -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}'
```

**Exibir cluster operator "authentication" em formato JSON**

```bash
oc get co authentication -o jsonpath='{.status.versions[0].version}'
```

**Exibir cluster operator "authentication" em formato JSON**

```bash
oc get co authentication -o jsonpath='{.status.relatedObjects}'
```

---

## Troubleshooting

### Diagnosticar Problemas
**Exibir cluster operator "authentication" em formato JSON**

```bash ignore-test
oc get co authentication -o jsonpath='{.status.relatedObjects[?(@.resource=="namespaces")].name}' | xargs -I {} oc get pods -n {}
```

**Logs do operator**

```bash ignore-test
oc logs -n <namespace-do-operator> <pod-name>
```

**Eventos relacionados**

```bash ignore-test
oc get events -n <namespace-do-operator> --sort-by='.lastTimestamp'
```

**Ver deployment do operator**

```bash ignore-test
oc get deploy -n <namespace-do-operator>
```

**Descrever deployment**

```bash ignore-test
oc describe deploy -n <namespace-do-operator> <deploy-name>
```

### Forçar Reconciliation
**Atualizar annotation existente com novo valor**

```bash
oc annotate co/authentication --overwrite operator.openshift.io/refresh="$(date +%s)"
```

**Restart do operator (deletar pod)**

```bash ignore-test
oc delete pod -n <namespace-do-operator> <pod-name>
```

**Ver progresso**

```bash
oc get co/authentication
```

### Must-Gather de Operadores
**Coletar dados de diagnóstico em diretório específico**

```bash ignore-test
oc adm must-gather --dest-dir=/tmp/must-gather
```

**Ver logs dos operators no must-gather**

```bash ignore-test
cd /tmp/must-gather
find . -name "*operator*" -type d
```

---

## Operadores Principais

### Authentication Operator
**Status**

```bash
oc get co authentication
```

**Pods**

```bash
oc get pods -n openshift-authentication
```

**Exibir oauth em formato YAML completo**

```bash
oc get oauth cluster -o yaml
```

**Logs**

```bash ignore-test
oc logs -n openshift-authentication-operator <pod-name>
```

### Ingress Operator
**Status**

```bash
oc get co ingress
```

**IngressControllers**

```bash
oc get ingresscontroller -n openshift-ingress-operator
```

**Pods do router**

```bash
oc get pods -n openshift-ingress
```

**Exibir logs de todos os pods que correspondem ao label**

```bash
oc logs -n openshift-ingress -l ingresscontroller.operator.openshift.io/deployment-ingresscontroller=default
```

**Exibir detalhes completos do ingresscontroller**

```bash
oc describe ingresscontroller default -n openshift-ingress-operator
```

### Network Operator
**Status**

```bash
oc get co network
```

**Exibir network.config.openshift.io em formato YAML**

```bash
oc get network.config.openshift.io cluster -o yaml
```

**Pods de rede (OVN)**

```bash
oc get pods -n openshift-ovn-kubernetes
```

**Pods de rede (SDN)**

```bash
oc get pods -n openshift-sdn
```

**Logs operator network**

```bash ignore-test
oc logs -n openshift-network-operator <pod-name>
```

### DNS Operator
**Status**

```bash
oc get co dns
```

**DNS pods**

```bash
oc get pods -n openshift-dns
```

**Exibir dns.operator/default em formato YAML**

```bash
oc get dns.operator/default -o yaml
```

**Logs**

```bash ignore-test
oc logs -n openshift-dns <dns-pod>
```

### Image Registry Operator
**Status**

```bash
oc get co image-registry
```

**Exibir configs.imageregistry.operator.openshift.io/cluster em formato YAML**

```bash
oc get configs.imageregistry.operator.openshift.io/cluster -o yaml
```

**Pods**

```bash
oc get pods -n openshift-image-registry
```

**Exibir configs.imageregistry.operator.openshift.io/cluster em formato JSON**

```bash
oc get configs.imageregistry.operator.openshift.io/cluster -o jsonpath='{.spec.storage}'
```

### Storage Operator
**Status**

```bash
oc get co storage
```

**CSI Drivers**

```bash
oc get csidrivers
```

**CSI Nodes**

```bash
oc get csinodes
```

**Storage classes**

```bash
oc get sc
```

### Monitoring Operator
**Status**

```bash
oc get co monitoring
```

**Pods de monitoring**

```bash
oc get pods -n openshift-monitoring
```

**Exibir recurso "cluster-monitoring-config" em formato YAML**

```bash ignore-test
oc get configmap cluster-monitoring-config -n openshift-monitoring -o yaml
```

**Prometheus**

```bash
oc get prometheus -n openshift-monitoring
```

**Alertmanager**

```bash
oc get alertmanager -n openshift-monitoring
```

---

## OLM (Operator Lifecycle Manager)

### Gerenciar Operadores Instalados
**Listar subscriptions de todos os namespaces do cluster**

```bash
oc get subscriptions -A
```

**Listar csv de todos os namespaces do cluster**

```bash
oc get csv -A
```

**Listar operators de todos os namespaces do cluster**

```bash
oc get operators -A
```

**Listar installplans de todos os namespaces do cluster**

```bash
oc get installplans -A
```

**CatalogSources**

```bash
oc get catalogsources -n openshift-marketplace
```

**Listar operatorgroups de todos os namespaces do cluster**

```bash
oc get operatorgroups -A
```

### Instalar Operadores
**Ver operators disponíveis**

```bash
oc get packagemanifests -n openshift-marketplace
```

**Buscar operator específico**

```bash ignore-test
oc get packagemanifests -n openshift-marketplace | grep odf-operator
```

**Exibir detalhes completos do packagemanifest**

```bash
oc describe packagemanifest odf-operator -n openshift-marketplace
```

**Criar subscription**

```bash ignore-test
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

**Ver progresso da instalação**

```bash ignore-test
oc get csv -n <namespace>
```

### Troubleshoot Operadores OLM
**Exibir detalhes completos do subscription**

```bash
oc describe subscription -n openshift-local-storage   local-storage-operator
```

**Ver CSV**

```bash ignore-test
oc describe csv <csv-name> -n <namespace>
```

**Ver install plan**

```bash ignore-test
oc get installplan -n <namespace>
```

**Aprovar install plan manual**

```bash ignore-test
oc patch installplan test-app -n <namespace> --type merge -p '{"spec":{"approved":true}}'
```

**Logs do OLM**

```bash ignore-test
oc logs -n openshift-operator-lifecycle-manager <olm-operator-pod>
```

**Catalog operator logs**

```bash ignore-test
oc logs -n openshift-operator-lifecycle-manager <catalog-operator-pod>
```

### Atualizar Operadores
**Ver versão atual**

```bash ignore-test
oc get csv -n <namespace>
```

**Exibir recurso em formato JSON**

```bash
oc get subscription  -n openshift-local-storage   local-storage-operator -o jsonpath='{.spec.installPlanApproval}'
```

**Mudar para manual**

```bash ignore-test
oc patch subscription test-app -n <namespace> --type merge -p '{"spec":{"installPlanApproval":"Manual"}}'
```

**Mudar para automatic**

```bash ignore-test
oc patch subscription test-app -n <namespace> --type merge -p '{"spec":{"installPlanApproval":"Automatic"}}'
```

**Ver install plans pendentes**

```bash ignore-test
oc get installplan -n <namespace> -o json | jq -r '.items[] | select(.spec.approved==false) | .metadata.name'
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators">Operators - Understanding Operators</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators">Operators - Cluster Operators</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators">Operator Lifecycle Manager</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration">Post-installation configuration</a>
---


## Navegação

- [← Anterior: Segurança e RBAC](16-seguranca-rbac.md)
- [→ Próximo: Nodes e Machine](18-nodes-machine.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
