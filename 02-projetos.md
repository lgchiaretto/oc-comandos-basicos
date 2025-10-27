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
**Listar projetos aos quais você tem acesso**

```bash
oc projects
```

**Listar todos os projetos do cluster**

```bash
oc get projects
```


**Listar projetos exibindo todas as labels**

```bash ignore-test
oc get projects --show-labels
```

### Criar Projetos
**Criar novo projeto (namespace) no cluster**


```bash
oc new-project development
```

**Exibir o projeto (namespace) atual**

```bash
oc project
```

**Criar novo projeto com descrição e nome de exibição**


```bash
oc new-project production --description="Minha descrição" --display-name="Nome de Exibição"
```

### Trocar entre Projetos
**Trocar para o projeto especificado**


```bash
oc project development
```

**Exemplo**


```bash ignore-test
oc project production
```

**Exibir o projeto (namespace) atual**

```bash
oc project
```

---

## Gerenciamento

### Descrever e Inspecionar
**Exibir detalhes completos do projeto**


```bash
oc describe project development
```

**Exibir projeto "development" em formato YAML**


```bash
oc get project development -o yaml
```

**Exibir projeto "development" em formato JSON**


```bash
oc get project development -o json
```

**Exibir projeto "development" em formato YAML**


```bash
oc get project development -o yaml > /tmp/projeto.yaml
```

### Editar Projetos
**Abrir editor para modificar recurso interativamente**


```bash ignore-test
oc edit project development
```

**Adicionar nova label ao recurso**


```bash
oc label namespace development test-validation=true pod-security.kubernetes.io/enforce=privileged
```

**Atualizar label existente com novo valor**


```bash
oc label namespace production test-validation=true pod-security.kubernetes.io/enforce=privileged --overwrite
```

**Adicionar annotation ao recurso**


```bash
oc annotate namespace development description="Meu projeto"
```

**Remover label do recurso**


```bash
oc label namespace development env-
```

**Aplicar modificação parcial ao recurso usando patch**


```bash
oc patch namespace development -p '{"metadata":{"labels":{"tier":"frontend"}}}'
```

### Deletar Projetos
**Deletar o projeto especificado**


```bash ignore-test
oc delete project development
```

**Deletar o projeto especificado**


```bash ignore-test
oc delete project development --wait=true
```

**Deletar o projeto especificado**


```bash ignore-test
oc delete project development production
```

>  **CUIDADO:** este comando deleta *todos* os recursos do projeto!

---

## Node Selectors

### Criar Projeto com Node Selector
**Criar projeto com node selector para ambiente**

```bash ignore-test
oc new-project <nome> --node-selector='env=prd'
```

**Criar projeto sem node selector (permite qualquer node)**

```bash ignore-test
oc new-project <nome> --node-selector=""
```

**Criar projeto com node selector específico por hostname**

```bash ignore-test
oc new-project <nome> --node-selector="kubernetes.io/hostname=<hostname>"
```

**Exemplo prático**


```bash ignore-test
oc new-project production --node-selector='env=production'
```

### Modificar Node Selector Existente
**Aplicar modificação parcial ao recurso usando patch**


```bash
oc patch namespace development -p '{"metadata":{"annotations":{"openshift.io/node-selector":"env=development"}}}'
```

**Aplicar modificação parcial ao recurso usando patch**


```bash
oc patch namespace development -p '{"metadata":{"annotations":{"openshift.io/node-selector":""}}}'
```

## Gerenciamento de Projetos


### Labels em Namespaces
**Adicionar labels ao namespace**

```bash ignore-test
oc label namespace development <key>=<value>
```

**Atualizar label existente com novo valor**


```bash
oc label namespace development env=development validation=true --overwrite
```

### Annotations em Namespaces
**Adicionar annotation ao namespace**

```bash ignore-test
oc annotate namespace development <key>='<value>'
```

**Atualizar annotation existente com novo valor**


```bash
oc annotate namespace development test-maintainer='test-team' --overwrite
```

### Listar Service Accounts
**Listar todas as ServiceAccounts do namespace**

```bash
oc get sa
```

**Em projeto específico**

```bash
oc get sa -n development
```


---

## Templates de Projeto

### Criar Template de Projeto Customizado
**Gerar template padrão**

```bash ignore-test
oc adm create-bootstrap-project-template -o yaml > /tmp/template.yaml
```

**Editar template**

```bash ignore-test
vim /tmp/template.yaml
```

**Criar novo recurso**


```bash ignore-test
oc create -f /tmp/template.yaml -n openshift-config
```

**Abrir editor para modificar recurso interativamente**
* Adicionar:
* spec:
* projectRequestTemplate:
* name: project-request

```bash ignore-test
oc edit project.config.openshift.io/cluster
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
**Listar todos os recursos principais do namespace**

```bash
oc get all
```

**Listar recursos específicos**

```bash
oc get pods,svc,routes
```

**Listar quotas de recursos do namespace atual**

```bash
oc get quota
```

```bash
oc describe quota
```

**Listar limit ranges configurados no namespace**

```bash
oc get limitrange
```

```bash
oc describe limitrange
```

**Listar políticas de rede configuradas no namespace**

```bash
oc get networkpolicy
```

### Status do Projeto
**Exibir visão geral dos recursos do projeto atual**

```bash
oc status
```

**Exibir status com sugestões de ações**

```bash
oc status --suggest
```

---

## Busca e Filtros

### Filtrar Projetos
**Projetos com nome contendo string**

```bash
oc get projects | grep dev
```

**Exibir projetos em formato JSON**

```bash ignore-test
oc get projects -o jsonpath='{.items[?(@.status.phase=="Active")].metadata.name}'
```

**Exibir projetos em formato JSON**

```bash ignore-test
oc get projects -o jsonpath='{.items[?(@.status.phase=="Terminating")].metadata.name}'
```

### Análise de Projetos
**Contar total de projetos**

```bash
oc get projects --no-headers | wc -l
```

**Listar projetos ordenados por campo específico**

```bash
oc get projects --sort-by='.metadata.creationTimestamp'
```

**Listar projetos filtrados por label**

```bash
oc get projects -l env=development
```

**Exibir projetos em formato JSON**

```bash
oc get projects -o json > /tmp/all-projects.json
```

---

## Segurança e Permissões

### Verificar Permissões
**Verificar se usuário tem permissão para executar ação específica**

```bash
oc auth can-i create projects
```

**Listar vinculações de roles no namespace atual**

```bash
oc get rolebindings
```

**Listar roles customizados do namespace**

```bash
oc get roles
```

**Adicionar usuário ao projeto**

```bash ignore-test
oc adm policy add-role-to-user admin <usuario> -n <projeto>
```

**Remover usuário do projeto**

```bash ignore-test
oc adm policy remove-role-from-user admin <usuario> -n <projeto>
```

---

## Exemplos Práticos

### Criar Ambiente Completo
**Criar novo projeto (namespace) no cluster**


```bash ignore-test
oc new-project meu-app-dev \
  --description="Ambiente de desenvolvimento" \
  --display-name="Meu App - DEV"
```

**Adicionar nova label ao recurso**


```bash ignore-test
oc label project meu-app-dev env=dev tier=backend team=devops
```

**Criar novo recurso**

```bash ignore-test
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

**Listar quotas de recursos do namespace atual**

```bash ignore-test
oc get quota
```

### Migração entre Projetos
**Exibir recurso em formato YAML**

```bash ignore-test
oc get all -n projeto-origem -o yaml > recursos.yaml
```

**Criar novo projeto (namespace) no cluster**


```bash ignore-test
oc new-project projeto-destino
```

**Criar novo recurso**

```bash ignore-test
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
