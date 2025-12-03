# Autenticação e Configuração

Este documento contém comandos essenciais para autenticação e configuração do cliente OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Login e Logout](#login-e-logout)
3. [Informações do Cluster](#informações-do-cluster)
4. [Configuração do Cliente](#configuração-do-cliente)
5. [Contextos](#contextos)
6. [Boas Práticas](#boas-práticas)
7. [Documentação Oficial](#documentação-oficial)
8. [Navegação](#navegação)
---

## Login e Logout

### Login Básico
**Login no cluster OpenShift**

```bash ignore-test
oc login <url-do-cluster>
```

**Login com usuário e senha**

```bash ignore-test
oc login <url-do-cluster> -u <usuario> -p <senha>
```

**Login com token**

```bash ignore-test
oc login --token=<token> --server=<url-do-cluster>
```

**Exemplo prático**

```bash ignore-test
oc login https://api.cluster.example.com:6443 -u developer -p mypassword
```

### Verificar Autenticação
**Exibir o nome do usuário autenticado atualmente**

```bash
oc whoami
```

**Exibir o token de autenticação do usuário atual**

```bash
oc whoami -t
```

**Exibir o contexto atual do kubeconfig**

```bash
oc whoami --show-context
```

**Exibir a URL da console web do cluster**

```bash
oc whoami --show-console
```

**Exibir a URL do servidor API conectado**

```bash
oc whoami --show-server
```

### Logout
**Fazer logout**

```bash ignore-test
oc logout
```

**Fazer logout e limpar contexto**

```bash ignore-test
oc logout && rm -f ~/.kube/config
```

---

## Informações do Cluster


### Listar API Resources
**Listar todos os recursos da API disponíveis no cluster**

```bash
oc api-resources
```

**Filtrar por verbo**

```bash
oc api-resources --verbs=list,get
```

**Filtrar por grupo de API**

```bash
oc api-resources --api-group=apps
```

**Ver recursos com alias**

```bash
oc api-resources | grep -E '^(NAME|pod|deploy|svc)'
```

### Listar API Versions
**Listar todas as versões de API disponíveis**

```bash
oc api-versions
```

**Filtrar saída filtrando por Apps**

```bash
oc api-versions | grep apps
```

**Ver versões do core**

```bash
oc api-versions | grep -v "/"
```

## Configuração do Cliente

### Versão e Informações
**Exibir versão do cliente oc e do servidor OpenShift**

```bash
oc version
```

**Exibir informações básicas do cluster**

```bash
oc cluster-info
```

**Ver informações do servidor**

```bash
oc cluster-info dump
```

### Configuração
**Exibir configuração atual do kubeconfig**

```bash
oc config view
```

**Exibir configuração com credenciais (cuidado!)**

```bash
oc config view --raw
```

**Exibir conteúdo do arquivo de configuração do kubectl/oc**

```bash
cat ~/.kube/config
```

### Namespace Padrão
**Definir namespace padrão para o contexto atual**

```bash
oc config set-context --current --namespace=development
```
---

## Contextos

### Listar e Gerenciar Contextos
**Listar todos os contextos disponíveis**

```bash
oc config get-contexts
```

**Exibir o contexto atual do kubeconfig**

```bash
oc config current-context
```

**Trocar de contexto**

```bash ignore-test
oc config use-context <nome-do-contexto>
```

**Renomear contexto**

```bash ignore-test
oc config rename-context <nome-antigo> <nome-novo>
```

**Deletar contexto**

```bash ignore-test
oc config delete-context <nome-do-contexto>
```

### Criar Contextos Customizados
**Criar novo contexto**

```bash ignore-test
oc config set-context <nome-do-contexto> \
  --cluster=<cluster> \
  --user=<usuario> \
  --namespace=<namespace>
```

**Exemplo**

```bash ignore-test
oc config set-context dev-context \
  --cluster=dev-cluster \
  --user=developer \
  --namespace=development
```

**Criar contexto para o cluster**

```bash ignore-test
oc config set-context <contexto> \
  --cluster=<cluster> \
  --user=<usuario>
```

### Variáveis de Ambiente
**Definir KUBECONFIG customizado**

```bash ignore-test
export KUBECONFIG=/path/to/kubeconfig
```

**Múltiplos kubeconfigs**

```bash ignore-test
export KUBECONFIG=/path/to/config1:/path/to/config2
```
---

## Boas Práticas

### Segurança
-  Nunca compartilhe seu token de acesso
-  Use `oc login` ao invés de guardar token em scripts
-  Faça logout ao terminar, especialmente em máquinas compartilhadas

### Organização
-  Use contextos descritivos (dev, qa, prod) mesmo em clusters distintos
-  Mantenha múltiplos kubeconfigs separados por ambiente

### Troubleshooting
-  Use `oc whoami` para verificar autenticação
-  Use `oc config view` para ver configuração atual
-  Use `-v=8` para debug detalhado

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools">CLI Tools</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/openshift-cli-oc">OpenShift CLI (oc)</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization">Authentication and Authorization</a>
---


## Navegação

- [→ Próximo: Projetos](02-projetos.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Dezembro 2025