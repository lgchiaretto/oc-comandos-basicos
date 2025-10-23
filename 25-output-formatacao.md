# 🎨 Output e Formatação

Este documento contém comandos para formatar e extrair informações específicas usando jsonpath, go-template, jq e outras ferramentas.

---

## 📋 Índice

1. [Jsonpath](#jsonpath)
2. [Go-Template](#go-template)
3. [JQ - JSON Processor](#jq---json-processor)
4. [Custom Columns](#custom-columns)
5. [Formatação de Saída](#formatação-de-saída)

---

## 🔍 Jsonpath

### Básico
```bash
# Extrair campo específico
# oc get pod <resource-name>app -o jsonpath='{.metadata.name}'
oc get pod test-app -o jsonpath='{.metadata.name}'
```

```bash
# Múltiplos campos
# oc get pod <resource-name>app -o jsonpath='{.metadata.name}{" "}{.status.phase}{"\n"}'
oc get pod test-app -o jsonpath='{.metadata.name}{" "}{.status.phase}{"\n"}'
```

```bash ignore-test
# Array de pods
oc get pods -o jsonpath='{.items[*].metadata.name}'
```

```bash ignore-test
# Com quebra de linha
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'
```

```bash ignore-test
# Campo nested
# oc get pod <resource-name>app -o jsonpath='{.spec.containers[0].image}'
oc get pod test-app -o jsonpath='{.spec.containers[0].image}'
```

```bash ignore-test
# Todos os containers
# oc get pod <resource-name>app -o jsonpath='{.spec.containers[*].name}'
oc get pod test-app -o jsonpath='{.spec.containers[*].name}'
```

### Filtros e Condições
```bash ignore-test
# Pods em estado específico
oc get pods -o jsonpath='{.items[?(@.status.phase=="Running")].metadata.name}'
```

```bash ignore-test
# Pods com restart > 0
oc get pods -o jsonpath='{.items[?(@.status.containerStatuses[0].restartCount>0)].metadata.name}'
```

```bash ignore-test
# Nodes ready
oc get nodes -o jsonpath='{.items[?(@.status.conditions[?(@.type=="Ready")].status=="True")].metadata.name}'
```

```bash ignore-test
# PVCs bound
oc get pvc -o jsonpath='{.items[?(@.status.phase=="Bound")].metadata.name}'
```

### Exemplos Práticos
```bash ignore-test
# IPs de todos os pods
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'
```

```bash ignore-test
# Imagens de todos os containers
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].image}{"\n"}{end}'
```

```bash ignore-test
# Nodes e suas roles
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.node-role\.kubernetes\.io/worker}{"\n"}{end}'
```

```bash ignore-test
# PVs e seus claims
oc get pv -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.claimRef.name}{"\n"}{end}'
```

```bash ignore-test
# Ver requests de CPU/memória
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\tCPU:"}{.spec.containers[0].resources.requests.cpu}{"\tMEM:"}{.spec.containers[0].resources.requests.memory}{"\n"}{end}'
```

---

## 📝 Go-Template

### Sintaxe Básica
```bash
# Template simples
oc get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'
```

```bash
# Com formatação
oc get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\t"}}{{.status.phase}}{{"\n"}}{{end}}'
```

```bash
# Condicionais
oc get pods -o go-template='{{range .items}}{{if eq .status.phase "Running"}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}'
```

### Templates Complexos
```bash
# Template com if/else
oc get pods -o go-template='{{range .items}}{{.metadata.name}}: {{if .status.containerStatuses}}{{(index .status.containerStatuses 0).ready}}{{else}}N/A{{end}}{{"\n"}}{{end}}'
```

```bash
# Funções built-in
oc get pods -o go-template='{{range .items}}{{.metadata.name | upper}}{{"\n"}}{{end}}'
```

```bash
# Template com tabela
oc get pods -o go-template='NAME{{"\t"}}STATUS{{"\t"}}IP{{"\n"}}{{range .items}}{{.metadata.name}}{{"\t"}}{{.status.phase}}{{"\t"}}{{.status.podIP}}{{"\n"}}{{end}}'
```

### Template em Arquivo
```bash
# Criar template file
cat > /tmp/pod-template.tmpl << 'EOF'
{{range .items}}
Pod: {{.metadata.name}}
  Namespace: {{.metadata.namespace}}
  Status: {{.status.phase}}
  Node: {{.spec.nodeName}}
  IP: {{.status.podIP}}
  Containers:
  {{range .spec.containers}}
    - {{.name}}: {{.image}}
  {{end}}
{{end}}
EOF
```

```bash
# Usar template
oc get pods -o go-template-file=/tmp/pod-template.tmpl
```

---

## 🔧 JQ - JSON Processor

### Instalação e Uso Básico
```bash
# Instalar jq (se não estiver instalado)
# sudo yum install jq -y  # RHEL/CentOS
# sudo apt install jq -y  # Ubuntu/Debian
```

```bash
# Uso básico com oc
oc get pods -o json | jq .
```

```bash
# Pretty print
oc get pods -o json | jq '.'
```

```bash ignore-test
# Extrair campo
oc get pods -o json | jq '.items[].metadata.name'
```

```bash ignore-test
# Com filtros
oc get pods -o json | jq '.items[] | select(.status.phase=="Running") | .metadata.name'
```

### Filtros Avançados
```bash ignore-test
# Múltiplos campos
oc get pods -o json | jq -r '.items[] | "\(.metadata.name) \(.status.phase)"'
```

```bash ignore-test
# Array de objetos
oc get pods -o json | jq '[.items[] | {name: .metadata.name, phase: .status.phase}]'
```

```bash
# Contar
oc get pods -o json | jq '.items | length'
```

```bash ignore-test
# Group by
oc get pods -A -o json | jq -r 'group_by(.metadata.namespace) | .[] | "\(.[0].metadata.namespace): \(length) pods"'
```

```bash
# Ordenar
oc get pods -o json | jq '.items | sort_by(.metadata.creationTimestamp)'
```

### Exemplos Práticos com JQ
```bash ignore-test
# Pods não Running
oc get pods -A -o json | jq -r '.items[] | select(.status.phase != "Running" and .status.phase != "Succeeded") | "\(.metadata.namespace)/\(.metadata.name): \(.status.phase)"'
```

```bash ignore-test
# Top pods por restarts
oc get pods -A -o json | jq -r '.items[] | "\(.status.containerStatuses[0].restartCount) \(.metadata.namespace)/\(.metadata.name)"' | sort -rn | head -10
```

```bash ignore-test
# Nodes e seus IPs
oc get nodes -o json | jq -r '.items[] | "\(.metadata.name): \(.status.addresses[] | select(.type=="InternalIP") | .address)"'
```

```bash ignore-test
# PVCs e tamanhos
oc get pvc -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name): \(.spec.resources.requests.storage)"'
```

```bash ignore-test
# Services e seus ClusterIPs
oc get svc -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name): \(.spec.clusterIP)"'
```

```bash ignore-test
# Cluster Operators degraded
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

---

## 📊 Custom Columns

### Formato Custom-Columns
```bash
# Sintaxe básica
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase
```

```bash
# Pods com mais info
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP,NODE:.spec.nodeName
```

```bash
# Sem headers
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase --no-headers
```

```bash ignore-test
# Nodes
oc get nodes -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[?(@.type==\"Ready\")].status,VERSION:.status.nodeInfo.kubeletVersion
```

```bash
# PVCs
oc get pvc -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,VOLUME:.spec.volumeName,CAPACITY:.spec.resources.requests.storage
```

```bash ignore-test
# Services
oc get svc -o custom-columns=NAME:.metadata.name,TYPE:.spec.type,CLUSTER-IP:.spec.clusterIP,PORT:.spec.ports[0].port
```

### Custom-Columns Complexas
```bash
# Deployments com replicas
oc get deploy -o custom-columns=NAME:.metadata.name,DESIRED:.spec.replicas,CURRENT:.status.replicas,READY:.status.readyReplicas,UP-TO-DATE:.status.updatedReplicas
```

```bash ignore-test
# Pods com resources
oc get pods -o custom-columns=NAME:.metadata.name,CPU_REQ:.spec.containers[0].resources.requests.cpu,MEM_REQ:.spec.containers[0].resources.requests.memory,CPU_LIM:.spec.containers[0].resources.limits.cpu,MEM_LIM:.spec.containers[0].resources.limits.memory
```

```bash
# Em arquivo
cat > /tmp/custom-cols.txt << 'EOF'
NAME:.metadata.name
NAMESPACE:.metadata.namespace
STATUS:.status.phase
NODE:.spec.nodeName
IP:.status.podIP
AGE:.metadata.creationTimestamp
EOF
```

```bash
oc get pods -o custom-columns-file=/tmp/custom-cols.txt
```

---

## 🎨 Formatação de Saída

### Outputs Nativos
```bash
# Wide (mais colunas)
oc get pods -o wide
```

```bash
# YAML
# oc get pod <resource-name>app -o yaml
oc get pod test-app -o yaml
```

```bash
# JSON
# oc get pod <resource-name>app -o json
oc get pod test-app -o json
```

```bash
# Name only
oc get pods -o name
```

```bash
# Sem headers
oc get pods --no-headers
```

### Combinações Úteis
```bash
# Pods com AWK
oc get pods --no-headers | awk '{print $1}'
```

```bash
# Nodes com grep e awk
oc get nodes --no-headers | grep Ready | awk '{print $1}'
```

```bash
# Sort por idade
oc get pods --sort-by=.metadata.creationTimestamp
```

```bash
# Sort por nome
oc get pods --sort-by=.metadata.name
```

```bash
# Labels
oc get pods --show-labels
```

```bash
# Selector
oc get pods -l app=myapp
```

```bash
# All namespaces com sorting
oc get pods -A --sort-by=.metadata.namespace
```

### Aliases Úteis
```bash
# Adicionar ao ~/.bashrc
alias okp='oc get pods'
alias okpw='oc get pods -o wide'
alias okpa='oc get pods -A'
alias okn='oc get nodes'
alias okd='oc get deploy'
alias oks='oc get svc'
alias okpj='oc get pods -o json'
alias okpy='oc get pods -o yaml'
```

```bash
# Custom output format
alias okpf='oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP,NODE:.spec.nodeName'
```

---

## 📖 Navegação

- [← Anterior: Etcd e Backup](22-etcd-backup.md)
- [→ Próximo: Templates e Manifests](26-templates-manifests.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
