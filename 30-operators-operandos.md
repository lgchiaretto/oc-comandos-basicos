# 🔮 Operators e Operandos

Este documento contém comandos para gerenciar Operators e seus Operandos (Custom Resources) no OpenShift.

---

## 📋 Índice

1. [🎯 Operator Lifecycle Manager (OLM)](#operator-lifecycle-manager-olm)
2. [📦 Instalando Operators](#instalando-operators)
3. [🎨 Custom Resources (Operandos)](#custom-resources-operandos)
4. [🔧 Troubleshooting Operators](#troubleshooting-operators)
---

## 🎯 Operator Lifecycle Manager (OLM)

### Componentes do OLM
```bash
# Pods do OLM
oc get pods -n openshift-operator-lifecycle-manager
```

```bash
# OLM Operator
oc get pods -n openshift-operator-lifecycle-manager -l app=olm-operator
```

```bash
# Catalog Operator
oc get pods -n openshift-operator-lifecycle-manager -l app=catalog-operator
```

```bash
# Packageserver
oc get pods -n openshift-operator-lifecycle-manager -l app=packageserver
```

```bash
# Status do OLM
# oc get clusteroperator <resource-name>
oc get clusteroperator operator-lifecycle-manager
# oc get clusteroperator <resource-name>
oc get clusteroperator operator-lifecycle-manager-catalog
# oc get clusteroperator <resource-name>
oc get clusteroperator operator-lifecycle-manager-packageserver
```

### Catalog Sources
```bash
# Listar catalog sources
oc get catalogsources -n openshift-marketplace
```

```bash
# Principais catalogs
# oc get catalogsource <resource-name>operators -n <namespace>
oc get catalogsource redhat-operators -n openshift-marketplace
# oc get catalogsource <resource-name>operators -n <namespace>
oc get catalogsource certified-operators -n openshift-marketplace
# oc get catalogsource <resource-name>operators -n <namespace>
oc get catalogsource community-operators -n openshift-marketplace
# oc get catalogsource <resource-name>marketplace -n <namespace>
oc get catalogsource redhat-marketplace -n openshift-marketplace
```

```bash
# Descrever catalog
# oc describe catalogsource <resource-name>operators -n <namespace>
oc describe catalogsource redhat-operators -n openshift-marketplace
```

```bash
# Ver imagem do catalog
# oc get catalogsource <resource-name>operators -n <namespace> -o jsonpath='{.spec.image}'
oc get catalogsource redhat-operators -n openshift-marketplace -o jsonpath='{.spec.image}'
```

```bash
# Status do catalog
oc get catalogsource -n openshift-marketplace -o custom-columns=NAME:.metadata.name,STATUS:.status.connectionState.lastObservedState
```

### PackageManifests
```bash
# Listar operators disponíveis
oc get packagemanifests -n openshift-marketplace
```

```bash
# Buscar operator específico
oc get packagemanifests -n openshift-marketplace | grep -i elasticsearch
```

```bash
# Descrever packagemanifest
# oc describe packagemanifest <resource-name>operator -n <namespace>
oc describe packagemanifest local-storage-operator -n openshift-marketplace
```

```bash ignore-test
# Ver channels disponíveis
# oc get packagemanifest <resource-name>operator -n <namespace> -o jsonpath='{.status.channels[*].name}'
oc get packagemanifest local-storage-operator -n openshift-marketplace -o jsonpath='{.status.channels[*].name}'
```

```bash ignore-test
# Ver versão do channel
# oc get packagemanifest <resource-name>operator -n <namespace> -o jsonpath='{.status.channels[?(@.name=="stable")].currentCSV}'
oc get packagemanifest local-storage-operator -n openshift-marketplace -o jsonpath='{.status.channels[?(@.name=="stable")].currentCSV}'
```

```bash
# Ver default channel
# oc get packagemanifest <resource-name>operator -n <namespace> -o jsonpath='{.status.defaultChannel}'
oc get packagemanifest local-storage-operator -n openshift-marketplace -o jsonpath='{.status.defaultChannel}'
```

---

## 📦 Instalando Operators

### Passo a Passo Completo
```bash ignore-test
# 1. Escolher operator
oc get packagemanifests -n openshift-marketplace | grep <operator-name>
```

```bash ignore-test
# 2. Ver detalhes
oc describe packagemanifest <operator-name> -n openshift-marketplace
```

```bash ignore-test
# 3. Criar namespace (se necessário)
oc create namespace <operator-namespace>
```

```bash ignore-test
# 4. Criar OperatorGroup
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: <og-name>
  namespace: <operator-namespace>
spec:
  targetNamespaces:
  - <operator-namespace>
EOF
```

```bash ignore-test
# 5. Criar Subscription
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: <subscription-name>
  namespace: <operator-namespace>
spec:
  channel: <channel>
  name: <operator-package-name>
  source: redhat-operators
  sourceNamespace: openshift-marketplace
  installPlanApproval: Automatic
EOF
```

```bash ignore-test
# 6. Verificar instalação
oc get csv -n <operator-namespace>
oc get pods -n <operator-namespace>
```

### Exemplo: Elasticsearch Operator
```bash ignore-test
# Criar namespace
# oc create namespace <namespace-name>
oc create namespace openshift-operators-redhat
```

```bash ignore-test
# Subscription
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: local-storage-operator
  namespace: openshift-operators-redhat
spec:
  channel: stable
  name: local-storage-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
  installPlanApproval: Automatic
EOF
```

```bash
# Verificar
oc get csv -n openshift-operators-redhat
oc get pods -n openshift-operators-redhat
```

### Install Plan
```bash ignore-test
# Listar install plans
oc get installplan -n <namespace>
```

```bash ignore-test
# Descrever install plan
oc describe installplan <plan-name> -n <namespace>
```

```bash ignore-test
# Se approval for Manual, aprovar
oc patch installplan <plan-name> -n <namespace> --type merge -p '{"spec":{"approved":true}}'
```

```bash ignore-test
# Ver status
oc get installplan <plan-name> -n <namespace> -o jsonpath='{.status.phase}'
```

### OperatorGroup
```bash
# Listar OperatorGroups
oc get operatorgroups -A
```

```bash ignore-test
# OperatorGroup para namespace único
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: my-og
  namespace: my-namespace
spec:
  targetNamespaces:
  - my-namespace
EOF
```

```bash ignore-test
# OperatorGroup para múltiplos namespaces
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: multi-og
  namespace: operator-namespace
spec:
  targetNamespaces:
  - namespace1
  - namespace2
  - namespace3
EOF
```

```bash ignore-test
# OperatorGroup cluster-wide (sem targetNamespaces)
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: global-og
  namespace: openshift-operators
spec: {}
EOF
```

---

## 🎨 Custom Resources (Operandos)

### Listar CRDs
```bash
# Todos os CRDs
oc get crd
```

```bash
# CRDs de um operator específico
oc get crd | grep ingresscontrollers
```

```bash
# Descrever CRD
# oc describe crd <resource-name>.operator.openshift.io
oc describe crd ingresscontrollers.operator.openshift.io
```

```bash
# Ver spec do CRD
# oc get crd <resource-name>.operator.openshift.io -o yaml
oc get crd ingresscontrollers.operator.openshift.io -o yaml
```

```bash
# Ver versões suportadas
# oc get crd <resource-name>.operator.openshift.io -o jsonpath='{.spec.versions[*].name}'
oc get crd ingresscontrollers.operator.openshift.io -o jsonpath='{.spec.versions[*].name}'
```

### Criar Custom Resources
```bash ignore-test
# Ver exemplos no CSV
CSV_NAME=$(oc get csv -n <namespace> -o name | head -1)
oc get $CSV_NAME -n <namespace> -o yaml | grep -A 50 alm-examples
```

```bash ignore-test
# Criar CR (exemplo: Elasticsearch)
cat <<EOF | oc apply -f -
apiVersion: logging.openshift.io/v1
kind: Elasticsearch
metadata:
  name: elasticsearch
  namespace: openshift-logging
spec:
  managementState: Managed
  redundancyPolicy: SingleRedundancy
  nodeSpec:
    resources:
      limits:
        memory: 2Gi
      requests:
        memory: 2Gi
EOF
```

```bash ignore-test
# Verificar CR
oc get elasticsearch -n openshift-logging
# oc describe elasticsearch elasticsearch -n <namespace>
oc describe elasticsearch elasticsearch -n openshift-logging
```

### Gerenciar CRs
```bash ignore-test
# Listar CRs de um tipo
oc get <crd-resource-name>
```

```bash ignore-test
# Com custom-columns
oc get elasticsearch -o custom-columns=NAME:.metadata.name,STATUS:.status.cluster.status
```

```bash ignore-test
# Edit CR
oc edit elasticsearch <name>
```

```bash ignore-test
# Patch CR
oc patch elasticsearch <name> -p '{"spec":{"redundancyPolicy":"FullRedundancy"}}'
```

```bash ignore-test
# Delete CR
oc delete elasticsearch <name>
```

```bash ignore-test
# Ver eventos relacionados
oc get events --field-selector involvedObject.name=<cr-name>
```

### Ver Status de CRs
```bash ignore-test
# Status geral
oc get <cr-type> <name> -o jsonpath='{.status}'
```

```bash ignore-test
# Condições
oc get <cr-type> <name> -o jsonpath='{.status.conditions}'
```

```bash ignore-test
# Exemplo específico
oc get elasticsearch <name> -o jsonpath='{.status.cluster.status}'
```

```bash ignore-test
# Watch status
oc get <cr-type> <name>
```

---

## 🔧 Troubleshooting Operators

### CSV (ClusterServiceVersion)
```bash
# Listar CSVs
oc get csv -A
```

```bash ignore-test
# CSV em namespace específico
oc get csv -n <namespace>
```

```bash ignore-test
# Descrever CSV
oc describe csv <csv-name> -n <namespace>
```

```bash ignore-test
# Ver fase do CSV
oc get csv <csv-name> -n <namespace> -o jsonpath='{.status.phase}'
```

```bash ignore-test
# Ver mensagem de erro
oc get csv <csv-name> -n <namespace> -o jsonpath='{.status.message}'
```

```bash ignore-test
# Ver pods gerenciados pelo CSV
oc get csv <csv-name> -n <namespace> -o jsonpath='{.spec.install.spec.deployments[*].name}'
```

### Logs do Operator
```bash ignore-test
# Ver deployment do operator
oc get deployment -n <namespace>
```

```bash ignore-test
# Pods do operator
oc get pods -n <namespace> -l name=<operator-name>
```

```bash ignore-test
# Logs
oc logs -n <namespace> deployment/<operator-deployment>
```

```bash ignore-test
# Logs com follow
oc logs -n <namespace> deployment/<operator-deployment> -f
```

```bash ignore-test
# Logs anteriores (se crashou)
oc logs -n <namespace> <operator-pod> --previous
```

### Troubleshoot Subscription
```bash ignore-test
# Ver subscription
oc get subscription <name> -n <namespace> -o yaml
```

```bash ignore-test
# Ver status
oc get subscription <name> -n <namespace> -o jsonpath='{.status}'
```

```bash ignore-test
# Ver CSV instalado
oc get subscription <name> -n <namespace> -o jsonpath='{.status.installedCSV}'
```

```bash ignore-test
# Ver conditions
oc get subscription <name> -n <namespace> -o jsonpath='{.status.conditions}'
```

```bash ignore-test
# Recrear subscription (deletar e criar novamente)
oc delete subscription <name> -n <namespace>
# Recriar...
```

### Operator Não Instala
```bash
# Verificar catalog source
oc get catalogsource -n openshift-marketplace
oc get pods -n openshift-marketplace
```

```bash ignore-test
# Ver packagemanifest
oc get packagemanifest <operator> -n openshift-marketplace
```

```bash ignore-test
# Verificar install plan
oc get installplan -n <namespace>
oc describe installplan <plan> -n <namespace>
```

```bash
# Logs do OLM
# oc logs -n <namespace> deployment/olm-operator
oc logs -n openshift-operator-lifecycle-manager deployment/olm-operator
# oc logs -n <namespace> deployment/catalog-operator
oc logs -n openshift-operator-lifecycle-manager deployment/catalog-operator
```

```bash ignore-test
# Eventos
oc get events -n <namespace> --sort-by='.lastTimestamp'
```

### CR Não Cria Recursos
```bash ignore-test
# Verificar se operator está rodando
oc get pods -n <operator-namespace>
```

```bash ignore-test
# Logs do operator
oc logs -n <operator-namespace> <operator-pod>
```

```bash ignore-test
# Ver status do CR
oc describe <cr-type> <cr-name>
```

```bash ignore-test
# Ver eventos
oc get events --field-selector involvedObject.name=<cr-name>
```

```bash ignore-test
# Verificar RBAC
oc auth can-i create pods --as=system:serviceaccount:<namespace>:<sa>
```

```bash ignore-test
# Ver service account do operator
oc get deployment <operator> -n <namespace> -o jsonpath='{.spec.template.spec.serviceAccountName}'
oc describe sa <sa-name> -n <namespace>
```

### Remover Operator
```bash ignore-test
# 1. Deletar todos os CRs criados
oc get <cr-type> -A
oc delete <cr-type> <name> -n <namespace>
```

```bash ignore-test
# 2. Deletar subscription
oc delete subscription <name> -n <namespace>
```

```bash ignore-test
# 3. Deletar CSV
oc delete csv <csv-name> -n <namespace>
```

```bash ignore-test
# 4. (Opcional) Deletar CRDs
oc delete crd <crd-name>
```

```bash ignore-test
# 5. (Opcional) Deletar namespace
oc delete namespace <namespace>
```

---


---

## 📚 Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- [Operators](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators)

---

## 📖 Navegação

- [← Anterior: Jobs e CronJobs](29-jobs-cronjobs.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
