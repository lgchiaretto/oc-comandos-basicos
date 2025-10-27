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
```markdown
**Ação:** Exibir recurso "test-app" em formato JSON
**Exemplo:** `oc get pod <resource-name>app -o jsonpath='{.metadata.name}'`
```

```bash ignore-test
oc get pod test-app -o jsonpath='{.metadata.name}'
```

```markdown
**Ação:** Exibir recurso "test-app" em formato JSON
**Exemplo:** `oc get pod <resource-name>app -o jsonpath='{.metadata.name}{" "}{.status.phase}{"\n"}'`
```

```bash ignore-test
oc get pod test-app -o jsonpath='{.metadata.name}{" "}{.status.phase}{"\n"}'
```

```markdown
**Ação:** Exibir pods em formato JSON
```

```bash
oc get pods -o jsonpath='{.items[*].metadata.name}'
```

```markdown
**Ação:** Exibir pods em formato JSON
```

```bash
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'
```

```markdown
**Ação:** Exibir recurso "test-app" em formato JSON
**Exemplo:** `oc get pod <resource-name>app -o jsonpath='{.spec.containers[0].image}'`
```

```bash ignore-test
oc get pod test-app -o jsonpath='{.spec.containers[0].image}'
```

```markdown
**Ação:** Exibir recurso "test-app" em formato JSON
**Exemplo:** `oc get pod <resource-name>app -o jsonpath='{.spec.containers[*].name}'`
```

```bash ignore-test
oc get pod test-app -o jsonpath='{.spec.containers[*].name}'
```

### Filtros e Condições
```markdown
**Ação:** Exibir pods em formato JSON
```

```bash
oc get pods -o jsonpath='{.items[?(@.status.phase=="Running")].metadata.name}'
```

```markdown
**Ação:** Exibir pods em formato JSON
```

```bash
oc get pods -o jsonpath='{.items[?(@.status.containerStatuses[0].restartCount>0)].metadata.name}'
```

```markdown
**Ação:** Exibir nodes em formato JSON
```

```bash
oc get nodes -o jsonpath='{range .items[?(@.status.conditions[-1:].status=="True")]}{.metadata.name}{"\n"}{end}'
```

```markdown
**Ação:** Exibir nodes em formato JSON
```

```bash
oc get nodes -o jsonpath='{range .items[?(@.status.conditions[-1:].status!="True")]}{.metadata.name}{"\n"}{end}'
```

```markdown
**Ação:** Exibir persistent volume claim em formato JSON
```

```bash ignore-test
oc get pvc -o jsonpath='{.items[?(@.status.phase=="Bound")].metadata.name}'
```

### Exemplos Práticos
```markdown
**Ação:** Exibir pods em formato JSON
```

```bash ignore-test
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'
```

```markdown
**Ação:** Exibir pods em formato JSON
```

```bash ignore-test
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].image}{"\n"}{end}'
```

```markdown
**Ação:** Exibir nodes em formato JSON
```

```bash ignore-test
oc get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.node-role\.kubernetes\.io/worker}{"\n"}{end}'
```

```markdown
**Ação:** Exibir persistent volume em formato JSON
```

```bash ignore-test
oc get pv -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.claimRef.name}{"\n"}{end}'
```

```markdown
**Ação:** Exibir pods em formato JSON
```

```bash ignore-test
oc get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\tCPU:"}{.spec.containers[0].resources.requests.cpu}{"\tMEM:"}{.spec.containers[0].resources.requests.memory}{"\n"}{end}'
```

---

## Go-Template

### Sintaxe Básica
```markdown
**Ação:** Template simples
```

```bash
oc get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'
```

```markdown
**Ação:** Com formatação
```

```bash
oc get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\t"}}{{.status.phase}}{{"\n"}}{{end}}'
```

```markdown
**Ação:** Condicionais
```

```bash
oc get pods -o go-template='{{range .items}}{{if eq .status.phase "Running"}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}'
```

### Templates Complexos
```markdown
**Ação:** Template com if/else
```

```bash
oc get pods -o go-template='{{range .items}}{{.metadata.name}}: {{if .status.containerStatuses}}{{(index .status.containerStatuses 0).ready}}{{else}}N/A{{end}}{{"\n"}}{{end}}'
```

```markdown
**Ação:** Funções built-in
```

```bash
oc get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'
```

```markdown
**Ação:** Template com tabela
```

```bash
oc get pods -o go-template='NAME{{"\t"}}STATUS{{"\t"}}IP{{"\n"}}{{range .items}}{{.metadata.name}}{{"\t"}}{{.status.phase}}{{"\t"}}{{.status.podIP}}{{"\n"}}{{end}}'
```

### Template em Arquivo
```markdown
**Ação:** Criar template file
```

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

```markdown
**Ação:** Usar template
```

```bash ignore-test
oc get pods -o go-template-file=/tmp/pod-template.tmpl
```

---

## JQ - JSON Processor

### Instalação e Uso Básico
```bash
# Instalar jq (se não estiver instalado)
# sudo dnf install jq -y
```
```markdown
**Ação:** Exibir pods em formato JSON
```

```bash
oc get pods -o json | jq .
```

```markdown
**Ação:** Exibir pods em formato JSON
```

```bash
oc get pods -o json | jq '.'
```

```markdown
**Ação:** Exibir pods em formato JSON
```

```bash ignore-test
oc get pods -o json | jq '.items[].metadata.name'
```

```markdown
**Ação:** Exibir pods em formato JSON
```

```bash ignore-test
oc get pods -o json | jq '.items[] | select(.status.phase=="Running") | .metadata.name'
```

### Filtros Avançados
```markdown
**Ação:** Exibir pods em formato JSON
```

```bash ignore-test
oc get pods -o json | jq -r '.items[] | "\(.metadata.name) \(.status.phase)"'
```

```markdown
**Ação:** Exibir pods em formato JSON
```

```bash ignore-test
oc get pods -o json | jq '[.items[] | {name: .metadata.name, phase: .status.phase}]'
```

```markdown
**Ação:** Exibir pods em formato JSON
```

```bash
oc get pods -o json | jq '.items | length'
```

```markdown
**Ação:** Listar pods de todos os namespaces do cluster
```

```bash ignore-test
oc get pods -A -o json | jq -r 'group_by(.metadata.namespace) | .[] | "\(.[0].metadata.namespace): \(length) pods"'
```

```markdown
**Ação:** Exibir pods em formato JSON
```

```bash
oc get pods -o json | jq '.items | sort_by(.metadata.creationTimestamp)'
```

### Exemplos Práticos com JQ
```markdown
**Ação:** Listar pods de todos os namespaces do cluster
```

```bash ignore-test
oc get pods -A -o json | jq -r '.items[] | select(.status.phase != "Running" and .status.phase != "Succeeded") | "\(.metadata.namespace)/\(.metadata.name): \(.status.phase)"'
```

```markdown
**Ação:** Listar pods de todos os namespaces do cluster
```

```bash ignore-test
oc get pods -A -o json | jq -r '.items[] | "\(.status.containerStatuses[0].restartCount) \(.metadata.namespace)/\(.metadata.name)"' | sort -rn | head -10
```

```markdown
**Ação:** Exibir nodes em formato JSON
```

```bash ignore-test
oc get nodes -o json | jq -r '.items[] | "\(.metadata.name): \(.status.addresses[] | select(.type=="InternalIP") | .address)"'
```

```markdown
**Ação:** Listar persistent volume claim de todos os namespaces do cluster
```

```bash ignore-test
oc get pvc -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name): \(.spec.resources.requests.storage)"'
```

```markdown
**Ação:** Listar service de todos os namespaces do cluster
```

```bash ignore-test
oc get svc -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name): \(.spec.clusterIP)"'
```

```markdown
**Ação:** Exibir cluster operator em formato JSON
```

```bash ignore-test
oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name'
```

---

## Custom Columns

### Formato Custom-Columns
```markdown
**Ação:** Listar pods com colunas customizadas
```

```bash
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase
```

```markdown
**Ação:** Listar pods com colunas customizadas
```

```bash
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP,NODE:.spec.nodeName
```

```markdown
**Ação:** Listar pods com colunas customizadas
```

```bash
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase --no-headers
```

```markdown
**Ação:** Listar nodes com colunas customizadas
```

```bash ignore-test
oc get nodes -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[?(@.type==\"Ready\")].status,VERSION:.status.nodeInfo.kubeletVersion
```

```markdown
**Ação:** Listar persistent volume claim com colunas customizadas
```

```bash
oc get pvc -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,VOLUME:.spec.volumeName,CAPACITY:.spec.resources.requests.storage
```

```markdown
**Ação:** Listar service com colunas customizadas
```

```bash ignore-test
oc get svc -o custom-columns=NAME:.metadata.name,TYPE:.spec.type,CLUSTER-IP:.spec.clusterIP,PORT:.spec.ports[0].port
```

### Custom-Columns Complexas
```markdown
**Ação:** Listar deployment com colunas customizadas
```

```bash
oc get deploy -o custom-columns=NAME:.metadata.name,DESIRED:.spec.replicas,CURRENT:.status.replicas,READY:.status.readyReplicas,UP-TO-DATE:.status.updatedReplicas
```

```markdown
**Ação:** Listar pods com colunas customizadas
```

```bash ignore-test
oc get pods -o custom-columns=NAME:.metadata.name,CPU_REQ:.spec.containers[0].resources.requests.cpu,MEM_REQ:.spec.containers[0].resources.requests.memory,CPU_LIM:.spec.containers[0].resources.limits.cpu,MEM_LIM:.spec.containers[0].resources.limits.memory
```

```markdown
**Ação:** Em arquivo
```

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
```markdown
**Ação:** Listar pods com informações adicionais (node, IP, etc)
```

```bash
oc get pods -o wide
```

```markdown
**Ação:** Exibir recurso "test-app" em formato YAML
**Exemplo:** `oc get pod <resource-name>app -o yaml`
```

```bash ignore-test
oc get pod test-app -o yaml
```

```markdown
**Ação:** Exibir recurso "test-app" em formato JSON
**Exemplo:** `oc get pod <resource-name>app -o json`
```

```bash ignore-test
oc get pod test-app -o json
```

```markdown
**Ação:** Name only
```

```bash
oc get pods -o name
```

```markdown
**Ação:** Sem headers
```

```bash
oc get pods --no-headers
```

### Combinações Úteis
```markdown
**Ação:** Pods com AWK
```

```bash
oc get pods --no-headers | awk '{print $1}'
```

```markdown
**Ação:** Nodes com grep e awk
```

```bash
oc get nodes --no-headers | grep Ready | awk '{print $1}'
```

```markdown
**Ação:** Listar pods ordenados por campo específico
```

```bash
oc get pods --sort-by=.metadata.creationTimestamp
```

```markdown
**Ação:** Listar pods ordenados por campo específico
```

```bash
oc get pods --sort-by=.metadata.name
```

```markdown
**Ação:** Listar pods mostrando todas as labels associadas
```

```bash
oc get pods --show-labels
```

```markdown
**Ação:** Listar pods filtrados por label
```

```bash
oc get pods -l app=myapp
```

```markdown
**Ação:** Listar pods de todos os namespaces do cluster
```

```bash
oc get pods -A --sort-by=.metadata.namespace
```

### Aliases Úteis
```markdown
**Ação:** Adicionar ao ~/.bashrc
```

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

```markdown
**Ação:** Listar recurso com colunas customizadas
```

```bash
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
