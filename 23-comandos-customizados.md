# 🛠️ Comandos Customizados com AWK, JQ, GREP e Pipes

Este documento contém comandos avançados do OpenShift combinados com ferramentas Unix para automação e análise de dados.

---

## 📋 Índice

1. [Comandos com AWK](#comandos-com-awk)
2. [Comandos com JQ](#comandos-com-jq)
3. [Comandos com GREP e EGREP](#comandos-com-grep-e-egrep)
4. [Pipes Complexos](#pipes-complexos)
5. [Automação e Scripts](#automação-e-scripts)
6. [Análise de Cluster Operators](#análise-de-cluster-operators)
7. [Análise de API Requests](#análise-de-api-requests)
8. [Extração de Certificados](#extração-de-certificados)
9. [Storage e PVCs](#storage-e-pvcs)
10. [Permissões e Validações](#permissões-e-validações)

---

## 🔧 Comandos com AWK

### CSR Management com AWK
```bash
# Aprovar CSRs pendentes usando awk
oc adm certificate approve $(oc get csr | grep Pending | awk '{print $1}')
```

```bash
# Aprovar CSRs não aprovados
oc adm certificate approve $(oc get csr | grep -v -E "Approved|NAME" | awk '{print $1}')
```

```bash
# Aprovar apenas CSRs específicos
oc adm certificate approve $(oc get csr | grep -i pending | awk '{print $1}')
```

### Análise de Recursos com AWK
```bash
# Listar status dos cluster operators com awk
oc get co --no-headers | awk '{print $1,$3,$4,$5}'
```

```bash
# Extrair nomes e IPs dos nodes
oc get nodes -o wide --no-headers | awk '{print $1, $6}'
```

```bash
# Listar pods e seus nodes
oc get pods -o wide --no-headers | awk '{print $1, $7}'
```

```bash
# Contar pods por node
oc get pods -o wide --all-namespaces --no-headers | awk '{print $8}' | sort | uniq -c
```

```bash
# Listar pods com uso de CPU (requer metrics-server)
oc adm top pods --no-headers | awk '{print $1, $2}' | sort -k2 -h
```

```bash
# Encontrar pods com mais memória
oc adm top pods --no-headers | awk '{print $1, $3}' | sort -k2 -h
```

### Builds com AWK
```bash
# Gerar comandos describe para todos os builds
oc get build --all-namespaces --no-headers | awk '{print "oc describe build -n " $1 " " $2}'
```

```bash
# Executar describe em todos os builds e filtrar imagens
oc get build --all-namespaces --no-headers | awk '{print "oc describe build -n " $1 " " $2}' | sh | egrep "Name:|From Image:"
```

```bash
# Salvar resultado em arquivo
oc get build --all-namespaces --no-headers | awk '{print "oc describe build -n " $1 " " $2}' | sh | egrep "Name:|From Image:" | tee /tmp/build-images.txt
```

### Service Mesh com AWK
```bash
# Extrair versão do Service Mesh Operator
oc -n openshift-operators get deployment.apps/istio-operator -o jsonpath='{.metadata.ownerReferences[0].name}' | awk -F "." '{print $2"."$3}' | cut -c2-
```

---

## 📊 Comandos com JQ

### Análise de Cluster Operators
```bash
# Ver status detalhado dos cluster operators
oc get clusteroperators -o json | jq -r '.items[] | [.metadata.name, (.status.conditions[] | select(.type=="Progressing").status), (.status.conditions[] | select(.type=="Degraded").status), (.status.conditions[] | select(.type=="Degraded").message)] | @tsv'
```

```bash
# Listar operators com problemas
oc get clusteroperator/operator-lifecycle-manager-packageserver -o json | jq
```

```bash
# Filtrar operators degradados
oc get co -o json | jq '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

### Análise de Pods
```bash
# Encontrar pods com OOMKilled
oc get pods -o json | jq '.items[] | select(.status.containerStatuses[]?.lastState.terminated.reason=="OOMKilled") | .metadata.name'
```

```bash
# Ver recursos de todos os pods
oc get pods -o json | jq '.items[] | {name: .metadata.name, cpu: .spec.containers[].resources.requests.cpu, memory: .spec.containers[].resources.requests.memory}'
```

```bash
# Listar pods por fase
oc get pods -o json | jq '.items[] | select(.status.phase=="Running") | .metadata.name'
```

```bash
# Ver imagens de todos os containers
oc get pods -o json | jq '.items[].spec.containers[].image' | sort -u
```

### Análise de Applications (ArgoCD)
```bash
# Ver status de sync do ArgoCD app
oc get application workshop-vms-prd -n openshift-gitops -o jsonpath='{.status.conditions}' | jq .
```

```bash
# Ver sync policy
oc get application workshop-gitops-vms-hml -n openshift-gitops -o jsonpath='{.spec.syncPolicy}' | jq
```

```bash
# Listar recursos de uma aplicação
oc get application workshop-vms-dev -n openshift-gitops -o json | jq '.status.resources[] | select(.kind == "Pod")'
```

### Análise de ClusterLogForwarder
```bash
# Ver condições do log forwarder
oc get clusterlogforwarder instance -n openshift-logging -o jsonpath='{.status.conditions[?(@.type=="Ready")]}' | jq '.'
```

```bash
# Ver filter conditions
oc get clusterlogforwarder instance -n openshift-logging -o jsonpath='{.status.filterConditions}' | jq '.'
```

### CSR com JQ
```bash
# Listar CSRs com status vazio e aprovar
oc get csr -ojson | jq -r '.items[] | select(.status == {}) | .metadata.name' | xargs oc adm certificate approve
```

```bash
# Ver detalhes de CSRs pendentes
oc get csr -o json | jq '.items[] | select(.status.conditions == null) | {name: .metadata.name, user: .spec.username}'
```

### Análise de Secrets
```bash
# Extrair CA do secret oauth
oc get $(oc get secrets -n openshift-authentication -o name | grep oauth-openshift-token | tail -1) -n openshift-authentication -o jsonpath='{.data.ca\.crt}' | base64 -d
```

```bash
# Salvar CA bundle em arquivo
oc get $(oc get secrets -n openshift-authentication -o name | grep oauth-openshift-token | tail -1) -n openshift-authentication -o jsonpath='{.data.ca\.crt}' | base64 -d > bundle-ca.crt
```

### Must-Gather Dinâmico com JQ
```bash
# Must-gather com detecção automática de operators
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

## 🔍 Comandos com GREP e EGREP

### Filtros Complexos
```bash
# Pods que não estão Running ou Completed
oc get pods -A | egrep -v "Running|Completed"
```

```bash
# Ver apenas pods com erro
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

```bash
# Filtrar eventos importantes
oc describe pod <pod-name> | grep -A 10 "Events:"
```

### Análise de Configurações
```bash
# Ver limites de recursos
oc get all -o yaml | grep -A5 limits
```

```bash
# Buscar configurações de registry
oc get all -A | grep redhat-operator
```

```bash
# Ver configurações de métricas
oc get all --all-namespaces | grep metrics
```

```bash
# Buscar referências a portas
oc get all -o yaml | grep 5000
```

### Busca em AdminNetworkPolicy
```bash
# Ver regras de ingress
oc get adminnetworkpolicy deny-cross-namespace-communication -o yaml | grep -A 30 "ingress:" | head -40
```

### Análise de ArgoCD
```bash
# Ver source da aplicação
oc get application.argoproj.io workshop-vms-dev -n openshift-gitops -o yaml | grep -A 10 source
```

```bash
# Ver destination
oc get application.argoproj.io workshop-vms-dev -n openshift-gitops -o yaml | grep -A 5 destination
```

```bash
# Ver sync policy
oc get application workshop-gitops-vms-hml -n openshift-gitops -o yaml | grep -A 5 -B 5 sync
```

```bash
# Ver mensagens de erro
oc get application workshop-vms-dev -n openshift-gitops -o yaml | grep -A 20 -B 5 "message"
```

### Filtros em CatalogSource
```bash
# Ver status do catalog source
oc get catalogsource certified-operators -n openshift-marketplace -o yaml | grep -A 10 status:
```

```bash
# Filtrar catalogs da Red Hat
oc get catalogsource -n openshift-marketplace | grep redhat
```

---

## 🔄 Pipes Complexos

### Análise de API Requests
```bash
# Ver API requests com formatação
oc get apirequestcounts ingresses.v1beta1.extensions -o jsonpath='{range .status.currentHour..byUser[*]}{..byVerb[*].verb}{","}{.username}{","}{.userAgent}{"\n"}{end}' | sort -k 2 -t, -u | column -t -s, -NVERBS,USERNAME,USERAGENT
```

```bash
# Para networking ingresses
oc get apirequestcounts ingresses.v1beta1.networking.k8s.io -o jsonpath='{range .status.currentHour..byUser[*]}{..byVerb[*].verb}{","}{.username}{","}{.userAgent}{"\n"}{end}' | sort -k 2 -t, -u | column -t -s, -NVERBS,USERNAME,USERAGENT
```

```bash
# Para roles RBAC
oc get apirequestcounts roles.v1beta1.rbac.authorization.k8s.io -o jsonpath='{range .status.currentHour..byUser[*]}{..byVerb[*].verb}{","}{.username}{","}{.userAgent}{"\n"}{end}' | sort -k 2 -t, -u | column -t -s, -NVERBS,USERNAME,USERAGENT
```

### Análise de ClusterOperators com Tabela
```bash
# Criar tabela formatada de cluster operators
oc get clusteroperators -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .status.conditions[?(@.type=="Progressing")]}{.status}{"\t"}{end}{range .status.conditions[?(@.type=="Degraded")]}{.status}{"\t"}{.message}{"\n"}{end}{end}' | column -t -s $'\t'
```

### Exportar Applications ArgoCD
```bash
# Exportar applications sem metadados desnecessários
oc get application -A -o yaml | sed '/creationTimestamp\|resourceVersion\|uid/d'
```

```bash
# Exportar e salvar com timestamp
oc get application -A -o yaml | sed '/creationTimestamp\|resourceVersion\|uid/d' > /tmp/argocd-apps-$(date +'%d%m%y_%H%M%S').yaml
```

```bash
# Exportar sem status
oc get application -A -o yaml | sed '/status:/d'
```

### Verificações Condicionais
```bash
# Verificar se aplicação existe
oc get applications.argoproj.io -n openshift-gitops  || echo "No applications found"
```

```bash
# Verificar health status com fallback
oc get application workshop-gitops-vms-dev -n openshift-gitops -o jsonpath='{.status.health.status}'  || echo "Application not found"
```

```bash
# Ver erro condition com fallback
oc get application workshop-vms-prd -n openshift-gitops -o jsonpath='{.status.conditions[0].message}'  || echo "No error condition found"
```

---

## 🤖 Automação e Scripts

### Loop para Coletar Logs
```bash
# Coletar logs de todos os pods em um arquivo
for pod in $(oc get pods -o name); do
  echo "=== $pod ===" >> all-logs.txt
  oc logs $pod >> all-logs.txt 2>&1
done
```

```bash
# Coletar logs apenas de pods com erro
for pod in $(oc get pods --field-selector=status.phase!=Running -o name); do
  echo "=== $pod ===" >> error-logs.txt
  oc logs $pod --previous >> error-logs.txt 2>&1
done
```

### Verificação de ArgoCD Apps
```bash
# Loop para verificar múltiplas aplicações
for app in $(oc get applications.argoproj.io -n openshift-gitops --no-headers | awk '{print $1}'); do
  echo "Application: $app"
  oc get application $app -n openshift-gitops -o jsonpath='{.status.health.status}'
  echo ""
done
```

### Aprovar CSRs em Loop
```bash
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

### Verificação de Nodes
```bash
# Verificar status de todos os nodes
for node in $(oc get nodes -o name); do
  echo "=== $node ==="
  oc describe $node | grep -A 5 "Conditions:"
  echo ""
done
```

---

## 📈 Análise de Cluster Operators

### Status Completo
```bash
# Ver todos os operators e suas condições
oc get co -o json | jq -r '.items[] | "\(.metadata.name): Available=\(.status.conditions[] | select(.type=="Available").status), Progressing=\(.status.conditions[] | select(.type=="Progressing").status), Degraded=\(.status.conditions[] | select(.type=="Degraded").status)"'
```

```bash
# Operators com problemas detalhados
oc get co -o json | jq '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | {name: .metadata.name, message: (.status.conditions[] | select(.type=="Degraded").message)}'
```

```bash
# Ver versões dos operators
oc get co -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.versions[0].version}{"\n"}{end}' | column -t
```

### APIServices
```bash
# Ver apiservices com problemas
oc get apiservice | grep -v True
```

```bash
# Ver certificados de apiservice
oc get apiservice v1beta1.metrics.k8s.io -o jsonpath='{.spec.caBundle}' | base64 -d | openssl x509 -text
```

```bash
# Análise completa de apiservice
oc get apiservice v1.packages.operators.coreos.com -o jsonpath='{.spec.caBundle}' | base64 -d | openssl x509 -noout -text
```

---

## 🔐 Extração de Certificados

### Extrair e Analisar Certificados
```bash
# Extrair certificado de service
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

```bash
# Ver expiração do certificado
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -enddate
```

```bash
# Verificar certificado de apiservice
oc get apiservice v1beta1.metrics.k8s.io -o jsonpath='{.spec.caBundle}' | base64 -d | openssl x509 -text
```

```bash
# Extrair bundle CA do OAuth
oc get $(oc get secrets -n openshift-authentication -o name | grep oauth-openshift-token | tail -1) -n openshift-authentication -o jsonpath='{.data.ca\.crt}' | base64 -d > oauth-ca-bundle.crt
```

---

## 💡 Dicas e Truques

### Combinando Comandos
```bash
# Ver pods com mais uso de CPU
oc adm top pods --all-namespaces --no-headers | sort -k3 -nr | head -10
```

```bash
# Ver nodes com mais pods
oc get pods -A -o wide --no-headers | awk '{print $8}' | sort | uniq -c | sort -nr
```

```bash
# Contar recursos por namespace
oc get all -A --no-headers | awk '{print $1}' | sort | uniq -c
```

### Aliases Úteis para Scripts
```bash
# Adicionar ao ~/.bashrc
alias ocpods='oc get pods -A | egrep -v "Running|Completed"'
alias occo='oc get co | grep -v "True.*False.*False"'
alias occsrfix='oc get csr -o name | xargs oc adm certificate approve'
alias octop='oc adm top pods --all-namespaces --no-headers | sort -k3 -nr | head -10'
```

### Verificações Rápidas
```bash
# Health check completo do cluster
echo "=== Cluster Operators ===" && oc get co | grep -v "True.*False.*False" && \
echo "=== Problematic Pods ===" && oc get pods -A | egrep -v "Running|Completed" && \
echo "=== Pending CSRs ===" && oc get csr | grep Pending && \
echo "=== Non-Ready Nodes ===" && oc get nodes | grep -v "Ready"
```

---

## 📚 Recursos Adicionais

- **JQ Manual**: https://stedolan.github.io/jq/manual/
- **AWK Tutorial**: https://www.gnu.org/software/gawk/manual/
- **GREP Guide**: https://www.gnu.org/software/grep/manual/

---

## 📖 Navegação

- [← Voltar para Networking](22-networking.md)
- [→ Próximo: Field Selectors](24-field-selectors.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
