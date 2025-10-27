# Output e Formatação

Este documento contém comandos para formatar e extrair informações específicas usando jsonpath, go-template, jq e outras ferramentas.

---

## Índice

1. [Índice](#índice)
2. [Jsonpath](#jsonpath)
3. [Go-Template](#go-template)
4. [JQ - JSON Processor](#jq-json-processor)
5. [Custom Columns](#custom-columns)
6. [Formatação de Saída](#formatação-de-saída)
7. [Documentação Oficial](#documentação-oficial)
8. [Navegação](#navegação)
---

## Jsonpath

### Básico
```bash ignore-test
# Exibir recurso "test-app" em formato JSON
# oc get pod <resource-name>app -o jsonpath='{.metadata.name}'
oc get pod test-app -o jsonpath='{.metadata.name}'
```

```bash ignore-test
# Exibir recurso "test-app" em formato JSON
# oc get pod <resource-name>app -o jsonpath='{.metadata.name}{" "}{.status.phase}{"\n"}'
oc get pod test-app -o jsonpath='{.metadata.name}{" "}{.status.phase}{"\n"}'
```

```bash
# Exibir pods em formato JSON
oc get pods -o jsonpath='{.items[*].metadata.name}'
```

```bash
# Exibir pods em formato JSON
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'
```

```bash ignore-test
# Exibir recurso "test-app" em formato JSON
# oc get pod <resource-name>app -o jsonpath='{.spec.containers[0].image}'
oc get pod test-app -o jsonpath='{.spec.containers[0].image}'
```

```bash ignore-test
# Exibir recurso "test-app" em formato JSON
# oc get pod <resource-name>app -o jsonpath='{.spec.containers[*].name}'
oc get pod test-app -o jsonpath='{.spec.containers[*].name}'
```

### Filtros e Condições
```bash
# Exibir pods em formato JSON
oc get pods -o jsonpath='{.items[?(@.status.phase=="Running")].metadata.name}'
```

```bash
# Exibir pods em formato JSON
oc get pods -o jsonpath='{.items[?(@.status.containerStatuses[0].restartCount>0)].metadata.name}'
```

```bash
# Exibir nodes em formato JSON
oc get nodes -o jsonpath='{range .items[?(@.status.conditions[-1:].status=="True")]}{.metadata.name}{"\n"}{end}'
```

```bash
# Exibir nodes em formato JSON
oc get nodes -o jsonpath='{range .items[?(@.status.conditions[-1:].status!="True")]}{.metadata.name}{"\n"}{end}'
```

```bash ignore-test
# Exibir persistent volume claim em formato JSON
oc get pvc -o jsonpath='{.items[?(@.status.phase=="Bound")].metadata.name}'
```

### Exemplos Práticos
```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'
```

```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].image}{"\n"}{end}'
```

```bash ignore-test
# Exibir nodes em formato JSON
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.node-role\.kubernetes\.io/worker}{"\n"}{end}'
```

```bash ignore-test
# Exibir persistent volume em formato JSON
oc get pv -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.claimRef.name}{"\n"}{end}'
```

```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\tCPU:"}{.spec.containers[0].resources.requests.cpu}{"\tMEM:"}{.spec.containers[0].resources.requests.memory}{"\n"}{end}'
```

---

## Go-Template

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
oc get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'
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

```bash ignore-test
# Usar template
oc get pods -o go-template-file=/tmp/pod-template.tmpl
```

---

## JQ - JSON Processor

### Instalação e Uso Básico
```bash
# Instalar jq (se não estiver instalado)
# sudo dnf install jq -y
```
```bash
# Exibir pods em formato JSON
oc get pods -o json | jq .
```

```bash
# Exibir pods em formato JSON
oc get pods -o json | jq '.'
```

```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o json | jq '.items[].metadata.name'
```

```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o json | jq '.items[] | select(.status.phase=="Running") | .metadata.name'
```

### Filtros Avançados
```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o json | jq -r '.items[] | "\(.metadata.name) \(.status.phase)"'
```

```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o json | jq '[.items[] | {name: .metadata.name, phase: .status.phase}]'
```

```bash
# Exibir pods em formato JSON
oc get pods -o json | jq '.items | length'
```

```bash ignore-test
# Listar pods de todos os namespaces do cluster
oc get pods -A -o json | jq -r 'group_by(.metadata.namespace) | .[] | "\(.[0].metadata.namespace): \(length) pods"'
```

```bash
# Exibir pods em formato JSON
oc get pods -o json | jq '.items | sort_by(.metadata.creationTimestamp)'
```

### Exemplos Práticos com JQ
```bash ignore-test
# Listar pods de todos os namespaces do cluster
oc get pods -A -o json | jq -r '.items[] | select(.status.phase != "Running" and .status.phase != "Succeeded") | "\(.metadata.namespace)/\(.metadata.name): \(.status.phase)"'
```

```bash ignore-test
# Listar pods de todos os namespaces do cluster
oc get pods -A -o json | jq -r '.items[] | "\(.status.containerStatuses[0].restartCount) \(.metadata.namespace)/\(.metadata.name)"' | sort -rn | head -10
```

```bash ignore-test
# Exibir nodes em formato JSON
oc get nodes -o json | jq -r '.items[] | "\(.metadata.name): \(.status.addresses[] | select(.type=="InternalIP") | .address)"'
```

```bash ignore-test
# Listar persistent volume claim de todos os namespaces do cluster
oc get pvc -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name): \(.spec.resources.requests.storage)"'
```

```bash ignore-test
# Listar service de todos os namespaces do cluster
oc get svc -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name): \(.spec.clusterIP)"'
```

```bash ignore-test
# Exibir cluster operator em formato JSON
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

---

## Custom Columns

### Formato Custom-Columns
```bash
# Listar pods com colunas customizadas
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase
```

```bash
# Listar pods com colunas customizadas
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP,NODE:.spec.nodeName
```

```bash
# Listar pods com colunas customizadas
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase --no-headers
```

```bash ignore-test
# Listar nodes com colunas customizadas
oc get nodes -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[?(@.type==\"Ready\")].status,VERSION:.status.nodeInfo.kubeletVersion
```

```bash
# Listar persistent volume claim com colunas customizadas
oc get pvc -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,VOLUME:.spec.volumeName,CAPACITY:.spec.resources.requests.storage
```

```bash ignore-test
# Listar service com colunas customizadas
oc get svc -o custom-columns=NAME:.metadata.name,TYPE:.spec.type,CLUSTER-IP:.spec.clusterIP,PORT:.spec.ports[0].port
```

### Custom-Columns Complexas
```bash
# Listar deployment com colunas customizadas
oc get deploy -o custom-columns=NAME:.metadata.name,DESIRED:.spec.replicas,CURRENT:.status.replicas,READY:.status.readyReplicas,UP-TO-DATE:.status.updatedReplicas
```

```bash ignore-test
# Listar pods com colunas customizadas
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

```bash ignore-test
oc get pods -o custom-columns-file=/tmp/custom-cols.txt
```

---

## Formatação de Saída

### Outputs Nativos
```bash
# Listar pods com informações adicionais (node, IP, etc)
oc get pods -o wide
```

```bash ignore-test
# Exibir recurso "test-app" em formato YAML
# oc get pod <resource-name>app -o yaml
oc get pod test-app -o yaml
```

```bash ignore-test
# Exibir recurso "test-app" em formato JSON
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
# Listar pods ordenados por campo específico
oc get pods --sort-by=.metadata.creationTimestamp
```

```bash
# Listar pods ordenados por campo específico
oc get pods --sort-by=.metadata.name
```

```bash
# Listar pods mostrando todas as labels associadas
oc get pods --show-labels
```

```bash
# Listar pods filtrados por label
oc get pods -l app=myapp
```

```bash
# Listar pods de todos os namespaces do cluster
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
# Listar recurso com colunas customizadas
alias okpf='oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP,NODE:.spec.nodeName'
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/openshift-cli-oc">CLI Tools - OpenShift CLI (oc)</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools">CLI Tools - Usage of oc and kubectl</a>
---

---

## Navegação

- [← Anterior: Etcd e Backup](22-etcd-backup.md)
- [→ Próximo: Templates e Manifests](26-templates-manifests.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
