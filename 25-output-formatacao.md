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
oc get pod <nome> -o jsonpath='{.metadata.name}'

# Múltiplos campos
oc get pod <nome> -o jsonpath='{.metadata.name}{" "}{.status.phase}{"\n"}'

# Array de pods
oc get pods -o jsonpath='{.items[*].metadata.name}'

# Com quebra de linha
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'

# Campo nested
oc get pod <nome> -o jsonpath='{.spec.containers[0].image}'

# Todos os containers
oc get pod <nome> -o jsonpath='{.spec.containers[*].name}'
```

### Filtros e Condições
```bash
# Pods em estado específico
oc get pods -o jsonpath='{.items[?(@.status.phase=="Running")].metadata.name}'

# Pods com restart > 0
oc get pods -o jsonpath='{.items[?(@.status.containerStatuses[0].restartCount>0)].metadata.name}'

# Nodes ready
oc get nodes -o jsonpath='{.items[?(@.status.conditions[?(@.type=="Ready")].status=="True")].metadata.name}'

# PVCs bound
oc get pvc -o jsonpath='{.items[?(@.status.phase=="Bound")].metadata.name}'
```

### Exemplos Práticos
```bash
# IPs de todos os pods
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'

# Imagens de todos os containers
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].image}{"\n"}{end}'

# Nodes e suas roles
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.node-role\.kubernetes\.io/worker}{"\n"}{end}'

# PVs e seus claims
oc get pv -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.claimRef.name}{"\n"}{end}'

# Ver requests de CPU/memória
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\tCPU:"}{.spec.containers[0].resources.requests.cpu}{"\tMEM:"}{.spec.containers[0].resources.requests.memory}{"\n"}{end}'
```

---

## 📝 Go-Template

### Sintaxe Básica
```bash
# Template simples
oc get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'

# Com formatação
oc get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\t"}}{{.status.phase}}{{"\n"}}{{end}}'

# Condicionais
oc get pods -o go-template='{{range .items}}{{if eq .status.phase "Running"}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}'
```

### Templates Complexos
```bash
# Template com if/else
oc get pods -o go-template='{{range .items}}{{.metadata.name}}: {{if .status.containerStatuses}}{{(index .status.containerStatuses 0).ready}}{{else}}N/A{{end}}{{"\n"}}{{end}}'

# Funções built-in
oc get pods -o go-template='{{range .items}}{{.metadata.name | upper}}{{"\n"}}{{end}}'

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

# Uso básico com oc
oc get pods -o json | jq .

# Pretty print
oc get pods -o json | jq '.'

# Extrair campo
oc get pods -o json | jq '.items[].metadata.name'

# Com filtros
oc get pods -o json | jq '.items[] | select(.status.phase=="Running") | .metadata.name'
```

### Filtros Avançados
```bash
# Múltiplos campos
oc get pods -o json | jq -r '.items[] | "\(.metadata.name) \(.status.phase)"'

# Array de objetos
oc get pods -o json | jq '[.items[] | {name: .metadata.name, phase: .status.phase}]'

# Contar
oc get pods -o json | jq '.items | length'

# Group by
oc get pods -A -o json | jq -r 'group_by(.metadata.namespace) | .[] | "\(.[0].metadata.namespace): \(length) pods"'

# Ordenar
oc get pods -o json | jq '.items | sort_by(.metadata.creationTimestamp)'
```

### Exemplos Práticos com JQ
```bash
# Pods não Running
oc get pods -A -o json | jq -r '.items[] | select(.status.phase != "Running" and .status.phase != "Succeeded") | "\(.metadata.namespace)/\(.metadata.name): \(.status.phase)"'

# Top pods por restarts
oc get pods -A -o json | jq -r '.items[] | "\(.status.containerStatuses[0].restartCount) \(.metadata.namespace)/\(.metadata.name)"' | sort -rn | head -10

# Nodes e seus IPs
oc get nodes -o json | jq -r '.items[] | "\(.metadata.name): \(.status.addresses[] | select(.type=="InternalIP") | .address)"'

# PVCs e tamanhos
oc get pvc -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name): \(.spec.resources.requests.storage)"'

# Services e seus ClusterIPs
oc get svc -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name): \(.spec.clusterIP)"'

# Cluster Operators degraded
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

---

## 📊 Custom Columns

### Formato Custom-Columns
```bash
# Sintaxe básica
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase

# Pods com mais info
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP,NODE:.spec.nodeName

# Sem headers
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase --no-headers

# Nodes
oc get nodes -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[?(@.type==\"Ready\")].status,VERSION:.status.nodeInfo.kubeletVersion

# PVCs
oc get pvc -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,VOLUME:.spec.volumeName,CAPACITY:.spec.resources.requests.storage

# Services
oc get svc -o custom-columns=NAME:.metadata.name,TYPE:.spec.type,CLUSTER-IP:.spec.clusterIP,PORT:.spec.ports[0].port
```

### Custom-Columns Complexas
```bash
# Deployments com replicas
oc get deploy -o custom-columns=NAME:.metadata.name,DESIRED:.spec.replicas,CURRENT:.status.replicas,READY:.status.readyReplicas,UP-TO-DATE:.status.updatedReplicas

# Pods com resources
oc get pods -o custom-columns=NAME:.metadata.name,CPU_REQ:.spec.containers[0].resources.requests.cpu,MEM_REQ:.spec.containers[0].resources.requests.memory,CPU_LIM:.spec.containers[0].resources.limits.cpu,MEM_LIM:.spec.containers[0].resources.limits.memory

# Em arquivo
cat > /tmp/custom-cols.txt << 'EOF'
NAME:.metadata.name
NAMESPACE:.metadata.namespace
STATUS:.status.phase
NODE:.spec.nodeName
IP:.status.podIP
AGE:.metadata.creationTimestamp
EOF

oc get pods -o custom-columns-file=/tmp/custom-cols.txt
```

---

## 🎨 Formatação de Saída

### Outputs Nativos
```bash
# Wide (mais colunas)
oc get pods -o wide

# YAML
oc get pod <nome> -o yaml

# JSON
oc get pod <nome> -o json

# Name only
oc get pods -o name

# Sem headers
oc get pods --no-headers
```

### Combinações Úteis
```bash
# Pods com AWK
oc get pods --no-headers | awk '{print $1}'

# Nodes com grep e awk
oc get nodes --no-headers | grep Ready | awk '{print $1}'

# Sort por idade
oc get pods --sort-by=.metadata.creationTimestamp

# Sort por nome
oc get pods --sort-by=.metadata.name

# Labels
oc get pods --show-labels

# Selector
oc get pods -l app=myapp

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
