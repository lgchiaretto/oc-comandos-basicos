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

# Login com usuário e senha
oc login <url-do-cluster> -u <usuario> -p <senha>

# Login com token
oc login --token=<token> --server=<url-do-cluster>

# Exemplo prático
oc login https://api.cluster.example.com:6443 -u developer -p mypassword
```

### Verificar Autenticação
```bash
# Verificar usuário atual
oc whoami

# Verificar token de acesso
oc whoami -t

# Verificar contexto atual
oc whoami --show-context

# Verificar a URL da console
oc whoami --show-console

# Verificar servidor conectado
oc whoami --show-server
```

### Logout
```bash
# Fazer logout
oc logout

# Fazer logout e limpar contexto
oc logout && rm -f ~/.kube/config
```

---

## 🔍 Informações do Cluster


### Listar API Resources
```bash
# Listar todos os recursos da API disponíveis
oc api-resources

# Filtrar por verbo
oc api-resources --verbs=list,get

# Filtrar por grupo de API
oc api-resources --api-group=apps

# Ver recursos com alias
oc api-resources | grep -E '^(NAME|pod|deploy|svc)'
```

### Listar API Versions
```bash
# Listar todas as versões da API disponíveis
oc api-versions

# Ver versões específicas do grupo
oc api-versions | grep apps

# Ver versões do core
oc api-versions | grep -v "/"
```

## ⚙️ Configuração do Cliente

### Versão e Informações
```bash
# Verificar versão do oc
oc version

# Verificar informações do cluster
oc cluster-info

# Ver informações do servidor
oc cluster-info dump
```

### Configuração
```bash
# Exibir configuração atual
oc config view

# Exibir configuração com credenciais (cuidado!)
oc config view --raw

# Ver arquivo de configuração
cat ~/.kube/config

```

### Namespace Padrão
```bash
# Definir namespace padrão para o contexto atual
oc config set-context --current --namespace=<nome-do-projeto>

# Exemplo
oc config set-context --current --namespace=production
```

---

## 🔄 Contextos

### Listar e Gerenciar Contextos
```bash
# Listar todos os contextos
oc config get-contexts

# Ver contexto atual
oc config current-context

# Trocar de contexto
oc config use-context <nome-do-contexto>

# Renomear contexto
oc config rename-context <nome-antigo> <nome-novo>

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

# Exemplo
oc config set-context dev-context \
  --cluster=dev-cluster \
  --user=developer \
  --namespace=development
```

---

## ✅ Verificações

### Status de Conexão
```bash
# Verificar se está conectado
oc whoami 2>/dev/null && echo "Conectado" || echo "Não conectado"

# Testar conexão com API
oc get --raw /healthz

# Ver endpoints da API
oc api-resources

# Ver versões da API
oc api-versions
```

### Troubleshooting de Conexão
```bash
# Verificar certificados SSL
oc login <url> --insecure-skip-tls-verify=true

# Debug de conexão
oc login <url> -v=8

# Testar proxy
oc --proxy-url=http://proxy:port login <url>

# Limpar cache de autenticação
rm -rf ~/.kube/cache
```

---

## 🔧 Configurações Avançadas

### Múltiplos Clusters
```bash
# Adicionar cluster
oc config set-cluster <nome-cluster> \
  --server=<url> \
  --certificate-authority=<ca-file>

# Adicionar usuário
oc config set-credentials <nome-usuario> \
  --token=<token>

# Criar contexto para o cluster
oc config set-context <contexto> \
  --cluster=<cluster> \
  --user=<usuario>
```

### Variáveis de Ambiente
```bash
# Definir KUBECONFIG customizado
export KUBECONFIG=/path/to/kubeconfig

# Múltiplos kubeconfigs
export KUBECONFIG=/path/to/config1:/path/to/config2

# Editor padrão
export OC_EDITOR=nano

# Namespace padrão
export KUBECONFIG_NAMESPACE=default
```

### Aliases Úteis
```bash
# Adicionar ao ~/.bashrc ou ~/.zshrc
alias oclogin='oc login https://api.cluster.example.com:6443'
alias ocdev='oc login https://dev-cluster.example.com:6443'
alias ocprd='oc login https://prd-cluster.example.com:6443'
alias ocwho='oc whoami && oc project'
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

## 🔐 Exemplo Completo de Setup

```bash
# 1. Login
oc login https://api.cluster.example.com:6443 -u admin

# 2. Verificar conexão
oc whoami
oc cluster-info

# 3. Configurar namespace padrão
oc config set-context --current --namespace=my-project

# 4. Criar alias
echo "alias k='oc'" >> ~/.bashrc
source ~/.bashrc

# 5. Testar
k get pods
```

---

## 📖 Navegação

- [→ Próximo: Projetos](02-projetos.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
