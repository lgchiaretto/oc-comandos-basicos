# Comandos Customizados com AWK, JQ, GREP e Pipes

Este documento contém comandos avançados do OpenShift combinados com ferramentas Unix para automação e análise de dados.

---

## Índice

1. [Índice](#índice)
2. [Comandos com AWK](#comandos-com-awk)
3. [Comandos com JQ](#comandos-com-jq)
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
```bash ignore-test
# Aprovar Certificate Signing Request (CSR)
oc adm certificate approve $(oc get csr | grep Pending | awk '{print $1}')
```

```bash ignore-test
# Aprovar Certificate Signing Request (CSR)
oc adm certificate approve $(oc get csr | grep -v -E "Approved|NAME" | awk '{print $1}')
```

```bash ignore-test
# Aprovar Certificate Signing Request (CSR)
oc adm certificate approve $(oc get csr | grep -i pending | awk '{print $1}')
```

### Análise de Recursos com AWK
```bash
# Listar status dos cluster operators com awk
oc get co --no-headers | awk '{print $1,$3,$4,$5}'
```

```bash
# Listar nodes com informações detalhadas
oc get nodes -o wide --no-headers | awk '{print $1, $6}'
```

```bash
# Listar pods com informações detalhadas
oc get pods -o wide --no-headers | awk '{print $1, $7}'
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -o wide -A --no-headers | awk '{print $8}' | sort | uniq -c
```

```bash
# Listar pods com uso de CPU (requer metrics-server)
oc adm top pods --no-headers | awk '{print $1, $2}' | sort -k2 -h
```
```bash
# Listar pods com uso de CPU no cluster todo (requer metrics-server)
oc adm top pods -A --no-headers | awk '{print $2, $3}' | sort -k2 -h
```

```bash
# Encontrar pods com mais memória
oc adm top pods --no-headers | awk '{print $1, $3}' | sort -k2 -h
```

```bash
# Encontrar pods com mais memória no cluster todo
oc adm top pods -A --no-headers | awk '{print $2, $4}' | sort -k2 -h
```

### Builds com AWK
```bash
# Listar build de todos os namespaces do cluster
oc get build -A --no-headers | awk '{print "oc describe build -n " $1 " " $2}'
```

```bash
# Listar build de todos os namespaces do cluster
oc get build -A --no-headers | awk '{print "oc describe build -n " $1 " " $2}' | sh | egrep "Name:|From Image:"
```

```bash
# Listar build de todos os namespaces do cluster
oc get build -A --no-headers | awk '{print "oc describe build -n " $1 " " $2}' | sh | egrep "Name:|From Image:" | tee /tmp/build-images.txt
```

### Service Mesh com AWK
```bash ignore-test
# Extrair versão do Service Mesh Operator
oc -n openshift-operators get deployment.apps/istio-operator -o jsonpath='{.metadata.ownerReferences[0].name}' | awk -F "." '{print $2"."$3}' | cut -c2-
```

---

## Comandos com JQ

### Análise de Cluster Operators
```bash ignore-test
# Exibir cluster operators em formato JSON
oc get clusteroperators -o json | jq -r '.items[] | [.metadata.name, (.status.conditions[] | select(.type=="Progressing").status), (.status.conditions[] | select(.type=="Degraded").status), (.status.conditions[] | select(.type=="Degraded").message)] | @tsv'
```

```bash
# Exibir cluster operator em formato JSON
oc get clusteroperator/operator-lifecycle-manager-packageserver -o json | jq
```

```bash ignore-test
# Exibir cluster operator em formato JSON
oc get co -o json | jq '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

### Análise de Pods
```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o json | jq '.items[] | select(.status.containerStatuses[]?.lastState.terminated.reason=="OOMKilled") | .metadata.name'
```

```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o json | jq '.items[] | {name: .metadata.name, cpu: .spec.containers[].resources.requests.cpu, memory: .spec.containers[].resources.requests.memory}'
```

```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o json | jq '.items[] | select(.status.phase=="Running") | .metadata.name'
```

```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o json | jq '.items[].spec.containers[].image' | sort -u
```

### Análise de Applications (ArgoCD)
```bash
# Exibir recurso "workshop-vms-prd" em formato JSON
# oc get application <resource-name>prd -n <namespace> -o jsonpath='{.status.conditions}' | jq .
oc get application workshop-vms-prd -n openshift-gitops -o jsonpath='{.status.conditions}' | jq .
```

```bash
# Exibir recurso "workshop-gitops-vms-hml" em formato JSON
# oc get application <resource-name>hml -n <namespace> -o jsonpath='{.spec.syncPolicy}' | jq
oc get application workshop-gitops-vms-hml -n openshift-gitops -o jsonpath='{.spec.syncPolicy}' | jq
```

```bash ignore-test
# Exibir recurso "workshop-vms-dev" em formato JSON
# oc get application <resource-name>dev -n <namespace> -o json | jq '.status.resources[] | select(.kind == "Pod")'
oc get application workshop-vms-dev -n openshift-gitops -o json | jq '.status.resources[] | select(.kind == "Pod")'
```

### Análise de ClusterLogForwarder
```bash ignore-test
# Exibir recurso "instance" em formato JSON
# oc get clusterlogforwarder instance -n <namespace> -o jsonpath='{.status.conditions[?(@.type=="Ready")]}' | jq '.'
oc get clusterlogforwarder instance -n openshift-logging -o jsonpath='{.status.conditions[?(@.type=="Ready")]}' | jq '.'
```

```bash
# Exibir recurso "instance" em formato JSON
# oc get clusterlogforwarder instance -n <namespace> -o jsonpath='{.status.filterConditions}' | jq '.'
oc get clusterlogforwarder instance -n openshift-logging -o jsonpath='{.status.filterConditions}' | jq '.'
```

### CSR com JQ
```bash ignore-test
# Aprovar Certificate Signing Request (CSR)
oc get csr -ojson | jq -r '.items[] | select(.status == {}) | .metadata.name' | xargs oc adm certificate approve
```

```bash ignore-test
# Exibir certificate signing request em formato JSON
oc get csr -o json | jq '.items[] | select(.status.conditions == null) | {name: .metadata.name, user: .spec.username}'
```

### Análise de Secrets
```bash
# Exibir recurso em formato JSON
oc get $(oc get secrets -n openshift-authentication -o name | grep oauth-openshift-token | tail -1) -n openshift-authentication -o jsonpath='{.data.ca\.crt}' | base64 -d
```

```bash
# Exibir recurso em formato JSON
oc get $(oc get secrets -n openshift-authentication -o name | grep oauth-openshift-token | tail -1) -n openshift-authentication -o jsonpath='{.data.ca\.crt}' | base64 -d > /tmp/bundle-ca.crt
```

### Must-Gather Dinâmico com JQ
```bash ignore-test
# Coletar dados de diagnóstico completo do cluster
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
```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep -E -v "Running|Completed"
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep -E "Error|CrashLoopBackOff|ImagePullBackOff"
```

```bash
# Cluster operators com problemas
oc get co | grep -v "True.*False.*False"
```

```bash
# Nodes não-Ready
oc get nodes | grep -v "Ready"
```

```bash ignore-test
# Filtrar eventos importantes
oc describe pod <pod-name> | grep -A 10 "Events:"
```

### Análise de Configurações
```bash
# Listar recurso de todos os namespaces do cluster
oc get all -o yaml | grep -A5 limits
```

```bash
# Listar recurso de todos os namespaces do cluster
oc get all -A | grep redhat-operator
```

```bash
# Listar recurso de todos os namespaces do cluster
oc get all -A | grep metrics
```

```bash
# Exibir recurso em formato YAML
oc get all -o yaml | grep 5000
```

### Busca em AdminNetworkPolicy
```bash
# Listar recurso de todos os namespaces do cluster
# oc get adminnetworkpolicy <resource-name>communication -o yaml | grep -A 30 "ingress:" | head -40
oc get adminnetworkpolicy deny-cross-namespace-communication -o yaml | grep -A 30 "ingress:" | head -40
```

### Análise de ArgoCD
```bash ignore-test
# Listar recurso de todos os namespaces do cluster
# oc get application.argoproj.io workshop-vms-dev -n <namespace> -o yaml | grep -A 10 source
oc get application.argoproj.io workshop-vms-dev -n openshift-gitops -o yaml | grep -A 10 source
```

```bash ignore-test
# Listar recurso de todos os namespaces do cluster
# oc get application.argoproj.io workshop-vms-dev -n <namespace> -o yaml | grep -A 5 destination
oc get application.argoproj.io workshop-vms-dev -n openshift-gitops -o yaml | grep -A 5 destination
```

```bash ignore-test
# Listar recurso de todos os namespaces do cluster
# oc get application <resource-name>hml -n <namespace> -o yaml | grep -A 5 -B 5 sync
oc get application workshop-gitops-vms-hml -n openshift-gitops -o yaml | grep -A 5 -B 5 sync
```

```bash ignore-test
# Listar recurso de todos os namespaces do cluster
# oc get application <resource-name>dev -n <namespace> -o yaml | grep -A 20 -B 5 "message"
oc get application workshop-vms-dev -n openshift-gitops -o yaml | grep -A 20 -B 5 "message"
```

### Filtros em CatalogSource
```bash
# Listar recurso de todos os namespaces do cluster
# oc get catalogsource <resource-name>operators -n <namespace> -o yaml | grep -A 10 status:
oc get catalogsource certified-operators -n openshift-marketplace -o yaml | grep -A 10 status:
```

```bash
# Filtrar catalogs da Red Hat
oc get catalogsource -n openshift-marketplace | grep redhat
```

---

## Pipes Complexos

### Análise de API Requests
```bash ignore-test
# Exibir recurso "ingresses.v1beta1.extensions" em formato JSON
# oc get apirequestcounts <resource-name>.v1beta1.extensions -o jsonpath='{range .status.currentHour..byUser[*]}{..byVerb[*].verb}{","}{.username}{","}{.userAgent}{"\n"}{end}' | sort -k 2 -t, -u | column -t -s, -NVERBS,USERNAME,USERAGENT
oc get apirequestcounts ingresses.v1beta1.extensions -o jsonpath='{range .status.currentHour..byUser[*]}{..byVerb[*].verb}{","}{.username}{","}{.userAgent}{"\n"}{end}' | sort -k 2 -t, -u | column -t -s, -NVERBS,USERNAME,USERAGENT
```

```bash ignore-test
# Exibir recurso "ingresses.v1beta1.networking.k8s.io" em formato JSON
# oc get apirequestcounts <resource-name>.v1beta1.networking.k8s.io -o jsonpath='{range .status.currentHour..byUser[*]}{..byVerb[*].verb}{","}{.username}{","}{.userAgent}{"\n"}{end}' | sort -k 2 -t, -u | column -t -s, -NVERBS,USERNAME,USERAGENT
oc get apirequestcounts ingresses.v1beta1.networking.k8s.io -o jsonpath='{range .status.currentHour..byUser[*]}{..byVerb[*].verb}{","}{.username}{","}{.userAgent}{"\n"}{end}' | sort -k 2 -t, -u | column -t -s, -NVERBS,USERNAME,USERAGENT
```

```bash ignore-test
# Exibir recurso "roles.v1beta1.rbac.authorization.k8s.io" em formato JSON
# oc get apirequestcounts <resource-name>.v1beta1.rbac.authorization.k8s.io -o jsonpath='{range .status.currentHour..byUser[*]}{..byVerb[*].verb}{","}{.username}{","}{.userAgent}{"\n"}{end}' | sort -k 2 -t, -u | column -t -s, -NVERBS,USERNAME,USERAGENT
oc get apirequestcounts roles.v1beta1.rbac.authorization.k8s.io -o jsonpath='{range .status.currentHour..byUser[*]}{..byVerb[*].verb}{","}{.username}{","}{.userAgent}{"\n"}{end}' | sort -k 2 -t, -u | column -t -s, -NVERBS,USERNAME,USERAGENT
```

### Análise de ClusterOperators com Tabela
```bash ignore-test
# Exibir cluster operators em formato JSON
oc get clusteroperators -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .status.conditions[?(@.type=="Progressing")]}{.status}{"\t"}{end}{range .status.conditions[?(@.type=="Degraded")]}{.status}{"\t"}{.message}{"\n"}{end}{end}' | column -t -s $'\t'
```

### Exportar Applications ArgoCD
```bash
# Listar recurso de todos os namespaces do cluster
oc get application -A -o yaml | sed '/creationTimestamp\|resourceVersion\|uid/d'
```

```bash
# Listar recurso de todos os namespaces do cluster
oc get application -A -o yaml | sed '/creationTimestamp\|resourceVersion\|uid/d' > /tmp/argocd-apps-$(date +'%d%m%y_%H%M%S').yaml
```

```bash
# Listar recurso de todos os namespaces do cluster
oc get application -A -o yaml | sed '/status:/d'
```

### Verificações Condicionais
```bash
# Verificar se aplicação existe
# oc get applications.argoproj.io -n <namespace>  || echo "No applications found"
oc get applications.argoproj.io -n openshift-gitops  || echo "No applications found"
```

```bash
# Exibir recurso "workshop-gitops-vms-dev" em formato JSON
# oc get application <resource-name>dev -n <namespace> -o jsonpath='{.status.health.status}'  || echo "Application not found"
oc get application workshop-gitops-vms-dev -n openshift-gitops -o jsonpath='{.status.health.status}'  || echo "Application not found"
```

```bash ignore-test
# Exibir recurso "workshop-vms-prd" em formato JSON
# oc get application <resource-name>prd -n <namespace> -o jsonpath='{.status.conditions[0].message}'  || echo "No error condition found"
oc get application workshop-vms-prd -n openshift-gitops -o jsonpath='{.status.conditions[0].message}'  || echo "No error condition found"
```

---

## Automação e Scripts

### Loop para Coletar Logs
```bash ignore-test
# Coletar logs de todos os pods em um arquivo
for pod in $(oc get pods -o name); do
  echo "=== $pod ===" >> /tmp/all-logs.txt
  oc logs $pod >> /tmp/all-logs.txt
done
```

```bash ignore-test
# Exibir recurso em formato JSON
for pod in $(oc get pods -o jsonpath="{range .items[?(@.status.containerStatuses[*].state.waiting.reason=='CrashLoopBackOff')]}{.metadata.name}{'\n'}{end}"); do
  echo "=== $pod ===" >> /tmp/error-logs.txt
  oc logs $pod --previous >> /tmp/error-logs.txt
done
```

### Verificação de ArgoCD Apps
```bash ignore-test
# Loop para verificar múltiplas aplicações
for app in $(oc get applications.argoproj.io -n openshift-gitops --no-headers | awk '{print $1}'); do
  echo "Application: $app"
  oc get application $app -n openshift-gitops -o jsonpath='{.status.health.status}'
  echo ""
done
```

### Aprovar CSRs em Loop
```bash ignore-test
# Aprovar CSRs pendentes até não haver mais
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

```bash ignore-test
# Aprovar CSRs até executar o cancelamento (pressione ctrl+c para cancelar)
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
```bash ignore-test
# Verificar status de todos os nodes
for node in $(oc get nodes -o name); do
  echo "=== $node ==="
  oc describe $node | grep -A 5 "Conditions:"
  echo ""
done
```

---

## Análise de Cluster Operators

### Status Completo
```bash
# Exibir cluster operator em formato JSON
oc get co -o json | jq -r '.items[] | "\(.metadata.name): Available=\(.status.conditions[] | select(.type=="Available").status), Progressing=\(.status.conditions[] | select(.type=="Progressing").status), Degraded=\(.status.conditions[] | select(.type=="Degraded").status)"'
```

```bash
# Exibir cluster operator em formato JSON
oc get co -o json | jq '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | {name: .metadata.name, message: (.status.conditions[] | select(.type=="Degraded").message)}'
```

```bash
# Exibir cluster operator em formato JSON
oc get co -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.versions[0].version}{"\n"}{end}' | column -t
```

### APIServices
```bash
# Ver apiservices com problemas
oc get apiservice | grep -v True
```

```bash
# Exibir recurso "v1beta1.metrics.k8s.io" em formato JSON
# oc get apiservice <service-name>.metrics.k8s.io -o jsonpath='{.spec.caBundle}' | base64 -d | openssl x509 -text
oc get apiservice v1beta1.metrics.k8s.io -o jsonpath='{.spec.caBundle}' | base64 -d | openssl x509 -text
```

```bash
# Exibir recurso "v1.packages.operators.coreos.com" em formato JSON
# oc get apiservice <service-name>.packages.operators.coreos.com -o jsonpath='{.spec.caBundle}' | base64 -d | openssl x509 -noout -text
oc get apiservice v1.packages.operators.coreos.com -o jsonpath='{.spec.caBundle}' | base64 -d | openssl x509 -noout -text
```

---

## Extração de Certificados

### Extrair e Analisar Certificados
```bash ignore-test
# Extrair certificado de service
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

```bash ignore-test
# Ver expiração do certificado
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -enddate
```

```bash
# Exibir recurso "v1beta1.metrics.k8s.io" em formato JSON
# oc get apiservice <service-name>.metrics.k8s.io -o jsonpath='{.spec.caBundle}' | base64 -d | openssl x509 -text
oc get apiservice v1beta1.metrics.k8s.io -o jsonpath='{.spec.caBundle}' | base64 -d | openssl x509 -text
```

```bash
# Exibir recurso em formato JSON
oc get $(oc get secrets -n openshift-authentication -o name | grep oauth-openshift-token | tail -1) -n openshift-authentication -o jsonpath='{.data.ca\.crt}' | base64 -d > /tmp/oauth-ca-bundle.crt
```

---

## Dicas e Truques

### Combinando Comandos
```bash
# Ver pods com mais uso de CPU
oc adm top pods -A --no-headers | sort -k3 -nr | head -10
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A -o wide --no-headers | awk '{print $8}' | sort | uniq -c | sort -nr
```

```bash
# Listar recurso de todos os namespaces do cluster
oc get all -A --no-headers | awk '{print $1}' | sort | uniq -c
```

### Aliases Úteis para Scripts
```bash ignore-test
# Listar recurso de todos os namespaces do cluster
alias ocpods='oc get pods -A | grep -E -v "Running|Completed"'
alias occo='oc get co | grep -v "True.*False.*False"'
alias occsrfix='oc get csr -o name | xargs oc adm certificate approve'
alias octop='oc adm top pods -A --no-headers | sort -k3 -nr | head -10'
```

### Verificações Rápidas
```bash
# Health check completo do cluster
echo "=== Cluster Operators ===" && (oc get co | grep -v "True.*False.*False" || echo "Todos os operators estão saudáveis") && \
echo "=== Problematic Pods ===" && (oc get pods -A | grep -E -v "Running|Completed" || echo "Nenhum pod com problema") && \
echo "=== Pending CSRs ===" && (oc get csr | grep Pending || echo "Nenhum CSR pendente") && \
echo "=== Non-Ready Nodes ===" && (oc get nodes | grep -v "Ready" || echo "Todos os nodes estão Ready")
```

---

## Recursos Adicionais

- **JQ Manual**: https://stedolan.github.io/jq/manual/
- **AWK Tutorial**: https://www.gnu.org/software/gawk/manual/
- **GREP Guide**: https://www.gnu.org/software/grep/manual/

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools">CLI Tools - Using the OpenShift CLI</a>
---

---

## Navegação

- [← Voltar para Networking](22-networking.md)
- [→ Próximo: Field Selectors](24-field-selectors.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
