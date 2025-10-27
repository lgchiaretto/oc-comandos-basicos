# Output e Formatação

Este documento contém comandos para formatar e extrair informações específicas usando jsonpath, go-template, jq e outras ferramentas.

---

## Índice

1. [Índice](#índice)
2. [Jsonpath](#jsonpath)
3. [Go-Template](#go-template)
4. [jq - JSON Processor](#jq-json-processor)
5. [Custom Columns](#custom-columns)
6. [Formatação de Saída](#formatação-de-saída)
7. [Documentação Oficial](#documentação-oficial)
8. [Navegação](#navegação)
---

## Jsonpath

### Básico
**Exibir recurso "test-app" em formato JSON**


```bash ignore-test
oc get pod test-app -o jsonpath='{.metadata.name}'
```

**Exibir recurso "test-app" em formato JSON**


```bash ignore-test
oc get pod test-app -o jsonpath='{.metadata.name}{" "}{.status.phase}{"\n"}'
```

**Exibir pods em formato JSON**

```bash
oc get pods -o jsonpath='{.items[*].metadata.name}'
```

**Exibir pods em formato JSON**

```bash
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'
```

**Exibir recurso "test-app" em formato JSON**


```bash ignore-test
oc get pod test-app -o jsonpath='{.spec.containers[0].image}'
```

**Exibir recurso "test-app" em formato JSON**


```bash ignore-test
oc get pod test-app -o jsonpath='{.spec.containers[*].name}'
```

### Filtros e Condições
**Exibir pods em formato JSON**

```bash
oc get pods -o jsonpath='{.items[?(@.status.phase=="Running")].metadata.name}'
```

**Exibir pods em formato JSON**

```bash
oc get pods -o jsonpath='{.items[?(@.status.containerStatuses[0].restartCount>0)].metadata.name}'
```

**Exibir nodes em formato JSON**

```bash
oc get nodes -o jsonpath='{range .items[?(@.status.conditions[-1:].status=="True")]}{.metadata.name}{"\n"}{end}'
```

**Exibir nodes em formato JSON**

```bash
oc get nodes -o jsonpath='{range .items[?(@.status.conditions[-1:].status!="True")]}{.metadata.name}{"\n"}{end}'
```

**Exibir persistent volume claim em formato JSON**

```bash ignore-test
oc get pvc -o jsonpath='{.items[?(@.status.phase=="Bound")].metadata.name}'
```

### Exemplos Práticos
**Exibir pods em formato JSON**

```bash ignore-test
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'
```

**Exibir pods em formato JSON**

```bash ignore-test
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].image}{"\n"}{end}'
```

**Exibir nodes em formato JSON**

```bash ignore-test
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.node-role\.kubernetes\.io/worker}{"\n"}{end}'
```

**Exibir persistent volume em formato JSON**

```bash ignore-test
oc get pv -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.claimRef.name}{"\n"}{end}'
```

**Exibir pods em formato JSON**

```bash ignore-test
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\tCPU:"}{.spec.containers[0].resources.requests.cpu}{"\tMEM:"}{.spec.containers[0].resources.requests.memory}{"\n"}{end}'
```

---

## Go-Template

### Sintaxe Básica
**Template simples**

```bash
oc get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'
```

**Com formatação**

```bash
oc get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\t"}}{{.status.phase}}{{"\n"}}{{end}}'
```

**Condicionais**

```bash
oc get pods -o go-template='{{range .items}}{{if eq .status.phase "Running"}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}'
```

### Templates Complexos
**Template com if/else**

```bash
oc get pods -o go-template='{{range .items}}{{.metadata.name}}: {{if .status.containerStatuses}}{{(index .status.containerStatuses 0).ready}}{{else}}N/A{{end}}{{"\n"}}{{end}}'
```

**Funções built-in**

```bash
oc get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'
```

**Template com tabela**

```bash
oc get pods -o go-template='NAME{{"\t"}}STATUS{{"\t"}}IP{{"\n"}}{{range .items}}{{.metadata.name}}{{"\t"}}{{.status.phase}}{{"\t"}}{{.status.podIP}}{{"\n"}}{{end}}'
```

### Template em Arquivo
**Criar template file**

```bash
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

**Usar template**

```bash ignore-test
oc get pods -o go-template-file=/tmp/pod-template.tmpl
```

---

## jq - JSON Processor

### Instalação e Uso Básico
```bash
# Instalar jq (se não estiver instalado)
# sudo dnf install jq -y
```
**Exibir pods em formato JSON**

```bash
oc get pods -o json | jq .
```

**Exibir pods em formato JSON**

```bash
oc get pods -o json | jq '.'
```

**Exibir pods em formato JSON**

```bash ignore-test
oc get pods -o json | jq '.items[].metadata.name'
```

**Exibir pods em formato JSON**

```bash ignore-test
oc get pods -o json | jq '.items[] | select(.status.phase=="Running") | .metadata.name'
```

### Filtros Avançados
**Exibir pods em formato JSON**

```bash ignore-test
oc get pods -o json | jq -r '.items[] | "\(.metadata.name) \(.status.phase)"'
```

**Exibir pods em formato JSON**

```bash ignore-test
oc get pods -o json | jq '[.items[] | {name: .metadata.name, phase: .status.phase}]'
```

**Exibir pods em formato JSON**

```bash
oc get pods -o json | jq '.items | length'
```

**Listar pods de todos os namespaces do cluster**

```bash ignore-test
oc get pods -A -o json | jq -r 'group_by(.metadata.namespace) | .[] | "\(.[0].metadata.namespace): \(length) pods"'
```

**Exibir pods em formato JSON**

```bash
oc get pods -o json | jq '.items | sort_by(.metadata.creationTimestamp)'
```

### Exemplos Práticos com jq
**Listar pods de todos os namespaces do cluster**

```bash ignore-test
oc get pods -A -o json | jq -r '.items[] | select(.status.phase != "Running" and .status.phase != "Succeeded") | "\(.metadata.namespace)/\(.metadata.name): \(.status.phase)"'
```

**Listar pods de todos os namespaces do cluster**

```bash ignore-test
oc get pods -A -o json | jq -r '.items[] | "\(.status.containerStatuses[0].restartCount) \(.metadata.namespace)/\(.metadata.name)"' | sort -rn | head -10
```

**Exibir nodes em formato JSON**

```bash ignore-test
oc get nodes -o json | jq -r '.items[] | "\(.metadata.name): \(.status.addresses[] | select(.type=="InternalIP") | .address)"'
```

**Listar persistent volume claim de todos os namespaces do cluster**

```bash ignore-test
oc get pvc -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name): \(.spec.resources.requests.storage)"'
```

**Listar service de todos os namespaces do cluster**

```bash ignore-test
oc get svc -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name): \(.spec.clusterIP)"'
```

**Exibir cluster operator em formato JSON**

```bash ignore-test
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

---

## Custom Columns

### Formato Custom-Columns
**Listar pods com colunas customizadas**

```bash
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase
```

**Listar pods com colunas customizadas**

```bash
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP,NODE:.spec.nodeName
```

**Listar pods com colunas customizadas**

```bash
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase --no-headers
```

**Listar nodes com colunas customizadas**

```bash ignore-test
oc get nodes -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[?(@.type==\"Ready\")].status,VERSION:.status.nodeInfo.kubeletVersion
```

**Listar persistent volume claim com colunas customizadas**

```bash
oc get pvc -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,VOLUME:.spec.volumeName,CAPACITY:.spec.resources.requests.storage
```

**Listar service com colunas customizadas**

```bash ignore-test
oc get svc -o custom-columns=NAME:.metadata.name,TYPE:.spec.type,CLUSTER-IP:.spec.clusterIP,PORT:.spec.ports[0].port
```

### Custom-Columns Complexas
**Listar deployment com colunas customizadas**

```bash
oc get deploy -o custom-columns=NAME:.metadata.name,DESIRED:.spec.replicas,CURRENT:.status.replicas,READY:.status.readyReplicas,UP-TO-DATE:.status.updatedReplicas
```

**Listar pods com colunas customizadas**

```bash ignore-test
oc get pods -o custom-columns=NAME:.metadata.name,CPU_REQ:.spec.containers[0].resources.requests.cpu,MEM_REQ:.spec.containers[0].resources.requests.memory,CPU_LIM:.spec.containers[0].resources.limits.cpu,MEM_LIM:.spec.containers[0].resources.limits.memory
```

**Em arquivo**

```bash
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
**Listar pods com informações adicionais (node, IP, etc)**

```bash
oc get pods -o wide
```

**Exibir recurso "test-app" em formato YAML**


```bash ignore-test
oc get pod test-app -o yaml
```

**Exibir recurso "test-app" em formato JSON**


```bash ignore-test
oc get pod test-app -o json
```

**Name only**

```bash
oc get pods -o name
```

**Sem headers**

```bash
oc get pods --no-headers
```

### Combinações Úteis
**Pods com AWK**

```bash
oc get pods --no-headers | awk '{print $1}'
```

**Nodes com grep e awk**

```bash
oc get nodes --no-headers | grep Ready | awk '{print $1}'
```

**Listar pods ordenados por campo específico**

```bash
oc get pods --sort-by=.metadata.creationTimestamp
```

**Listar pods ordenados por campo específico**

```bash
oc get pods --sort-by=.metadata.name
```

**Listar pods mostrando todas as labels associadas**

```bash
oc get pods --show-labels
```

**Listar pods filtrados por label**

```bash
oc get pods -l app=myapp
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A --sort-by=.metadata.namespace
```

### Aliases Úteis
**Adicionar ao ~/.bashrc**

```bash
alias okp='oc get pods'
alias okpw='oc get pods -o wide'
alias okpa='oc get pods -A'
alias okn='oc get nodes'
alias okd='oc get deploy'
alias oks='oc get svc'
alias okpj='oc get pods -o json'
alias okpy='oc get pods -o yaml'
```

**Listar recurso com colunas customizadas**

```bash
alias okpf='oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP,NODE:.spec.nodeName'
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/openshift-cli-oc">CLI Tools - OpenShift CLI (oc)</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools">CLI Tools - Usage of oc and kubectl</a>
---


## Navegação

- [← Anterior: Etcd e Backup](22-etcd-backup.md)
- [→ Próximo: Templates e Manifests](26-templates-manifests.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
