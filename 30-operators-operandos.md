# Operators e Operandos

Este documento contém comandos para gerenciar Operators e seus Operandos (Custom Resources) no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Operator Lifecycle Manager (OLM)](#operator-lifecycle-manager-(olm))
3. [Instalando Operators](#instalando-operators)
4. [Custom Resources (Operandos)](#custom-resources-(operandos))
5. [Troubleshooting Operators](#troubleshooting-operators)
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## Operator Lifecycle Manager (OLM)

### Componentes do OLM
```markdown
**Ação:** Pods do OLM
```

```bash
oc get pods -n openshift-operator-lifecycle-manager
```

```markdown
**Ação:** Listar pods filtrados por label
```

```bash
oc get pods -n openshift-operator-lifecycle-manager -l app=olm-operator
```

```markdown
**Ação:** Listar pods filtrados por label
```

```bash
oc get pods -n openshift-operator-lifecycle-manager -l app=catalog-operator
```

```markdown
**Ação:** Listar pods filtrados por label
```

```bash
oc get pods -n openshift-operator-lifecycle-manager -l app=packageserver
```

```markdown
**Ação:** Status do OLM
**Exemplo:** `oc get clusteroperator <resource-name>`
**Ação:** oc get clusteroperator <resource-name>
**Ação:** oc get clusteroperator <resource-name>
```

```bash
oc get clusteroperator operator-lifecycle-manager
oc get clusteroperator operator-lifecycle-manager-catalog
oc get clusteroperator operator-lifecycle-manager-packageserver
```

### Catalog Sources
```markdown
**Ação:** Listar catalog sources
```

```bash
oc get catalogsources -n openshift-marketplace
```

```markdown
**Ação:** Principais catalogs
**Exemplo:** `oc get catalogsource <resource-name>operators -n <namespace>`
**Ação:** oc get catalogsource <resource-name>operators -n <namespace>
**Ação:** oc get catalogsource <resource-name>operators -n <namespace>
**Ação:** oc get catalogsource <resource-name>marketplace -n <namespace>
```

```bash
oc get catalogsource redhat-operators -n openshift-marketplace
oc get catalogsource certified-operators -n openshift-marketplace
oc get catalogsource community-operators -n openshift-marketplace
oc get catalogsource redhat-marketplace -n openshift-marketplace
```

```markdown
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe catalogsource <resource-name>operators -n <namespace>`
```

```bash
oc describe catalogsource redhat-operators -n openshift-marketplace
```

```markdown
**Ação:** Exibir recurso "redhat-operators" em formato JSON
**Exemplo:** `oc get catalogsource <resource-name>operators -n <namespace> -o jsonpath='{.spec.image}'`
```

```bash
oc get catalogsource redhat-operators -n openshift-marketplace -o jsonpath='{.spec.image}'
```

```markdown
**Ação:** Listar recurso com colunas customizadas
```

```bash
oc get catalogsource -n openshift-marketplace -o custom-columns=NAME:.metadata.name,STATUS:.status.connectionState.lastObservedState
```

### PackageManifests
```markdown
**Ação:** Listar operators disponíveis
```

```bash
oc get packagemanifests -n openshift-marketplace
```

```markdown
**Ação:** Buscar operator específico
```

```bash
oc get packagemanifests -n openshift-marketplace | grep -i elasticsearch
```

```markdown
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe packagemanifest <resource-name>operator -n <namespace>`
```

```bash
oc describe packagemanifest local-storage-operator -n openshift-marketplace
```

```markdown
**Ação:** Exibir recurso "local-storage-operator" em formato JSON
**Exemplo:** `oc get packagemanifest <resource-name>operator -n <namespace> -o jsonpath='{.status.channels[*].name}'`
```

```bash ignore-test
oc get packagemanifest local-storage-operator -n openshift-marketplace -o jsonpath='{.status.channels[*].name}'
```

```markdown
**Ação:** Exibir recurso "local-storage-operator" em formato JSON
**Exemplo:** `oc get packagemanifest <resource-name>operator -n <namespace> -o jsonpath='{.status.channels[?(@.name=="stable")].currentCSV}'`
```

```bash ignore-test
oc get packagemanifest local-storage-operator -n openshift-marketplace -o jsonpath='{.status.channels[?(@.name=="stable")].currentCSV}'
```

```markdown
**Ação:** Exibir recurso "local-storage-operator" em formato JSON
**Exemplo:** `oc get packagemanifest <resource-name>operator -n <namespace> -o jsonpath='{.status.defaultChannel}'`
```

```bash
oc get packagemanifest local-storage-operator -n openshift-marketplace -o jsonpath='{.status.defaultChannel}'
```

---

## Instalando Operators

### Passo a Passo Completo
```markdown
**Ação:** 1. Escolher operator
```

```bash ignore-test
oc get packagemanifests -n openshift-marketplace | grep <operator-name>
```

```markdown
**Ação:** 2. Ver detalhes
```

```bash ignore-test
oc describe packagemanifest <operator-name> -n openshift-marketplace
```

```markdown
**Ação:** 3. Criar namespace (se necessário)
```

```bash ignore-test
oc create namespace <operator-namespace>
```

```markdown
**Ação:** 4. Criar OperatorGroup
```

```bash ignore-test
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

```markdown
**Ação:** 5. Criar Subscription
```

```bash ignore-test
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

```markdown
**Ação:** 6. Verificar instalação
```

```bash ignore-test
oc get csv -n <operator-namespace>
oc get pods -n <operator-namespace>
```

### Exemplo: Elasticsearch Operator
```markdown
**Ação:** Criar novo recurso
**Exemplo:** `oc create namespace <namespace-name>`
```

```bash ignore-test
oc create namespace openshift-operators-redhat
```

```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash ignore-test
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

```markdown
**Ação:** Verificar
```

```bash
oc get csv -n openshift-operators-redhat
oc get pods -n openshift-operators-redhat
```

### Install Plan
```markdown
**Ação:** Listar install plans
```

```bash ignore-test
oc get installplan -n <namespace>
```

```markdown
**Ação:** Descrever install plan
```

```bash ignore-test
oc describe installplan <plan-name> -n <namespace>
```

```markdown
**Ação:** Se approval for Manual, aprovar
```

```bash ignore-test
oc patch installplan <plan-name> -n <namespace> --type merge -p '{"spec":{"approved":true}}'
```

```markdown
**Ação:** Ver status
```

```bash ignore-test
oc get installplan <plan-name> -n <namespace> -o jsonpath='{.status.phase}'
```

### OperatorGroup
```markdown
**Ação:** Listar recurso de todos os namespaces do cluster
```

```bash
oc get operatorgroups -A
```

```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash ignore-test
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

```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash ignore-test
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

```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash ignore-test
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

## Custom Resources (Operandos)

### Listar CRDs
```markdown
**Ação:** Todos os CRDs
```

```bash
oc get crd
```

```markdown
**Ação:** CRDs de um operator específico
```

```bash
oc get crd | grep ingresscontrollers
```

```markdown
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe crd <resource-name>.operator.openshift.io`
```

```bash
oc describe crd ingresscontrollers.operator.openshift.io
```

```markdown
**Ação:** Exibir recurso "ingresscontrollers.operator.openshift.io" em formato YAML
**Exemplo:** `oc get crd <resource-name>.operator.openshift.io -o yaml`
```

```bash
oc get crd ingresscontrollers.operator.openshift.io -o yaml
```

```markdown
**Ação:** Exibir recurso "ingresscontrollers.operator.openshift.io" em formato JSON
**Exemplo:** `oc get crd <resource-name>.operator.openshift.io -o jsonpath='{.spec.versions[*].name}'`
```

```bash
oc get crd ingresscontrollers.operator.openshift.io -o jsonpath='{.spec.versions[*].name}'
```

### Criar Custom Resources
```markdown
**Ação:** Ver exemplos no CSV
```

```bash ignore-test
CSV_NAME=$(oc get csv -n <namespace> -o name | head -1)
oc get $CSV_NAME -n <namespace> -o yaml | grep -A 50 alm-examples
```

```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash ignore-test
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

```markdown
**Ação:** Verificar CR
**Ação:** oc describe elasticsearch elasticsearch -n <namespace>
```

```bash ignore-test
oc get elasticsearch -n openshift-logging
oc describe elasticsearch elasticsearch -n openshift-logging
```

### Gerenciar CRs
```markdown
**Ação:** Listar CRs de um tipo
```

```bash ignore-test
oc get <crd-resource-name>
```

```markdown
**Ação:** Listar recurso com colunas customizadas
```

```bash ignore-test
oc get elasticsearch -o custom-columns=NAME:.metadata.name,STATUS:.status.cluster.status
```

```markdown
**Ação:** Edit CR
```

```bash ignore-test
oc edit elasticsearch <name>
```

```markdown
**Ação:** Patch CR
```

```bash ignore-test
oc patch elasticsearch <name> -p '{"spec":{"redundancyPolicy":"FullRedundancy"}}'
```

```markdown
**Ação:** Delete CR
```

```bash ignore-test
oc delete elasticsearch <name>
```

```markdown
**Ação:** Ver eventos relacionados
```

```bash ignore-test
oc get events --field-selector involvedObject.name=<cr-name>
```

### Ver Status de CRs
```markdown
**Ação:** Status geral
```

```bash ignore-test
oc get <cr-type> <name> -o jsonpath='{.status}'
```

```markdown
**Ação:** Condições
```

```bash ignore-test
oc get <cr-type> <name> -o jsonpath='{.status.conditions}'
```

```markdown
**Ação:** Exemplo específico
```

```bash ignore-test
oc get elasticsearch <name> -o jsonpath='{.status.cluster.status}'
```

```markdown
**Ação:** Watch status
```

```bash ignore-test
oc get <cr-type> <name>
```

---

## Troubleshooting Operators

### CSV (ClusterServiceVersion)
```markdown
**Ação:** Listar recurso de todos os namespaces do cluster
```

```bash
oc get csv -A
```

```markdown
**Ação:** CSV em namespace específico
```

```bash ignore-test
oc get csv -n <namespace>
```

```markdown
**Ação:** Descrever CSV
```

```bash ignore-test
oc describe csv <csv-name> -n <namespace>
```

```markdown
**Ação:** Ver fase do CSV
```

```bash ignore-test
oc get csv <csv-name> -n <namespace> -o jsonpath='{.status.phase}'
```

```markdown
**Ação:** Ver mensagem de erro
```

```bash ignore-test
oc get csv <csv-name> -n <namespace> -o jsonpath='{.status.message}'
```

```markdown
**Ação:** Ver pods gerenciados pelo CSV
```

```bash ignore-test
oc get csv <csv-name> -n <namespace> -o jsonpath='{.spec.install.spec.deployments[*].name}'
```

### Logs do Operator
```markdown
**Ação:** Ver deployment do operator
```

```bash ignore-test
oc get deployment -n <namespace>
```

```markdown
**Ação:** Pods do operator
```

```bash ignore-test
oc get pods -n <namespace> -l name=<operator-name>
```

```markdown
**Ação:** Logs
```

```bash ignore-test
oc logs -n <namespace> deployment/<operator-deployment>
```

```markdown
**Ação:** Logs com follow
```

```bash ignore-test
oc logs -n <namespace> deployment/<operator-deployment> -f
```

```markdown
**Ação:** Logs anteriores (se crashou)
```

```bash ignore-test
oc logs -n <namespace> <operator-pod> --previous
```

### Troubleshoot Subscription
```markdown
**Ação:** Ver subscription
```

```bash ignore-test
oc get subscription <name> -n <namespace> -o yaml
```

```markdown
**Ação:** Ver status
```

```bash ignore-test
oc get subscription <name> -n <namespace> -o jsonpath='{.status}'
```

```markdown
**Ação:** Ver CSV instalado
```

```bash ignore-test
oc get subscription <name> -n <namespace> -o jsonpath='{.status.installedCSV}'
```

```markdown
**Ação:** Ver conditions
```

```bash ignore-test
oc get subscription <name> -n <namespace> -o jsonpath='{.status.conditions}'
```

```markdown
**Ação:** Recrear subscription (deletar e criar novamente)
* Recriar...
```

```bash ignore-test
oc delete subscription <name> -n <namespace>
```

### Operator Não Instala
```markdown
**Ação:** Verificar catalog source
```

```bash
oc get catalogsource -n openshift-marketplace
oc get pods -n openshift-marketplace
```

```markdown
**Ação:** Ver packagemanifest
```

```bash ignore-test
oc get packagemanifest <operator> -n openshift-marketplace
```

```markdown
**Ação:** Verificar install plan
```

```bash ignore-test
oc get installplan -n <namespace>
oc describe installplan <plan> -n <namespace>
```

```markdown
**Ação:** Exibir logs do pod especificado
**Exemplo:** `oc logs -n <namespace> deployment/olm-operator`
**Ação:** oc logs -n <namespace> deployment/catalog-operator
```

```bash
oc logs -n openshift-operator-lifecycle-manager deployment/olm-operator
oc logs -n openshift-operator-lifecycle-manager deployment/catalog-operator
```

```markdown
**Ação:** Eventos
```

```bash ignore-test
oc get events -n <namespace> --sort-by='.lastTimestamp'
```

### CR Não Cria Recursos
```markdown
**Ação:** Verificar se operator está rodando
```

```bash ignore-test
oc get pods -n <operator-namespace>
```

```markdown
**Ação:** Logs do operator
```

```bash ignore-test
oc logs -n <operator-namespace> <operator-pod>
```

```markdown
**Ação:** Ver status do CR
```

```bash ignore-test
oc describe <cr-type> <cr-name>
```

```markdown
**Ação:** Ver eventos
```

```bash ignore-test
oc get events --field-selector involvedObject.name=<cr-name>
```

```markdown
**Ação:** Verificar RBAC
```

```bash ignore-test
oc auth can-i create pods --as=system:serviceaccount:<namespace>:<sa>
```

```markdown
**Ação:** Ver service account do operator
```

```bash ignore-test
oc get deployment <operator> -n <namespace> -o jsonpath='{.spec.template.spec.serviceAccountName}'
oc describe sa <sa-name> -n <namespace>
```

### Remover Operator
```markdown
**Ação:** 1. Deletar todos os CRs criados
```

```bash ignore-test
oc get <cr-type> -A
oc delete <cr-type> <name> -n <namespace>
```

```markdown
**Ação:** 2. Deletar subscription
```

```bash ignore-test
oc delete subscription <name> -n <namespace>
```

```markdown
**Ação:** 3. Deletar CSV
```

```bash ignore-test
oc delete csv <csv-name> -n <namespace>
```

```markdown
**Ação:** 4. (Opcional) Deletar CRDs
```

```bash ignore-test
oc delete crd <crd-name>
```

```markdown
**Ação:** 5. (Opcional) Deletar namespace
```

```bash ignore-test
oc delete namespace <namespace>
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators">Operators - Understanding Operators</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators/administrator-tasks">Operators - Administrator tasks</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators/user-tasks">Operators - User tasks</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators">Operator Lifecycle Manager</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/operators">Custom Resources</a>
---

---

## Navegação

- [← Anterior: Jobs e CronJobs](29-jobs-cronjobs.md)
- [→ Próximo: Troubleshooting de Upgrade do Cluster](31-troubleshooting-upgrade.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
