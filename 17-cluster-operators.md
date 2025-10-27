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
**Ação:** Listar status de todos os cluster operators

```bash
oc get clusteroperators
oc get co
```

**Ação:** Listar cluster operator com colunas customizadas

```bash
oc get co -o custom-columns=NAME:.metadata.name,VERSION:.status.versions[0].version
```

**Ação:** Exibir cluster operator em formato JSON

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Available" and .status!="True")) | .metadata.name'
```

**Ação:** Exibir cluster operator em formato JSON

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

**Ação:** Exibir cluster operator em formato JSON

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Progressing" and .status=="True")) | .metadata.name'
```

**Ação:** Watch operators

```bash ignore-test
watch oc get co
```

### Status Detalhado
**Ação:** Exibir detalhes completos do cluster operator
**Exemplo:** `oc describe co <resource-name>`

```bash
oc describe co authentication
```

**Ação:** Exibir cluster operator "authentication" em formato JSON
**Exemplo:** `oc get co <resource-name>app -o jsonpath='{.status.conditions[*].type}{"\n"}{.status.conditions[*].status}'`

```bash
oc get co authentication -o jsonpath='{.status.conditions[*].type}{"\n"}{.status.conditions[*].status}'
```

**Ação:** Exibir cluster operator "authentication" em formato JSON
**Exemplo:** `oc get co <resource-name>app -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}'`

```bash
oc get co authentication -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}'
```

**Ação:** Exibir cluster operator "authentication" em formato JSON
**Exemplo:** `oc get co <resource-name>app -o jsonpath='{.status.versions[0].version}'`

```bash
oc get co authentication -o jsonpath='{.status.versions[0].version}'
```

**Ação:** Exibir cluster operator "authentication" em formato JSON
**Exemplo:** `oc get co <resource-name>app -o jsonpath='{.status.relatedObjects}'`

```bash
oc get co authentication -o jsonpath='{.status.relatedObjects}'
```

---

## Troubleshooting

### Diagnosticar Problemas
**Ação:** Exibir cluster operator "authentication" em formato JSON
**Exemplo:** `oc get co <resource-name>app -o jsonpath='{.status.relatedObjects[?(@.resource=="namespaces")].name}' | xargs -I {} oc get pods -n {}`

```bash ignore-test
oc get co authentication -o jsonpath='{.status.relatedObjects[?(@.resource=="namespaces")].name}' | xargs -I {} oc get pods -n {}
```

**Ação:** Logs do operator

```bash ignore-test
oc logs -n <namespace-do-operator> <pod-name>
```

**Ação:** Eventos relacionados

```bash ignore-test
oc get events -n <namespace-do-operator> --sort-by='.lastTimestamp'
```

**Ação:** Ver deployment do operator

```bash ignore-test
oc get deploy -n <namespace-do-operator>
```

**Ação:** Descrever deployment

```bash ignore-test
oc describe deploy -n <namespace-do-operator> <deploy-name>
```

### Forçar Reconciliation
**Ação:** Atualizar annotation existente com novo valor

```bash
oc annotate co/authentication --overwrite operator.openshift.io/refresh="$(date +%s)"
```

**Ação:** Restart do operator (deletar pod)

```bash ignore-test
oc delete pod -n <namespace-do-operator> <pod-name>
```

**Ação:** Ver progresso

```bash
oc get co/authentication
```

### Must-Gather de Operadores
**Ação:** Coletar dados de diagnóstico em diretório específico

```bash ignore-test
oc adm must-gather --dest-dir=/tmp/must-gather
```

**Ação:** Ver logs dos operators no must-gather

```bash ignore-test
cd /tmp/must-gather
find . -name "*operator*" -type d
```

---

## Operadores Principais

### Authentication Operator
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`

```bash
oc get co authentication
```

**Ação:** Pods

```bash
oc get pods -n openshift-authentication
```

**Ação:** Exibir recurso "cluster" em formato YAML

```bash
oc get oauth cluster -o yaml
```

**Ação:** Logs

```bash ignore-test
oc logs -n openshift-authentication-operator <pod-name>
```

### Ingress Operator
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`

```bash
oc get co ingress
```

**Ação:** IngressControllers

```bash
oc get ingresscontroller -n openshift-ingress-operator
```

**Ação:** Pods do router

```bash
oc get pods -n openshift-ingress
```

**Ação:** Exibir logs de todos os pods que correspondem ao label
**Exemplo:** `oc logs -n <namespace> -l ingresscontroller.operator.openshift.io/deployment-ingresscontroller=default`

```bash
oc logs -n openshift-ingress -l ingresscontroller.operator.openshift.io/deployment-ingresscontroller=default
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe ingresscontroller default -n <namespace>`

```bash
oc describe ingresscontroller default -n openshift-ingress-operator
```

### Network Operator
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`

```bash
oc get co network
```

**Ação:** Exibir recurso em formato YAML

```bash
oc get network.config.openshift.io cluster -o yaml
```

**Ação:** Pods de rede (OVN)

```bash
oc get pods -n openshift-ovn-kubernetes
```

**Ação:** Pods de rede (SDN)

```bash
oc get pods -n openshift-sdn
```

**Ação:** Logs operator network

```bash ignore-test
oc logs -n openshift-network-operator <pod-name>
```

### DNS Operator
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`

```bash
oc get co dns
```

**Ação:** DNS pods

```bash
oc get pods -n openshift-dns
```

**Ação:** Exibir recurso em formato YAML

```bash
oc get dns.operator/default -o yaml
```

**Ação:** Logs

```bash ignore-test
oc logs -n openshift-dns <dns-pod>
```

### Image Registry Operator
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`

```bash
oc get co image-registry
```

**Ação:** Exibir recurso em formato YAML

```bash
oc get configs.imageregistry.operator.openshift.io/cluster -o yaml
```

**Ação:** Pods

```bash
oc get pods -n openshift-image-registry
```

**Ação:** Exibir recurso em formato JSON

```bash
oc get configs.imageregistry.operator.openshift.io/cluster -o jsonpath='{.spec.storage}'
```

### Storage Operator
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`

```bash
oc get co storage
```

**Ação:** CSI Drivers

```bash
oc get csidrivers
```

**Ação:** CSI Nodes

```bash
oc get csinodes
```

**Ação:** Storage classes

```bash
oc get sc
```

### Monitoring Operator
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`

```bash
oc get co monitoring
```

**Ação:** Pods de monitoring

```bash
oc get pods -n openshift-monitoring
```

**Ação:** Exibir recurso "cluster-monitoring-config" em formato YAML
**Exemplo:** `oc get configmap <configmap-name> -n <namespace> -o yaml`

```bash ignore-test
oc get configmap cluster-monitoring-config -n openshift-monitoring -o yaml
```

**Ação:** Prometheus

```bash
oc get prometheus -n openshift-monitoring
```

**Ação:** Alertmanager

```bash
oc get alertmanager -n openshift-monitoring
```

---

## OLM (Operator Lifecycle Manager)

### Gerenciar Operadores Instalados
**Ação:** Listar recurso de todos os namespaces do cluster

```bash
oc get subscriptions -A
```

**Ação:** Listar recurso de todos os namespaces do cluster

```bash
oc get csv -A
```

**Ação:** Listar recurso de todos os namespaces do cluster

```bash
oc get operators -A
```

**Ação:** Listar recurso de todos os namespaces do cluster

```bash
oc get installplans -A
```

**Ação:** CatalogSources

```bash
oc get catalogsources -n openshift-marketplace
```

**Ação:** Listar recurso de todos os namespaces do cluster

```bash
oc get operatorgroups -A
```

### Instalar Operadores
**Ação:** Ver operators disponíveis

```bash
oc get packagemanifests -n openshift-marketplace
```

**Ação:** Buscar operator específico

```bash ignore-test
oc get packagemanifests -n openshift-marketplace | grep odf-operator
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe packagemanifest <resource-name>app -n <namespace>`

```bash
oc describe packagemanifest odf-operator -n openshift-marketplace
```

**Ação:** Criar subscription

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

**Ação:** Ver progresso da instalação

```bash ignore-test
oc get csv -n <namespace>
```

### Troubleshoot Operadores OLM
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe subscription -n <namespace>   local-storage-operator`

```bash
oc describe subscription -n openshift-local-storage   local-storage-operator
```

**Ação:** Ver CSV

```bash ignore-test
oc describe csv <csv-name> -n <namespace>
```

**Ação:** Ver install plan

```bash ignore-test
oc get installplan -n <namespace>
```

**Ação:** Aprovar install plan manual

```bash ignore-test
oc patch installplan test-app -n <namespace> --type merge -p '{"spec":{"approved":true}}'
```

**Ação:** Logs do OLM

```bash ignore-test
oc logs -n openshift-operator-lifecycle-manager <olm-operator-pod>
```

**Ação:** Catalog operator logs

```bash ignore-test
oc logs -n openshift-operator-lifecycle-manager <catalog-operator-pod>
```

### Atualizar Operadores
**Ação:** Ver versão atual

```bash ignore-test
oc get csv -n <namespace>
```

**Ação:** Exibir recurso em formato JSON

```bash
oc get subscription  -n openshift-local-storage   local-storage-operator -o jsonpath='{.spec.installPlanApproval}'
```

**Ação:** Mudar para manual

```bash ignore-test
oc patch subscription test-app -n <namespace> --type merge -p '{"spec":{"installPlanApproval":"Manual"}}'
```

**Ação:** Mudar para automatic

```bash ignore-test
oc patch subscription test-app -n <namespace> --type merge -p '{"spec":{"installPlanApproval":"Automatic"}}'
```

**Ação:** Ver install plans pendentes

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

---

## Navegação

- [← Anterior: Segurança e RBAC](16-seguranca-rbac.md)
- [→ Próximo: Nodes e Machine](18-nodes-machine.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
