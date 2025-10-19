# 🔮 Operators e Operandos

Este documento contém comandos para gerenciar Operators e seus Operandos (Custom Resources) no OpenShift.

---

## 📋 Índice

1. [Operator Lifecycle Manager (OLM)](#operator-lifecycle-manager-olm)
2. [Instalando Operators](#instalando-operators)
3. [Custom Resources (Operandos)](#custom-resources-operandos)
4. [Troubleshooting Operators](#troubleshooting-operators)

---

## 🎯 Operator Lifecycle Manager (OLM)

### Componentes do OLM
```bash
# Pods do OLM
oc get pods -n openshift-operator-lifecycle-manager

# OLM Operator
oc get pods -n openshift-operator-lifecycle-manager -l app=olm-operator

# Catalog Operator
oc get pods -n openshift-operator-lifecycle-manager -l app=catalog-operator

# Packageserver
oc get pods -n openshift-operator-lifecycle-manager -l app=packageserver

# Status do OLM
oc get clusteroperator operator-lifecycle-manager
oc get clusteroperator operator-lifecycle-manager-catalog
oc get clusteroperator operator-lifecycle-manager-packageserver
```

### Catalog Sources
```bash
# Listar catalog sources
oc get catalogsources -n openshift-marketplace

# Principais catalogs
oc get catalogsource redhat-operators -n openshift-marketplace
oc get catalogsource certified-operators -n openshift-marketplace
oc get catalogsource community-operators -n openshift-marketplace
oc get catalogsource redhat-marketplace -n openshift-marketplace

# Descrever catalog
oc describe catalogsource redhat-operators -n openshift-marketplace

# Ver imagem do catalog
oc get catalogsource redhat-operators -n openshift-marketplace -o jsonpath='{.spec.image}'

# Status do catalog
oc get catalogsource -n openshift-marketplace -o custom-columns=NAME:.metadata.name,STATUS:.status.connectionState.lastObservedState
```

### PackageManifests
```bash
# Listar operators disponíveis
oc get packagemanifests -n openshift-marketplace

# Buscar operator específico
oc get packagemanifests -n openshift-marketplace | grep -i elasticsearch

# Descrever packagemanifest
oc describe packagemanifest elasticsearch-operator -n openshift-marketplace

# Ver channels disponíveis
oc get packagemanifest elasticsearch-operator -n openshift-marketplace -o jsonpath='{.status.channels[*].name}'

# Ver versão do channel
oc get packagemanifest elasticsearch-operator -n openshift-marketplace -o jsonpath='{.status.channels[?(@.name=="stable")].currentCSV}'

# Ver default channel
oc get packagemanifest elasticsearch-operator -n openshift-marketplace -o jsonpath='{.status.defaultChannel}'
```

---

## 📦 Instalando Operators

### Passo a Passo Completo
```bash
# 1. Escolher operator
oc get packagemanifests -n openshift-marketplace | grep <operator-name>

# 2. Ver detalhes
oc describe packagemanifest <operator-name> -n openshift-marketplace

# 3. Criar namespace (se necessário)
oc create namespace <operator-namespace>

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

# 6. Verificar instalação
oc get csv -n <operator-namespace> -w
oc get pods -n <operator-namespace> -w
```

### Exemplo: Elasticsearch Operator
```bash
# Criar namespace
oc create namespace openshift-operators-redhat

# OperatorGroup (já existe globalmente, pular se for cluster-wide)

# Subscription
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: elasticsearch-operator
  namespace: openshift-operators-redhat
spec:
  channel: stable
  name: elasticsearch-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
  installPlanApproval: Automatic
EOF

# Verificar
oc get csv -n openshift-operators-redhat
oc get pods -n openshift-operators-redhat
```

### Install Plan
```bash
# Listar install plans
oc get installplan -n <namespace>

# Descrever install plan
oc describe installplan <plan-name> -n <namespace>

# Se approval for Manual, aprovar
oc patch installplan <plan-name> -n <namespace> --type merge -p '{"spec":{"approved":true}}'

# Ver status
oc get installplan <plan-name> -n <namespace> -o jsonpath='{.status.phase}'
```

### OperatorGroup
```bash
# Listar OperatorGroups
oc get operatorgroups -A

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

# CRDs de um operator específico
oc get crd | grep elasticsearch

# Descrever CRD
oc describe crd elasticsearches.logging.openshift.io

# Ver spec do CRD
oc get crd elasticsearches.logging.openshift.io -o yaml

# Ver versões suportadas
oc get crd elasticsearches.logging.openshift.io -o jsonpath='{.spec.versions[*].name}'
```

### Criar Custom Resources
```bash
# Ver exemplos no CSV
CSV_NAME=$(oc get csv -n <namespace> -o name | head -1)
oc get $CSV_NAME -n <namespace> -o yaml | grep -A 50 alm-examples

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

# Verificar CR
oc get elasticsearch -n openshift-logging
oc describe elasticsearch elasticsearch -n openshift-logging
```

### Gerenciar CRs
```bash
# Listar CRs de um tipo
oc get <crd-resource-name>

# Com custom-columns
oc get elasticsearch -o custom-columns=NAME:.metadata.name,STATUS:.status.cluster.status

# Edit CR
oc edit elasticsearch <name>

# Patch CR
oc patch elasticsearch <name> -p '{"spec":{"redundancyPolicy":"FullRedundancy"}}'

# Delete CR
oc delete elasticsearch <name>

# Ver eventos relacionados
oc get events --field-selector involvedObject.name=<cr-name>
```

### Ver Status de CRs
```bash
# Status geral
oc get <cr-type> <name> -o jsonpath='{.status}'

# Condições
oc get <cr-type> <name> -o jsonpath='{.status.conditions}'

# Exemplo específico
oc get elasticsearch <name> -o jsonpath='{.status.cluster.status}'

# Watch status
oc get <cr-type> <name> -w
```

---

## 🔧 Troubleshooting Operators

### CSV (ClusterServiceVersion)
```bash
# Listar CSVs
oc get csv -A

# CSV em namespace específico
oc get csv -n <namespace>

# Descrever CSV
oc describe csv <csv-name> -n <namespace>

# Ver fase do CSV
oc get csv <csv-name> -n <namespace> -o jsonpath='{.status.phase}'

# Ver mensagem de erro
oc get csv <csv-name> -n <namespace> -o jsonpath='{.status.message}'

# Ver pods gerenciados pelo CSV
oc get csv <csv-name> -n <namespace> -o jsonpath='{.spec.install.spec.deployments[*].name}'
```

### Logs do Operator
```bash
# Ver deployment do operator
oc get deployment -n <namespace>

# Pods do operator
oc get pods -n <namespace> -l name=<operator-name>

# Logs
oc logs -n <namespace> deployment/<operator-deployment>

# Logs com follow
oc logs -n <namespace> deployment/<operator-deployment> -f

# Logs anteriores (se crashou)
oc logs -n <namespace> <operator-pod> --previous
```

### Troubleshoot Subscription
```bash
# Ver subscription
oc get subscription <name> -n <namespace> -o yaml

# Ver status
oc get subscription <name> -n <namespace> -o jsonpath='{.status}'

# Ver CSV instalado
oc get subscription <name> -n <namespace> -o jsonpath='{.status.installedCSV}'

# Ver conditions
oc get subscription <name> -n <namespace> -o jsonpath='{.status.conditions}'

# Recrear subscription (deletar e criar novamente)
oc delete subscription <name> -n <namespace>
# Recriar...
```

### Operator Não Instala
```bash
# Verificar catalog source
oc get catalogsource -n openshift-marketplace
oc get pods -n openshift-marketplace

# Ver packagemanifest
oc get packagemanifest <operator> -n openshift-marketplace

# Verificar install plan
oc get installplan -n <namespace>
oc describe installplan <plan> -n <namespace>

# Logs do OLM
oc logs -n openshift-operator-lifecycle-manager deployment/olm-operator
oc logs -n openshift-operator-lifecycle-manager deployment/catalog-operator

# Eventos
oc get events -n <namespace> --sort-by='.lastTimestamp'
```

### CR Não Cria Recursos
```bash
# Verificar se operator está rodando
oc get pods -n <operator-namespace>

# Logs do operator
oc logs -n <operator-namespace> <operator-pod>

# Ver status do CR
oc describe <cr-type> <cr-name>

# Ver eventos
oc get events --field-selector involvedObject.name=<cr-name>

# Verificar RBAC
oc auth can-i create pods --as=system:serviceaccount:<namespace>:<sa>

# Ver service account do operator
oc get deployment <operator> -n <namespace> -o jsonpath='{.spec.template.spec.serviceAccountName}'
oc describe sa <sa-name> -n <namespace>
```

### Remover Operator
```bash
# 1. Deletar todos os CRs criados
oc get <cr-type> -A
oc delete <cr-type> <name> -n <namespace>

# 2. Deletar subscription
oc delete subscription <name> -n <namespace>

# 3. Deletar CSV
oc delete csv <csv-name> -n <namespace>

# 4. (Opcional) Deletar CRDs
oc delete crd <crd-name>

# 5. (Opcional) Deletar namespace
oc delete namespace <namespace>
```

---

## 📖 Navegação

- [← Anterior: Jobs e CronJobs](29-jobs-cronjobs.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
