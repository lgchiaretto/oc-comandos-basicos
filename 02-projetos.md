# Gerenciamento de Projetos

Este documento contém comandos para criar, listar e gerenciar projetos (namespaces) no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Conceitos](#conceitos)
3. [Criação e Listagem](#criação-e-listagem)
4. [Gerenciamento](#gerenciamento)
5. [Node Selectors](#node-selectors)
6. [Gerenciamento de Projetos](#gerenciamento-de-projetos)
7. [Templates de Projeto](#templates-de-projeto)
8. [Informações e Status](#informações-e-status)
9. [Busca e Filtros](#busca-e-filtros)
10. [Segurança e Permissões](#segurança-e-permissões)
11. [Exemplos Práticos](#exemplos-práticos)
12. [Boas Práticas](#boas-práticas)
13. [Documentação Oficial](#documentação-oficial)
14. [Navegação](#navegação)
---

## Conceitos

### O que é um Projeto?
Projetos no OpenShift são similares a namespaces do Kubernetes, mas com funcionalidades adicionais:
- Isolamento de recursos
- Quotas e limites
- RBAC (controle de acesso)
- Network policies

---

## Criação e Listagem

### Listar Projetos
```bash
# Listar projetos aos quais você tem acesso
oc projects
```

```bash
# Listar todos os projetos do cluster
oc get projects
```


```bash ignore-test
# Listar projetos exibindo todas as labels
oc get projects --show-labels
```

### Criar Projetos
```bash
# Criar novo projeto (namespace) no cluster
# oc new-project <project-name>
oc new-project development
```

```bash
# Exibir o projeto (namespace) atual
oc project
```

```bash
# Criar novo projeto com descrição e nome de exibição
# oc new-project <project-name> --description="Minha descrição" --display-name="Nome de Exibição"
oc new-project production --description="Minha descrição" --display-name="Nome de Exibição"
```

### Trocar entre Projetos
```bash
# Trocar para o projeto especificado
# oc project <project-name>
oc project development
```

```bash ignore-test
# Exemplo
# oc project <project-name>
oc project production
```

```bash
# Exibir o projeto (namespace) atual
oc project
```

---

## Gerenciamento

### Descrever e Inspecionar
```bash
# Exibir detalhes completos do projeto
# oc describe project <project-name>
oc describe project development
```

```bash
# Exibir projeto "development" em formato YAML
# oc get project <project-name> -o yaml
oc get project development -o yaml
```

```bash
# Exibir projeto "development" em formato JSON
# oc get project <project-name> -o json
oc get project development -o json
```

```bash
# Exibir projeto "development" em formato YAML
# oc get project <project-name> -o yaml > /tmp/projeto.yaml
oc get project development -o yaml > /tmp/projeto.yaml
```

### Editar Projetos
```bash ignore-test
# Abrir editor para modificar recurso interativamente
# oc edit project <project-name>
oc edit project development
```

```bash
# Adicionar nova label ao recurso
# oc label namespace <namespace-name> test-validation=true
oc label namespace development test-validation=true pod-security.kubernetes.io/enforce=privileged
```

```bash
# Atualizar label existente com novo valor
# oc label namespace <namespace-name> test-validation=true --overwrite
oc label namespace production test-validation=true pod-security.kubernetes.io/enforce=privileged --overwrite
```

```bash
# Adicionar annotation ao recurso
# oc annotate namespace <namespace-name> description="Meu projeto"
oc annotate namespace development description="Meu projeto"
```

```bash
# Remover label do recurso
# oc label namespace <namespace-name> env-
oc label namespace development env-
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch namespace <namespace-name> -p '{"metadata":{"labels":{"tier":"frontend"}}}'
oc patch namespace development -p '{"metadata":{"labels":{"tier":"frontend"}}}'
```

### Deletar Projetos
```bash ignore-test
# Deletar o projeto especificado
# oc delete project <project-name>
oc delete project development
```

```bash ignore-test
# Deletar o projeto especificado
# oc delete project <project-name> --wait=true
oc delete project development --wait=true
```

```bash ignore-test
# Deletar o projeto especificado
# oc delete project <project-name> production
oc delete project development production
```

>  **CUIDADO:** este comando deleta *todos* os recursos do projeto!

---

## Node Selectors

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
# Aplicar modificação parcial ao recurso usando patch
# oc patch namespace <namespace-name> -p '{"metadata":{"annotations":{"openshift.io/node-selector":"env=development"}}}'
oc patch namespace development -p '{"metadata":{"annotations":{"openshift.io/node-selector":"env=development"}}}'
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch namespace <namespace-name> -p '{"metadata":{"annotations":{"openshift.io/node-selector":""}}}'
oc patch namespace development -p '{"metadata":{"annotations":{"openshift.io/node-selector":""}}}'
```

## Gerenciamento de Projetos


### Labels em Namespaces
```bash ignore-test
# Adicionar labels ao namespace
oc label namespace development <key>=<value>
```

```bash
# Atualizar label existente com novo valor
# oc label namespace <namespace-name> env=development validation=true --overwrite
oc label namespace development env=development validation=true --overwrite
```

### Annotations em Namespaces
```bash ignore-test
# Adicionar annotation ao namespace
oc annotate namespace development <key>='<value>'
```

```bash
# Atualizar annotation existente com novo valor
# oc annotate namespace <namespace-name> test-maintainer='test-team' --overwrite
oc annotate namespace development test-maintainer='test-team' --overwrite
```

### Listar Service Accounts
```bash
# Listar todas as ServiceAccounts do namespace
oc get sa
```

```bash
# Em projeto específico
oc get sa -n development
```


---

## Templates de Projeto

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
# Criar novo recurso
# oc create -f /tmp/template.yaml -n <namespace>
oc create -f /tmp/template.yaml -n openshift-config
```

```bash ignore-test
# Abrir editor para modificar recurso interativamente
oc edit project.config.openshift.io/cluster
# Adicionar:
# spec:
# projectRequestTemplate:
# name: project-request
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

## Informações e Status

### Ver Recursos do Projeto
```bash
# Listar todos os recursos principais do namespace
oc get all
```

```bash
# Listar recursos específicos
oc get pods,svc,routes
```

```bash
# Listar quotas de recursos do namespace atual
oc get quota
```

```bash
oc describe quota
```

```bash
# Listar limit ranges configurados no namespace
oc get limitrange
```

```bash
oc describe limitrange
```

```bash
# Listar políticas de rede configuradas no namespace
oc get networkpolicy
```

### Status do Projeto
```bash
# Exibir visão geral dos recursos do projeto atual
oc status
```

```bash
# Exibir status com sugestões de ações
oc status --suggest
```

---

## Busca e Filtros

### Filtrar Projetos
```bash
# Projetos com nome contendo string
oc get projects | grep dev
```

```bash ignore-test
# Exibir projetos em formato JSON
oc get projects -o jsonpath='{.items[?(@.status.phase=="Active")].metadata.name}'
```

```bash ignore-test
# Exibir projetos em formato JSON
oc get projects -o jsonpath='{.items[?(@.status.phase=="Terminating")].metadata.name}'
```

### Análise de Projetos
```bash
# Contar total de projetos
oc get projects --no-headers | wc -l
```

```bash
# Listar projetos ordenados por campo específico
oc get projects --sort-by='.metadata.creationTimestamp'
```

```bash
# Listar projetos filtrados por label
oc get projects -l env=development
```

```bash
# Exibir projetos em formato JSON
oc get projects -o json > /tmp/all-projects.json
```

---

## Segurança e Permissões

### Verificar Permissões
```bash
# Verificar se usuário tem permissão para executar ação específica
oc auth can-i create projects
```

```bash
# Listar vinculações de roles no namespace atual
oc get rolebindings
```

```bash
# Listar roles customizados do namespace
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

## Exemplos Práticos

### Criar Ambiente Completo
```bash ignore-test
# Criar novo projeto (namespace) no cluster
# oc new-project <project-name> \
oc new-project meu-app-dev \
  --description="Ambiente de desenvolvimento" \
  --display-name="Meu App - DEV"
```

```bash ignore-test
# Adicionar nova label ao recurso
# oc label project <project-name> env=dev tier=backend team=devops
oc label project meu-app-dev env=dev tier=backend team=devops
```

```bash ignore-test
# Criar novo recurso
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
# Listar quotas de recursos do namespace atual
oc get quota
```

### Migração entre Projetos
```bash ignore-test
# Exibir recurso em formato YAML
oc get all -n projeto-origem -o yaml > recursos.yaml
```

```bash ignore-test
# Criar novo projeto (namespace) no cluster
# oc new-project <project-name>
oc new-project projeto-destino
```

```bash ignore-test
# Criar novo recurso
sed 's/projeto-origem/projeto-destino/g' recursos.yaml | oc create -f -
```

---


## Boas Práticas

### Nomenclatura
-  Use nomes descritivos: `app-production`, `api-dev`
-  Inclua ambiente no nome: `myapp-dev`, `myapp-qa`, `myapp-prod`
-  Use labels para categorização: `env=prod`, `team=backend`
-  Evite nomes genéricos: `test`, `temp`, `proj1`

### Organização
-  Crie projetos separados por ambiente
-  Use quotas para limitar recursos
-  Configure network policies para isolamento
-  Documente o propósito em annotations

### Segurança
-  Limite quem pode criar projetos
-  Use RBAC para controlar acesso
-  Revise permissões regularmente
-  Delete projetos não utilizados

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/projects">Working with projects</a>
---

---

## Navegação

- [← Anterior: Autenticação](01-autenticacao-configuracao.md)
- [→ Próximo: Aplicações](03-aplicacoes.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
