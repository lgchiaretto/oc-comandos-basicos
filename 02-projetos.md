# 📁 Gerenciamento de Projetos

Este documento contém comandos para criar, listar e gerenciar projetos (namespaces) no OpenShift.

---

## 📋 Índice

1. [Conceitos](#conceitos)
2. [Criação e Listagem](#criação-e-listagem)
3. [Gerenciamento](#gerenciamento)
4. [Node Selectors](#node-selectors)
5. [Templates de Projeto](#templates-de-projeto)

---

## 💡 Conceitos

### O que é um Projeto?
Projetos no OpenShift são similares a namespaces do Kubernetes, mas com funcionalidades adicionais:
- Isolamento de recursos
- Quotas e limites
- RBAC (controle de acesso)
- Network policies

---

## 🆕 Criação e Listagem

### Listar Projetos
```bash
# Listar todos os projetos
oc projects

# Listar projetos (formato detalhado)
oc get projects

# Listar com mais informações
oc get projects -o wide

# Ver projeto atual
oc project

# Listar com labels
oc get projects --show-labels
```

### Criar Projetos
```bash
# Criar novo projeto
oc new-project <nome-do-projeto>

# Criar projeto com descrição
oc new-project <nome-do-projeto> \
  --description="Minha descrição" \
  --display-name="Nome de Exibição"

# Exemplo completo
oc new-project producao \
  --description="Ambiente de produção" \
  --display-name="Produção"
```

### Trocar entre Projetos
```bash
# Trocar para outro projeto
oc project <nome-do-projeto>

# Exemplo
oc project development

# Verificar projeto atual
oc project
```

---

## 🔧 Gerenciamento

### Descrever e Inspecionar
```bash
# Descrever um projeto
oc describe project <nome-do-projeto>

# Ver em YAML
oc get project <nome-do-projeto> -o yaml

# Ver em JSON
oc get project <nome-do-projeto> -o json

# Exportar definição do projeto
oc get project <nome-do-projeto> -o yaml > projeto.yaml
```

### Editar Projetos
```bash
# Editar projeto
oc edit project <nome-do-projeto>

# Adicionar label
oc label project <nome-do-projeto> env=production

# Adicionar annotation
oc annotate project <nome-do-projeto> description="Meu projeto"

# Remover label
oc label project <nome-do-projeto> env-

# Patch de projeto
oc patch project <nome-do-projeto> -p '{"metadata":{"labels":{"tier":"frontend"}}}'
```

### Deletar Projetos
```bash
# Deletar um projeto
oc delete project <nome-do-projeto>

# Deletar com confirmação
oc delete project <nome-do-projeto> --wait=true

# Deletar múltiplos projetos
oc delete project projeto1 projeto2 projeto3

# CUIDADO: Isso deleta TODOS os recursos do projeto!
```

---

## 🎯 Node Selectors

### Criar Projeto com Node Selector (requer permissões admin)
```bash
# Criar projeto com node selector para ambiente
oc adm new-project <nome> --node-selector='env=prd'

# Criar projeto sem node selector (permite qualquer node)
oc adm new-project <nome> --node-selector=""

# Criar projeto com node selector específico por hostname
oc adm new-project <nome> \
  --node-selector="kubernetes.io/hostname=<hostname>"

# Exemplo prático
oc adm new-project producao --node-selector='env=production'
```

### Modificar Node Selector Existente
```bash
# Adicionar node selector a projeto existente
oc patch namespace <nome-do-projeto> -p \
  '{"metadata":{"annotations":{"openshift.io/node-selector":"env=prod"}}}'

# Remover node selector
oc patch namespace <nome-do-projeto> -p \
  '{"metadata":{"annotations":{"openshift.io/node-selector":""}}}'
```

---

## 📄 Templates de Projeto

### Criar Template de Projeto Customizado
```bash
# Gerar template padrão
oc adm create-bootstrap-project-template -o yaml > template.yaml

# Editar template
vim template.yaml

# Aplicar template customizado
oc create -f template.yaml -n openshift-config

# Configurar cluster para usar template
oc edit project.config.openshift.io/cluster
# Adicionar:
# spec:
#   projectRequestTemplate:
#     name: project-request
```

### Template com Quotas e Limites
```yaml
# Exemplo de template com quota
apiVersion: template.openshift.io/v1
kind: Template
metadata:
  name: project-request
objects:
- apiVersion: v1
  kind: Project
  metadata:
    name: ${PROJECT_NAME}
    annotations:
      openshift.io/description: ${PROJECT_DESCRIPTION}
- apiVersion: v1
  kind: ResourceQuota
  metadata:
    name: ${PROJECT_NAME}-quota
  spec:
    hard:
      requests.cpu: "10"
      requests.memory: 20Gi
      pods: "10"
parameters:
- name: PROJECT_NAME
- name: PROJECT_DESCRIPTION
```

---

## 📊 Informações e Status

### Ver Recursos do Projeto
```bash
# Listar todos os recursos
oc get all

# Listar recursos específicos
oc get pods,svc,routes

# Ver quotas do projeto
oc get quota
oc describe quota

# Ver limit ranges
oc get limitrange
oc describe limitrange

# Ver network policies
oc get networkpolicy
```

### Status do Projeto
```bash
# Status geral
oc status

# Status detalhado
oc status -v

# Status sugerindo ações
oc status --suggest
```

---

## 🔍 Busca e Filtros

### Filtrar Projetos
```bash
# Projetos com label específica
oc get projects -l env=production

# Projetos com nome contendo string
oc get projects | grep dev

# Projetos ativos
oc get projects --field-selector status.phase=Active

# Projetos em terminação
oc get projects --field-selector status.phase=Terminating
```

### Análise de Projetos
```bash
# Contar total de projetos
oc get projects --no-headers | wc -l

# Projetos ordenados por criação
oc get projects --sort-by='.metadata.creationTimestamp'

# Projetos com suas labels
oc get projects -L env,tier,team

# Exportar lista de projetos
oc get projects -o json > all-projects.json
```

---

## 🛡️ Segurança e Permissões

### Verificar Permissões
```bash
# Verificar se pode criar projeto
oc auth can-i create projects

# Ver quem tem acesso ao projeto
oc get rolebindings

# Ver roles do projeto
oc get roles

# Adicionar usuário ao projeto
oc adm policy add-role-to-user admin <usuario> -n <projeto>

# Remover usuário do projeto
oc adm policy remove-role-from-user admin <usuario> -n <projeto>
```

---

## 💡 Boas Práticas

### Nomenclatura
- ✅ Use nomes descritivos: `app-producao`, `api-dev`
- ✅ Inclua ambiente no nome: `myapp-dev`, `myapp-qa`, `myapp-prod`
- ✅ Use labels para categorização: `env=prod`, `team=backend`
- ✅ Evite nomes genéricos: `test`, `temp`, `proj1`

### Organização
- ✅ Crie projetos separados por ambiente
- ✅ Use quotas para limitar recursos
- ✅ Configure network policies para isolamento
- ✅ Documente o propósito em annotations

### Segurança
- ✅ Limite quem pode criar projetos
- ✅ Use RBAC para controlar acesso
- ✅ Revise permissões regularmente
- ✅ Delete projetos não utilizados

---

## 🎓 Exemplos Práticos

### Criar Ambiente Completo
```bash
# 1. Criar projeto
oc new-project meu-app-dev \
  --description="Ambiente de desenvolvimento" \
  --display-name="Meu App - DEV"

# 2. Adicionar labels
oc label project meu-app-dev env=dev tier=backend team=devops

# 3. Configurar quota
cat <<EOF | oc create -f -
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    pods: "20"
EOF

# 4. Verificar
oc describe project meu-app-dev
oc get quota
```

### Migração entre Projetos
```bash
# 1. Exportar recursos do projeto origem
oc get all -n projeto-origem -o yaml > recursos.yaml

# 2. Criar projeto destino
oc new-project projeto-destino

# 3. Importar recursos (após ajustar namespace no YAML)
sed 's/projeto-origem/projeto-destino/g' recursos.yaml | oc create -f -
```

---

## 📖 Navegação

- [← Anterior: Autenticação](01-autenticacao-configuracao.md)
- [→ Próximo: Aplicações](03-aplicacoes.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
