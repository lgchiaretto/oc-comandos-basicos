# 🔐 Autenticação e Configuração

Este documento contém comandos essenciais para autenticação e configuração do cliente OpenShift.

---

## 📋 Índice

1. [Login e Logout](#login-e-logout)
2. [Configuração do Cliente](#configuração-do-cliente)
3. [Contextos](#contextos)
4. [Verificações](#verificações)

---

## 🔑 Login e Logout

### Login Básico
```bash
# Login no cluster OpenShift
oc login <url-do-cluster>
```

```bash
# Login com usuário e senha
oc login <url-do-cluster> -u <usuario> -p <senha>
```

```bash
# Login com token
oc login --token=<token> --server=<url-do-cluster>
```

```bash
# Exemplo prático
oc login https://api.cluster.example.com:6443 -u developer -p mypassword
```

### Verificar Autenticação
```bash
# Verificar usuário atual
oc whoami
```

```bash
# Verificar token de acesso
oc whoami -t
```

```bash
# Verificar contexto atual
oc whoami --show-context
```

```bash
# Verificar a URL da console
oc whoami --show-console
```

```bash
# Verificar servidor conectado
oc whoami --show-server
```

### Logout
```bash ignore
# Fazer logout
oc logout
```

```bash ignore
# Fazer logout e limpar contexto
oc logout && rm -f ~/.kube/config
```

---

## 🔍 Informações do Cluster


### Listar API Resources
```bash
# Listar todos os recursos da API disponíveis
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
# Listar todas as versões da API disponíveis
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

## ⚙️ Configuração do Cliente

### Versão e Informações
```bash
# Verificar versão do oc
oc version
```

```bash
# Verificar informações do cluster
oc cluster-info
```

```bash
# Ver informações do servidor
oc cluster-info dump
```

### Configuração
```bash
# Exibir configuração atual
oc config view
```

```bash
# Exibir configuração com credenciais (cuidado!)
oc config view --raw
```

```bash
# Ver arquivo de configuração ~/.kube/config
cat ~/.kube/config
```

### Namespace Padrão
```bash
# Definir namespace padrão para o contexto atual
oc config set-context --current --namespace=development
```

```bash
# Exemplo
oc config set-context --current --namespace=production
```

---

## 🔄 Contextos

### Listar e Gerenciar Contextos
```bash
# Listar todos os contextos
oc config get-contexts
```

```bash
# Ver contexto atual
oc config current-context
```

```bash
# Trocar de contexto
oc config use-context <nome-do-contexto>
```

```bash
# Renomear contexto
oc config rename-context <nome-antigo> <nome-novo>
```

```bash
# Deletar contexto
oc config delete-context <nome-do-contexto>
```

### Criar Contextos Customizados
```bash
# Criar novo contexto
oc config set-context <nome-do-contexto> \
  --cluster=<cluster> \
  --user=<usuario> \
  --namespace=<namespace>
```

```bash
# Exemplo
oc config set-context dev-context \
  --cluster=dev-cluster \
  --user=developer \
  --namespace=development
```

## 🔧 Configurações Avançadas

### Múltiplos Clusters
```bash
# Adicionar cluster
oc config set-cluster <nome-cluster> \
  --server=<url> \
  --certificate-authority=<ca-file>
```

```bash
# Adicionar usuário
oc config set-credentials <nome-usuario> \
  --token=<token>
```

```bash
# Criar contexto para o cluster
oc config set-context <contexto> \
  --cluster=<cluster> \
  --user=<usuario>
```

### Variáveis de Ambiente
```bash
# Definir KUBECONFIG customizado
export KUBECONFIG=/path/to/kubeconfig
```

```bash
# Múltiplos kubeconfigs
export KUBECONFIG=/path/to/config1:/path/to/config2
```
---

## 📝 Boas Práticas

### Segurança
- ✅ Nunca compartilhe seu token de acesso
- ✅ Use `oc login` ao invés de guardar token em scripts
- ✅ Faça logout ao terminar, especialmente em máquinas compartilhadas
- ✅ Não use `--insecure-skip-tls-verify` em produção

### Organização
- ✅ Use contextos descritivos (dev, qa, prod)
- ✅ Configure namespace padrão para cada contexto
- ✅ Mantenha múltiplos kubeconfigs separados por ambiente
- ✅ Use aliases para facilitar login em diferentes clusters

### Troubleshooting
- ✅ Use `oc whoami` para verificar autenticação
- ✅ Use `oc config view` para ver configuração atual
- ✅ Use `-v=8` para debug detalhado
- ✅ Verifique permissões com `oc auth can-i --list`

---

## 📖 Navegação

- [→ Próximo: Projetos](02-projetos.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
