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
```markdown
**Ação:** Listar status de todos os cluster operators
```

```bash
oc get clusteroperators
oc get co
```

```markdown
**Ação:** Listar cluster operator com colunas customizadas
```

```bash
oc get co -o custom-columns=NAME:.metadata.name,VERSION:.status.versions[0].version
```

```markdown
**Ação:** Exibir cluster operator em formato JSON
```

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Available" and .status!="True")) | .metadata.name'
```

```markdown
**Ação:** Exibir cluster operator em formato JSON
```

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

```markdown
**Ação:** Exibir cluster operator em formato JSON
```

```bash
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Progressing" and .status=="True")) | .metadata.name'
```

```markdown
**Ação:** Watch operators
```

```bash ignore-test
watch oc get co
```

### Status Detalhado
```markdown
**Ação:** Exibir detalhes completos do cluster operator
**Exemplo:** `oc describe co <resource-name>`
```

```bash
oc describe co authentication
```

```markdown
**Ação:** Exibir cluster operator "authentication" em formato JSON
**Exemplo:** `oc get co <resource-name>app -o jsonpath='{.status.conditions[*].type}{"\n"}{.status.conditions[*].status}'`
```

```bash
oc get co authentication -o jsonpath='{.status.conditions[*].type}{"\n"}{.status.conditions[*].status}'
```

```markdown
**Ação:** Exibir cluster operator "authentication" em formato JSON
**Exemplo:** `oc get co <resource-name>app -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}'`
```

```bash
oc get co authentication -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}'
```

```markdown
**Ação:** Exibir cluster operator "authentication" em formato JSON
**Exemplo:** `oc get co <resource-name>app -o jsonpath='{.status.versions[0].version}'`
```

```bash
oc get co authentication -o jsonpath='{.status.versions[0].version}'
```

```markdown
**Ação:** Exibir cluster operator "authentication" em formato JSON
**Exemplo:** `oc get co <resource-name>app -o jsonpath='{.status.relatedObjects}'`
```

```bash
oc get co authentication -o jsonpath='{.status.relatedObjects}'
```

---

## Troubleshooting

### Diagnosticar Problemas
```markdown
**Ação:** Exibir cluster operator "authentication" em formato JSON
**Exemplo:** `oc get co <resource-name>app -o jsonpath='{.status.relatedObjects[?(@.resource=="namespaces")].name}' | xargs -I {} oc get pods -n {}`
```

```bash ignore-test
oc get co authentication -o jsonpath='{.status.relatedObjects[?(@.resource=="namespaces")].name}' | xargs -I {} oc get pods -n {}
```

```markdown
**Ação:** Logs do operator
```

```bash ignore-test
oc logs -n <namespace-do-operator> <pod-name>
```

```markdown
**Ação:** Eventos relacionados
```

```bash ignore-test
oc get events -n <namespace-do-operator> --sort-by='.lastTimestamp'
```

```markdown
**Ação:** Ver deployment do operator
```

```bash ignore-test
oc get deploy -n <namespace-do-operator>
```

```markdown
**Ação:** Descrever deployment
```

```bash ignore-test
oc describe deploy -n <namespace-do-operator> <deploy-name>
```

### Forçar Reconciliation
```markdown
**Ação:** Atualizar annotation existente com novo valor
```

```bash
oc annotate co/authentication --overwrite operator.openshift.io/refresh="$(date +%s)"
```

```markdown
**Ação:** Restart do operator (deletar pod)
```

```bash ignore-test
oc delete pod -n <namespace-do-operator> <pod-name>
```

```markdown
**Ação:** Ver progresso
```

```bash
oc get co/authentication
```

### Must-Gather de Operadores
```markdown
**Ação:** Coletar dados de diagnóstico em diretório específico
```

```bash ignore-test
oc adm must-gather --dest-dir=/tmp/must-gather
```

```markdown
**Ação:** Ver logs dos operators no must-gather
```

```bash ignore-test
cd /tmp/must-gather
find . -name "*operator*" -type d
```

---

## Operadores Principais

### Authentication Operator
```markdown
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`
```

```bash
oc get co authentication
```

```markdown
**Ação:** Pods
```

```bash
oc get pods -n openshift-authentication
```

```markdown
**Ação:** Exibir recurso "cluster" em formato YAML
```

```bash
oc get oauth cluster -o yaml
```

```markdown
**Ação:** Logs
```

```bash ignore-test
oc logs -n openshift-authentication-operator <pod-name>
```

### Ingress Operator
```markdown
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`
```

```bash
oc get co ingress
```

```markdown
**Ação:** IngressControllers
```

```bash
oc get ingresscontroller -n openshift-ingress-operator
```

```markdown
**Ação:** Pods do router
```

```bash
oc get pods -n openshift-ingress
```

```markdown
**Ação:** Exibir logs de todos os pods que correspondem ao label
**Exemplo:** `oc logs -n <namespace> -l ingresscontroller.operator.openshift.io/deployment-ingresscontroller=default`
```

```bash
oc logs -n openshift-ingress -l ingresscontroller.operator.openshift.io/deployment-ingresscontroller=default
```

```markdown
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe ingresscontroller default -n <namespace>`
```

```bash
oc describe ingresscontroller default -n openshift-ingress-operator
```

### Network Operator
```markdown
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`
```

```bash
oc get co network
```

```markdown
**Ação:** Exibir recurso em formato YAML
```

```bash
oc get network.config.openshift.io cluster -o yaml
```

```markdown
**Ação:** Pods de rede (OVN)
```

```bash
oc get pods -n openshift-ovn-kubernetes
```

```markdown
**Ação:** Pods de rede (SDN)
```

```bash
oc get pods -n openshift-sdn
```

```markdown
**Ação:** Logs operator network
```

```bash ignore-test
oc logs -n openshift-network-operator <pod-name>
```

### DNS Operator
```markdown
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`
```

```bash
oc get co dns
```

```markdown
**Ação:** DNS pods
```

```bash
oc get pods -n openshift-dns
```

```markdown
**Ação:** Exibir recurso em formato YAML
```

```bash
oc get dns.operator/default -o yaml
```

```markdown
**Ação:** Logs
```

```bash ignore-test
oc logs -n openshift-dns <dns-pod>
```

### Image Registry Operator
```markdown
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`
```

```bash
oc get co image-registry
```

```markdown
**Ação:** Exibir recurso em formato YAML
```

```bash
oc get configs.imageregistry.operator.openshift.io/cluster -o yaml
```

```markdown
**Ação:** Pods
```

```bash
oc get pods -n openshift-image-registry
```

```markdown
**Ação:** Exibir recurso em formato JSON
```

```bash
oc get configs.imageregistry.operator.openshift.io/cluster -o jsonpath='{.spec.storage}'
```

### Storage Operator
```markdown
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`
```

```bash
oc get co storage
```

```markdown
**Ação:** CSI Drivers
```

```bash
oc get csidrivers
```

```markdown
**Ação:** CSI Nodes
```

```bash
oc get csinodes
```

```markdown
**Ação:** Storage classes
```

```bash
oc get sc
```

### Monitoring Operator
```markdown
**Ação:** Status
**Exemplo:** `oc get co <resource-name>`
```

```bash
oc get co monitoring
```

```markdown
**Ação:** Pods de monitoring
```

```bash
oc get pods -n openshift-monitoring
```

```markdown
**Ação:** Exibir recurso "cluster-monitoring-config" em formato YAML
**Exemplo:** `oc get configmap <configmap-name> -n <namespace> -o yaml`
```

```bash ignore-test
oc get configmap cluster-monitoring-config -n openshift-monitoring -o yaml
```

```markdown
**Ação:** Prometheus
```

```bash
oc get prometheus -n openshift-monitoring
```

```markdown
**Ação:** Alertmanager
```

```bash
oc get alertmanager -n openshift-monitoring
```

---

## OLM (Operator Lifecycle Manager)

### Gerenciar Operadores Instalados
```markdown
**Ação:** Listar recurso de todos os namespaces do cluster
```

```bash
oc get subscriptions -A
```

```markdown
**Ação:** Listar recurso de todos os namespaces do cluster
```

```bash
oc get csv -A
```

```markdown
**Ação:** Listar recurso de todos os namespaces do cluster
```

```bash
oc get operators -A
```

```markdown
**Ação:** Listar recurso de todos os namespaces do cluster
```

```bash
oc get installplans -A
```

```markdown
**Ação:** CatalogSources
```

```bash
oc get catalogsources -n openshift-marketplace
```

```markdown
**Ação:** Listar recurso de todos os namespaces do cluster
```

```bash
oc get operatorgroups -A
```

### Instalar Operadores
```markdown
**Ação:** Ver operators disponíveis
```

```bash
oc get packagemanifests -n openshift-marketplace
```

```markdown
**Ação:** Buscar operator específico
```

```bash ignore-test
oc get packagemanifests -n openshift-marketplace | grep odf-operator
```

```markdown
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe packagemanifest <resource-name>app -n <namespace>`
```

```bash
oc describe packagemanifest odf-operator -n openshift-marketplace
```

```markdown
**Ação:** Criar subscription
```

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

```markdown
**Ação:** Ver progresso da instalação
```

```bash ignore-test
oc get csv -n <namespace>
```

### Troubleshoot Operadores OLM
```markdown
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe subscription -n <namespace>   local-storage-operator`
```

```bash
oc describe subscription -n openshift-local-storage   local-storage-operator
```

```markdown
**Ação:** Ver CSV
```

```bash ignore-test
oc describe csv <csv-name> -n <namespace>
```

```markdown
**Ação:** Ver install plan
```

```bash ignore-test
oc get installplan -n <namespace>
```

```markdown
**Ação:** Aprovar install plan manual
```

```bash ignore-test
oc patch installplan test-app -n <namespace> --type merge -p '{"spec":{"approved":true}}'
```

```markdown
**Ação:** Logs do OLM
```

```bash ignore-test
oc logs -n openshift-operator-lifecycle-manager <olm-operator-pod>
```

```markdown
**Ação:** Catalog operator logs
```

```bash ignore-test
oc logs -n openshift-operator-lifecycle-manager <catalog-operator-pod>
```

### Atualizar Operadores
```markdown
**Ação:** Ver versão atual
```

```bash ignore-test
oc get csv -n <namespace>
```

```markdown
**Ação:** Exibir recurso em formato JSON
```

```bash
oc get subscription  -n openshift-local-storage   local-storage-operator -o jsonpath='{.spec.installPlanApproval}'
```

```markdown
**Ação:** Mudar para manual
```

```bash ignore-test
oc patch subscription test-app -n <namespace> --type merge -p '{"spec":{"installPlanApproval":"Manual"}}'
```

```markdown
**Ação:** Mudar para automatic
```

```bash ignore-test
oc patch subscription test-app -n <namespace> --type merge -p '{"spec":{"installPlanApproval":"Automatic"}}'
```

```markdown
**Ação:** Ver install plans pendentes
```

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
