# 📁 Gerenciamento de Projetos

Este documento contém comandos para criar, listar e gerenciar projetos (namespaces) no OpenShift.

---

## 📋 Índice

1. [💡 Conceitos](#conceitos)
2. [🆕 Criação e Listagem](#criacao-e-listagem)
3. [🔧 Gerenciamento](#gerenciamento)
4. [🎯 Node Selectors](#node-selectors)
5. [🔧 Gerenciamento de Projetos](#gerenciamento-de-projetos)
6. [📄 Templates de Projeto](#templates-de-projeto)
7. [📊 Informações e Status](#informacoes-e-status)
8. [🔍 Busca e Filtros](#busca-e-filtros)
9. [🛡 ️ Segurança e Permissões](#seguranca-e-permissoes)
10. [🎓 Exemplos Práticos](#exemplos-praticos)
11. [💡 Boas Práticas](#boas-praticas)
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
```

```bash
# Listar projetos (formato detalhado)
oc get projects
```


```bash ignore-test
# Listar com labels
oc get projects --show-labels
```

### Criar Projetos
```bash
# Criar novo projeto
# oc new-project <project-name>
oc new-project development
```

```bash
# Ver projeto atual
oc project
```

```bash
# Criar projeto com descrição
# oc new-project <project-name> --description="Minha descrição" --display-name="Nome de Exibição"
oc new-project production --description="Minha descrição" --display-name="Nome de Exibição"
```

### Trocar entre Projetos
```bash
# Trocar para outro projeto
# oc project <project-name>
oc project development
```

```bash ignore-test
# Exemplo
# oc project <project-name>
oc project production
```

```bash
# Verificar projeto atual
oc project
```

---

## 🔧 Gerenciamento

### Descrever e Inspecionar
```bash
# Descrever um projeto
# oc describe project <project-name>
oc describe project development
```

```bash
# Ver em YAML
# oc get project <project-name> -o yaml
oc get project development -o yaml
```

```bash
# Ver em JSON
# oc get project <project-name> -o json
oc get project development -o json
```

```bash
# Exportar definição do projeto
# oc get project <project-name> -o yaml > /tmp/projeto.yaml
oc get project development -o yaml > /tmp/projeto.yaml
```

### Editar Projetos
```bash ignore-test
# Editar projeto
# oc edit project <project-name>
oc edit project development
```

```bash
# Adicionar label
# oc label namespace <namespace-name> test-validation=true
oc label namespace development test-validation=true pod-security.kubernetes.io/enforce=privileged
```

```bash
# Trocar o valor de uma label existente
# oc label namespace <namespace-name> test-validation=true --overwrite
oc label namespace production test-validation=true pod-security.kubernetes.io/enforce=privileged --overwrite
```

```bash
# Adicionar annotation
# oc annotate namespace <namespace-name> description="Meu projeto"
oc annotate namespace development description="Meu projeto"
```

```bash
# Remover label
# oc label namespace <namespace-name> env-
oc label namespace development env-
```

```bash
# Patch de projeto
# oc patch namespace <namespace-name> -p '{"metadata":{"labels":{"tier":"frontend"}}}'
oc patch namespace development -p '{"metadata":{"labels":{"tier":"frontend"}}}'
```

### Deletar Projetos
```bash ignore-test
# Deletar um projeto
# oc delete project <project-name>
oc delete project development
```

```bash ignore-test
# Deletar com confirmação
# oc delete project <project-name> --wait=true
oc delete project development --wait=true
```

```bash ignore-test
# Deletar múltiplos projetos
# oc delete project <project-name> production
oc delete project development production
```

> ⚠️ **CUIDADO:** este comando deleta *todos* os recursos do projeto!

---

## 🎯 Node Selectors

### Criar Projeto com Node Selector
```bash ignore-test
# Criar projeto com node selector para ambiente
oc new-project <nome> --node-selector='env=prd'
```

```bash ignore-test
# Criar projeto sem node selector (permite qualquer node)
oc new-project <nome> --node-selector=""
```

```bash ignore-test
# Criar projeto com node selector específico por hostname
oc new-project <nome> --node-selector="kubernetes.io/hostname=<hostname>"
```

```bash ignore-test
# Exemplo prático
# oc new-project <project-name> --node-selector='env=production'
oc new-project production --node-selector='env=production'
```

### Modificar Node Selector Existente
```bash
# Adicionar node selector a projeto existente
# oc patch namespace <namespace-name> -p '{"metadata":{"annotations":{"openshift.io/node-selector":"env=development"}}}'
oc patch namespace development -p '{"metadata":{"annotations":{"openshift.io/node-selector":"env=development"}}}'
```

```bash
# Remover node selector
# oc patch namespace <namespace-name> -p '{"metadata":{"annotations":{"openshift.io/node-selector":""}}}'
oc patch namespace development -p '{"metadata":{"annotations":{"openshift.io/node-selector":""}}}'
```

## 🔧 Gerenciamento de Projetos


### Labels em Namespaces
```bash ignore-test
# Adicionar labels ao namespace
oc label namespace development <key>=<value>
```

```bash
# Adicionar múltiplas labels
# oc label namespace <namespace-name> env=development validation=true --overwrite
oc label namespace development env=development validation=true --overwrite
```

### Annotations em Namespaces
```bash ignore-test
# Adicionar annotation ao namespace
oc annotate namespace development <key>='<value>'
```

```bash
# Sobrescrever annotation existente
# oc annotate namespace <namespace-name> test-maintainer='test-team' --overwrite
oc annotate namespace development test-maintainer='test-team' --overwrite
```

### Listar Service Accounts
```bash
# Listar service accounts do projeto
oc get sa
```

```bash
# Em projeto específico
oc get sa -n development
```


---

## 📄 Templates de Projeto

### Criar Template de Projeto Customizado
```bash ignore-test
# Gerar template padrão
oc adm create-bootstrap-project-template -o yaml > /tmp/template.yaml
```

```bash ignore-test
# Editar template
vim /tmp/template.yaml
```

```bash ignore-test
# Aplicar template customizado
# oc create -f /tmp/template.yaml -n <namespace>
oc create -f /tmp/template.yaml -n openshift-config
```

```bash ignore-test
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
```

```bash
# Listar recursos específicos
oc get pods,svc,routes
```

```bash
# Ver quotas do projeto
oc get quota
```

```bash
oc describe quota
```

```bash
# Ver limit ranges
oc get limitrange
```

```bash
oc describe limitrange
```

```bash
# Ver network policies
oc get networkpolicy
```

### Status do Projeto
```bash
# Status geral
oc status
```

```bash
# Status sugerindo ações
oc status --suggest
```

---

## 🔍 Busca e Filtros

### Filtrar Projetos
```bash
# Projetos com nome contendo string
oc get projects | grep dev
```

```bash ignore-test
# Projetos ativos
oc get projects -o jsonpath='{.items[?(@.status.phase=="Active")].metadata.name}'
```

```bash ignore-test
# Projetos em terminação
oc get projects -o jsonpath='{.items[?(@.status.phase=="Terminating")].metadata.name}'
```

### Análise de Projetos
```bash
# Contar total de projetos
oc get projects --no-headers | wc -l
```

```bash
# Projetos ordenados por criação
oc get projects --sort-by='.metadata.creationTimestamp'
```

```bash
# Projetos com label env=test
oc get projects -l env=development
```

```bash
# Exportar lista de projetos
oc get projects -o json > /tmp/all-projects.json
```

---

## 🛡️ Segurança e Permissões

### Verificar Permissões
```bash
# Verificar se pode criar projeto
oc auth can-i create projects
```

```bash
# Ver quem tem acesso ao projeto
oc get rolebindings
```

```bash
# Ver roles do projeto
oc get roles
```

```bash ignore-test
# Adicionar usuário ao projeto
oc adm policy add-role-to-user admin <usuario> -n <projeto>
```

```bash ignore-test
# Remover usuário do projeto
oc adm policy remove-role-from-user admin <usuario> -n <projeto>
```

---

## 🎓 Exemplos Práticos

### Criar Ambiente Completo
```bash ignore-test
# 1. Criar projeto
# oc new-project <project-name> \
oc new-project meu-app-dev \
  --description="Ambiente de desenvolvimento" \
  --display-name="Meu App - DEV"
```

```bash ignore-test
# 2. Adicionar labels
# oc label project <project-name> env=dev tier=backend team=devops
oc label project meu-app-dev env=dev tier=backend team=devops
```

```bash ignore-test
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
```

```bash ignore-test
# 4. Verificar
oc get quota
```

### Migração entre Projetos
```bash ignore-test
# 1. Exportar recursos do projeto origem
oc get all -n projeto-origem -o yaml > recursos.yaml
```

```bash ignore-test
# 2. Criar projeto destino
# oc new-project <project-name>
oc new-project projeto-destino
```

```bash ignore-test
# 3. Importar recursos (após ajustar namespace no YAML)
sed 's/projeto-origem/projeto-destino/g' recursos.yaml | oc create -f -
```

---


## 💡 Boas Práticas

### Nomenclatura
- ✅ Use nomes descritivos: `app-production`, `api-dev`
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


---

## 📚 Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- [Building applications](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications)

---

## 📖 Navegação

- [← Anterior: Autenticação](01-autenticacao-configuracao.md)
- [→ Próximo: Aplicações](03-aplicacoes.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
