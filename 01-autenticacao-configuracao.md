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
```bash ignore-test
# Login no cluster OpenShift
oc login <url-do-cluster>
```

```bash ignore-test
# Login com usuário e senha
oc login <url-do-cluster> -u <usuario> -p <senha>
```

```bash ignore-test
# Login com token
oc login --token=<token> --server=<url-do-cluster>
```

```bash ignore-test
# Exemplo prático
oc login https://api.cluster.example.com:6443 -u developer -p mypassword
```

### Verificar Autenticação
```bash
# Exibir o nome do usuário autenticado atualmente
oc whoami
```

```bash
# Exibir o token de autenticação do usuário atual
oc whoami -t
```

```bash
# Exibir o contexto atual do kubeconfig
oc whoami --show-context
```

```bash
# Exibir a URL da console web do cluster
oc whoami --show-console
```

```bash
# Exibir a URL do servidor API conectado
oc whoami --show-server
```

### Logout
```bash ignore-test
# Fazer logout
oc logout
```

```bash ignore-test
# Fazer logout e limpar contexto
oc logout && rm -f ~/.kube/config
```

---

## Informações do Cluster


### Listar API Resources
```bash
# Listar todos os recursos da API disponíveis no cluster
oc api-resources
```

```bash
# Filtrar por verbo
oc api-resources --verbs=list,get
```

```bash
# Filtrar por grupo de API
oc api-resources --api-group=apps
```

```bash
# Ver recursos com alias
oc api-resources | grep -E '^(NAME|pod|deploy|svc)'
```

### Listar API Versions
```bash
# Listar todas as versões de API disponíveis
oc api-versions
```

```bash
# Ver versões específicas do grupo
oc api-versions | grep apps
```

```bash
# Ver versões do core
oc api-versions | grep -v "/"
```

## Configuração do Cliente

### Versão e Informações
```bash
# Exibir versão do cliente oc e do servidor OpenShift
oc version
```

```bash
# Exibir informações básicas do cluster
oc cluster-info
```

```bash
# Ver informações do servidor
oc cluster-info dump
```

### Configuração
```bash
# Exibir configuração atual do kubeconfig
oc config view
```

```bash
# Exibir configuração com credenciais (cuidado!)
oc config view --raw
```

```bash
# Exibir conteúdo do arquivo de configuração do kubectl/oc
cat ~/.kube/config
```

### Namespace Padrão
```bash
# Definir namespace padrão para o contexto atual
oc config set-context --current --namespace=development
```
---

## Contextos

### Listar e Gerenciar Contextos
```bash
# Listar todos os contextos disponíveis
oc config get-contexts
```

```bash
# Exibir o contexto atual do kubeconfig
oc config current-context
```

```bash ignore-test
# Trocar de contexto
oc config use-context <nome-do-contexto>
```

```bash ignore-test
# Renomear contexto
oc config rename-context <nome-antigo> <nome-novo>
```

```bash ignore-test
# Deletar contexto
oc config delete-context <nome-do-contexto>
```

### Criar Contextos Customizados
```bash ignore-test
# Criar novo contexto
oc config set-context <nome-do-contexto> \
  --cluster=<cluster> \
  --user=<usuario> \
  --namespace=<namespace>
```

```bash ignore-test
# Exemplo
oc config set-context dev-context \
  --cluster=dev-cluster \
  --user=developer \
  --namespace=development
```

```bash ignore-test
# Criar contexto para o cluster
oc config set-context <contexto> \
  --cluster=<cluster> \
  --user=<usuario>
```

### Variáveis de Ambiente
```bash ignore-test
# Definir KUBECONFIG customizado
export KUBECONFIG=/path/to/kubeconfig
```

```bash ignore-test
# Múltiplos kubeconfigs
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

---

## Navegação

- [→ Próximo: Projetos](02-projetos.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025


```markdown
**Ação:** Deletar recurso forçadamente (sem período de espera).

* `--grace-period=0`: Define o período de espera para zero, forçando a remoção imediata.
* `--force`: Força a deleção do recurso.
```

```bash
oc delete pod my-pod --grace-period=0 --force
```