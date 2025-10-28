# Comandos Customizados com AWK, jq, GREP e Pipes

Este documento contém comandos avançados do OpenShift combinados com ferramentas Unix para automação e análise de dados.

---

## Índice

1. [Índice](#índice)
2. [Comandos com AWK](#comandos-com-awk)
3. [Comandos com jq](#comandos-com-jq)
4. [Comandos com GREP](#comandos-com-grep)
5. [Pipes Complexos](#pipes-complexos)
6. [Automação e Scripts](#automação-e-scripts)
7. [Análise de Cluster Operators](#análise-de-cluster-operators)
8. [Extração de Certificados](#extração-de-certificados)
9. [Dicas e Truques](#dicas-e-truques)
10. [Recursos Adicionais](#recursos-adicionais)
11. [Documentação Oficial](#documentação-oficial)
12. [Navegação](#navegação)
---

## Comandos com AWK

### CSR Management com AWK
**Aprovar Certificate Signing Request (CSR)**

```bash ignore-test
oc adm certificate approve $(oc get csr | grep Pending | awk '{print $1}')
```

**Aprovar Certificate Signing Request (CSR)**

```bash ignore-test
oc adm certificate approve $(oc get csr | grep -v -E "Approved|NAME" | awk '{print $1}')
```

**Aprovar Certificate Signing Request (CSR)**

```bash ignore-test
oc adm certificate approve $(oc get csr | grep -i pending | awk '{print $1}')
```

### Análise de Recursos com AWK
**Listar status dos cluster operators com awk**

```bash
oc get co --no-headers | awk '{print $1,$3,$4,$5}'
```

**Listar nodes com informações detalhadas**

```bash
oc get nodes -o wide --no-headers | awk '{print $1, $6}'
```

**Listar pods com informações detalhadas**

```bash
oc get pods -o wide --no-headers | awk '{print $1, $7}'
```

**Listar pods com informações adicionais (formato wide)**

```bash
oc get pods -o wide -A --no-headers | awk '{print $8}' | sort | uniq -c
```

**Listar pods com uso de CPU**

```bash
oc adm top pods --no-headers | awk '{print $1, $2}' | sort -k2 -h
```
**Listar pods com uso de CPU no cluster todo**

```bash
oc adm top pods -A --no-headers | awk '{print $2, $3}' | sort -k2 -h
```

**Encontrar pods com mais memória**

```bash
oc adm top pods --no-headers | awk '{print $1, $3}' | sort -k2 -h
```

**Encontrar pods com mais memória no cluster todo**

```bash
oc adm top pods -A --no-headers | awk '{print $2, $4}' | sort -k2 -h
```

### Builds com AWK
**Listar build de todos os namespaces do cluster**

```bash
oc get build -A --no-headers | awk '{print "oc describe build -n " $1 " " $2}'
```

**Listar build de todos os namespaces do cluster**

```bash
oc get build -A --no-headers | awk '{print "oc describe build -n " $1 " " $2}' | sh | egrep "Name:|From Image:"
```

**Listar build de todos os namespaces do cluster**

```bash
oc get build -A --no-headers | awk '{print "oc describe build -n " $1 " " $2}' | sh | egrep "Name:|From Image:" | tee /tmp/build-images.txt
```

### Service Mesh com AWK
**Extrair versão do Service Mesh Operator**

```bash ignore-test
oc -n openshift-operators get deployment.apps/istio-operator -o jsonpath='{.metadata.ownerReferences[0].name}' | awk -F "." '{print $2"."$3}' | cut -c2-
```

---

## Comandos com jq

### Análise de Cluster Operators
**Exibir cluster operators em formato JSON completo**

```bash ignore-test
oc get clusteroperators -o json | jq -r '.items[] | [.metadata.name, (.status.conditions[] | select(.type=="Progressing").status), (.status.conditions[] | select(.type=="Degraded").status), (.status.conditions[] | select(.type=="Degraded").message)] | @tsv'
```

**Exibir clusteroperator/operator-lifecycle-manager-packageserver em formato JSON completo**

```bash
oc get clusteroperator/operator-lifecycle-manager-packageserver -o json | jq
```

**Exibir cluster operator em formato JSON completo**

```bash ignore-test
oc get co -o json | jq '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

### Análise de Pods
**Exibir pods em formato JSON completo**

```bash ignore-test
oc get pods -o json | jq '.items[] | select(.status.containerStatuses[]?.lastState.terminated.reason=="OOMKilled") | .metadata.name'
```

**Exibir pods em formato JSON completo**

```bash ignore-test
oc get pods -o json | jq '.items[] | {name: .metadata.name, cpu: .spec.containers[].resources.requests.cpu, memory: .spec.containers[].resources.requests.memory}'
```

**Exibir pods em formato JSON completo**

```bash ignore-test
oc get pods -o json | jq '.items[] | select(.status.phase=="Running") | .metadata.name'
```

**Exibir pods em formato JSON completo**

```bash ignore-test
oc get pods -o json | jq '.items[].spec.containers[].image' | sort -u
```

### Análise de Applications (ArgoCD)
**Exibir recurso "workshop-vms-prd" em formato JSON**

```bash
oc get application workshop-vms-prd -n openshift-gitops -o jsonpath='{.status.conditions}' | jq .
```

**Exibir recurso "workshop-gitops-vms-hml" em formato JSON**

```bash
oc get application workshop-gitops-vms-hml -n openshift-gitops -o jsonpath='{.spec.syncPolicy}' | jq
```

**Exibir recurso "workshop-vms-dev" em formato JSON**

```bash ignore-test
oc get application workshop-vms-dev -n openshift-gitops -o json | jq '.status.resources[] | select(.kind == "Pod")'
```

### Análise de ClusterLogForwarder
**Exibir recurso "instance" em formato JSON**

```bash ignore-test
oc get clusterlogforwarder instance -n openshift-logging -o jsonpath='{.status.conditions[?(@.type=="Ready")]}' | jq '.'
```

**Exibir recurso "instance" em formato JSON**

```bash
oc get clusterlogforwarder instance -n openshift-logging -o jsonpath='{.status.filterConditions}' | jq '.'
```

### CSR com jq
**Aprovar Certificate Signing Request (CSR)**

```bash ignore-test
oc get csr -ojson | jq -r '.items[] | select(.status == {}) | .metadata.name' | xargs oc adm certificate approve
```

**Exibir certificate signing request em formato JSON completo**

```bash ignore-test
oc get csr -o json | jq '.items[] | select(.status.conditions == null) | {name: .metadata.name, user: .spec.username}'
```

### Análise de Secrets
**Exibir recurso em formato JSON**

```bash
oc get $(oc get secrets -n openshift-authentication -o name | grep oauth-openshift-token | tail -1) -n openshift-authentication -o jsonpath='{.data.ca\.crt}' | base64 -d
```

**Exibir recurso em formato JSON**

```bash
oc get $(oc get secrets -n openshift-authentication -o name | grep oauth-openshift-token | tail -1) -n openshift-authentication -o jsonpath='{.data.ca\.crt}' | base64 -d > /tmp/bundle-ca.crt
```

### Must-Gather Dinâmico com jq
**Coletar dados de diagnóstico completo do cluster**

```bash ignore-test
oc adm must-gather \
  --image-stream=openshift/must-gather \
  `$(oc get ns | grep -q openshift-logging) && \
    logging_mg=$(oc -n openshift-logging get deployment/cluster-logging-operator -o jsonpath='{.metadata.ownerReferences[0].name}'); \
    echo "--image=$(oc -n openshift-logging get csv/$logging_mg -o json | jq '.spec.relatedImages[] | select (.name | contains ("cluster-logging-operator")) | .image' | sed 's/"//g')"` \
  `$(oc get ns | grep -q openshift-storage) && \
    odf_mg=$(oc -n openshift-storage get deployment.apps/ocs-operator -o jsonpath='{.metadata.ownerReferences[0].name}'); \
    echo "--image=$(oc -n openshift-storage get csv/$odf_mg -o json | jq '.spec.relatedImages[] | select (.name | contains ("must-gather")) | .image' | sed 's/"//g')"`
```

---

## Comandos com GREP 

### Filtros Complexos
**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A | grep -E -v "Running|Completed"
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A | grep -E "Error|CrashLoopBackOff|ImagePullBackOff"
```

**Cluster operators com problemas**

```bash
oc get co | grep -v "True.*False.*False"
```

**Nodes não-Ready**

```bash
oc get nodes | grep -v "Ready"
```

**Filtrar eventos importantes**

```bash ignore-test
oc describe pod <pod-name> | grep -A 10 "Events:"
```

### Análise de Configurações
**Exibir recurso em formato YAML**

```bash
oc get all -o yaml | grep -A5 limits
```

**Listar recurso de todos os namespaces do cluster**

```bash
oc get all -A | grep redhat-operator
```

**Listar recurso de todos os namespaces do cluster**

```bash
oc get all -A | grep metrics
```

**Exibir recurso em formato YAML**

```bash
oc get all -o yaml | grep 5000
```

### Busca em AdminNetworkPolicy
**Exibir recurso em formato YAML**

```bash
oc get adminnetworkpolicy deny-cross-namespace-communication -o yaml | grep -A 30 "ingress:" | head -40
```

### Análise de ArgoCD
**Listar recurso de todos os namespaces do cluster**

```bash ignore-test
oc get application.argoproj.io workshop-vms-dev -n openshift-gitops -o yaml | grep -A 10 source
```

**Listar recurso de todos os namespaces do cluster**

```bash ignore-test
oc get application.argoproj.io workshop-vms-dev -n openshift-gitops -o yaml | grep -A 5 destination
```

**Listar recurso de todos os namespaces do cluster**

```bash ignore-test
oc get application workshop-gitops-vms-hml -n openshift-gitops -o yaml | grep -A 5 -B 5 sync
```

**Listar recurso de todos os namespaces do cluster**

```bash ignore-test
oc get application workshop-vms-dev -n openshift-gitops -o yaml | grep -A 20 -B 5 "message"
```

### Filtros em CatalogSource
**Listar recurso de todos os namespaces do cluster**

```bash
oc get catalogsource certified-operators -n openshift-marketplace -o yaml | grep -A 10 status:
```

**Filtrar catalogs da Red Hat**

```bash
oc get catalogsource -n openshift-marketplace | grep redhat
```

---

## Pipes Complexos

### Análise de API Requests
**Exibir recurso "ingresses.v1beta1.extensions" em formato JSON**

```bash ignore-test
oc get apirequestcounts ingresses.v1beta1.extensions -o jsonpath='{range .status.currentHour..byUser[*]}{..byVerb[*].verb}{","}{.username}{","}{.userAgent}{"\n"}{end}' | sort -k 2 -t, -u | column -t -s, -NVERBS,USERNAME,USERAGENT
```

**Exibir recurso "ingresses.v1beta1.networking.k8s.io" em formato JSON**

```bash ignore-test
oc get apirequestcounts ingresses.v1beta1.networking.k8s.io -o jsonpath='{range .status.currentHour..byUser[*]}{..byVerb[*].verb}{","}{.username}{","}{.userAgent}{"\n"}{end}' | sort -k 2 -t, -u | column -t -s, -NVERBS,USERNAME,USERAGENT
```

**Exibir recurso "roles.v1beta1.rbac.authorization.k8s.io" em formato JSON**

```bash ignore-test
oc get apirequestcounts roles.v1beta1.rbac.authorization.k8s.io -o jsonpath='{range .status.currentHour..byUser[*]}{..byVerb[*].verb}{","}{.username}{","}{.userAgent}{"\n"}{end}' | sort -k 2 -t, -u | column -t -s, -NVERBS,USERNAME,USERAGENT
```

### Análise de ClusterOperators com Tabela
**Exibir cluster operators em formato JSON**

```bash ignore-test
oc get clusteroperators -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .status.conditions[?(@.type=="Progressing")]}{.status}{"\t"}{end}{range .status.conditions[?(@.type=="Degraded")]}{.status}{"\t"}{.message}{"\n"}{end}{end}' | column -t -s $'\t'
```

### Exportar Applications ArgoCD
**Exibir recurso em formato YAML**

```bash
oc get application -A -o yaml | sed '/creationTimestamp\|resourceVersion\|uid/d'
```

**Exibir recurso em formato YAML**

```bash
oc get application -A -o yaml | sed '/creationTimestamp\|resourceVersion\|uid/d' > /tmp/argocd-apps-$(date +'%d%m%y_%H%M%S').yaml
```

**Exibir recurso em formato YAML**

```bash
oc get application -A -o yaml | sed '/status:/d'
```

### Verificações Condicionais
**Verificar se aplicação existe**

```bash
oc get applications.argoproj.io -n openshift-gitops  || echo "No applications found"
```

**Exibir recurso "workshop-gitops-vms-dev" em formato JSON**

```bash
oc get application workshop-gitops-vms-dev -n openshift-gitops -o jsonpath='{.status.health.status}'  || echo "Application not found"
```

**Exibir recurso "workshop-vms-prd" em formato JSON**

```bash ignore-test
oc get application workshop-vms-prd -n openshift-gitops -o jsonpath='{.status.conditions[0].message}'  || echo "No error condition found"
```

---

## Automação e Scripts

### Loop para Coletar Logs
**Coletar logs de todos os pods em um arquivo**

```bash ignore-test
for pod in $(oc get pods -o name); do
  echo "=== $pod ===" >> /tmp/all-logs.txt
  oc logs $pod >> /tmp/all-logs.txt
done
```

**Exibir recurso em formato JSON**

```bash ignore-test
for pod in $(oc get pods -o jsonpath="{range .items[?(@.status.containerStatuses[*].state.waiting.reason=='CrashLoopBackOff')]}{.metadata.name}{'\n'}{end}"); do
  echo "=== $pod ===" >> /tmp/error-logs.txt
  oc logs $pod --previous >> /tmp/error-logs.txt
done
```

### Verificação de ArgoCD Apps
**Loop para verificar múltiplas aplicações**

```bash ignore-test
for app in $(oc get applications.argoproj.io -n openshift-gitops --no-headers | awk '{print $1}'); do
  echo "Application: $app"
  oc get application $app -n openshift-gitops -o jsonpath='{.status.health.status}'
  echo ""
done
```

### Aprovar CSRs em Loop
**Aprovar CSRs pendentes até não haver mais**

```bash ignore-test
while true; do
  csrs=$(oc get csr | grep Pending | awk '{print $1}')
  if [ -z "$csrs" ]; then
    echo "No pending CSRs"
    break
  fi
  oc adm certificate approve $csrs
  sleep 5
done
```

**Aprovar CSRs até executar o cancelamento (pressione ctrl+c para cancelar)**

```bash ignore-test
while true; do
  csrs=$(oc get csr | grep Pending | awk '{print $1}')
  if [ -z "$csrs" ]; then
    echo "$(date "+%Y-%m-%d %H:%M:%S") No pending CSRs"
    sleep 5
    continue
  fi
  oc adm certificate approve $csrs
done
```

### Verificação de Nodes
**Verificar status de todos os nodes**

```bash ignore-test
for node in $(oc get nodes -o name); do
  echo "=== $node ==="
  oc describe $node | grep -A 5 "Conditions:"
  echo ""
done
```

---

## Análise de Cluster Operators

### Status Completo
**Exibir cluster operator em formato JSON completo**

```bash
oc get co -o json | jq -r '.items[] | "\(.metadata.name): Available=\(.status.conditions[] | select(.type=="Available").status), Progressing=\(.status.conditions[] | select(.type=="Progressing").status), Degraded=\(.status.conditions[] | select(.type=="Degraded").status)"'
```

**Exibir cluster operator em formato JSON completo**

```bash
oc get co -o json | jq '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | {name: .metadata.name, message: (.status.conditions[] | select(.type=="Degraded").message)}'
```

**Exibir cluster operator em formato JSON**

```bash
oc get co -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.versions[0].version}{"\n"}{end}' | column -t
```

### APIServices
**Ver apiservices com problemas**

```bash
oc get apiservice | grep -v True
```

**Exibir recurso "v1beta1.metrics.k8s.io" em formato JSON**

```bash
oc get apiservice v1beta1.metrics.k8s.io -o jsonpath='{.spec.caBundle}' | base64 -d | openssl x509 -text
```

**Exibir recurso "v1.packages.operators.coreos.com" em formato JSON**

```bash
oc get apiservice v1.packages.operators.coreos.com -o jsonpath='{.spec.caBundle}' | base64 -d | openssl x509 -noout -text
```

---

## Extração de Certificados

### Extrair e Analisar Certificados
**Extrair certificado de service**

```bash ignore-test
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

**Ver expiração do certificado**

```bash ignore-test
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -enddate
```

**Exibir recurso "v1beta1.metrics.k8s.io" em formato JSON**

```bash
oc get apiservice v1beta1.metrics.k8s.io -o jsonpath='{.spec.caBundle}' | base64 -d | openssl x509 -text
```

**Exibir recurso em formato JSON**

```bash
oc get $(oc get secrets -n openshift-authentication -o name | grep oauth-openshift-token | tail -1) -n openshift-authentication -o jsonpath='{.data.ca\.crt}' | base64 -d > /tmp/oauth-ca-bundle.crt
```

---

## Dicas e Truques

### Combinando Comandos
**Ver pods com mais uso de CPU**

```bash
oc adm top pods -A --no-headers | sort -k3 -nr | head -10
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A -o wide --no-headers | awk '{print $8}' | sort | uniq -c | sort -nr
```

**Listar recurso de todos os namespaces do cluster**

```bash
oc get all -A --no-headers | awk '{print $1}' | sort | uniq -c
```

### Aliases Úteis para Scripts
**Listar recurso de todos os namespaces do cluster**

```bash ignore-test
alias ocpods='oc get pods -A | grep -E -v "Running|Completed"'
alias occo='oc get co | grep -v "True.*False.*False"'
alias occsrfix='oc get csr -o name | xargs oc adm certificate approve'
alias octop='oc adm top pods -A --no-headers | sort -k3 -nr | head -10'
```

### Verificações Rápidas
**Health check completo do cluster**

```bash
echo "=== Cluster Operators ===" && (oc get co | grep -v "True.*False.*False" || echo "Todos os operators estão saudáveis") && \
echo "=== Problematic Pods ===" && (oc get pods -A | grep -E -v "Running|Completed" || echo "Nenhum pod com problema") && \
echo "=== Pending CSRs ===" && (oc get csr | grep Pending || echo "Nenhum CSR pendente") && \
echo "=== Non-Ready Nodes ===" && (oc get nodes | grep -v "Ready" || echo "Todos os nodes estão Ready")
```

---

## Recursos Adicionais

- **jq Manual**: https://stedolan.github.io/jq/manual/
- **AWK Tutorial**: https://www.gnu.org/software/gawk/manual/
- **GREP Guide**: https://www.gnu.org/software/grep/manual/

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools">CLI Tools - Using the OpenShift CLI</a>
---


## Navegação

- [← Voltar para Networking](22-networking.md)
- [→ Próximo: Field Selectors](24-field-selectors.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
