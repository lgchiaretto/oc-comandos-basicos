# 🔐 ConfigMaps e Secrets

Este documento contém comandos para gerenciar ConfigMaps e Secrets no OpenShift.

---

## 📋 Índice

1. [ConfigMaps](#configmaps)
2. [Secrets](#secrets)
3. [Usando em Pods](#usando-em-pods)

---

## 📝 ConfigMaps

### Criar ConfigMaps
```bash
# Listar ConfigMaps
oc get configmaps
oc get cm

# De literal
oc create configmap <nome> --from-literal=<chave>=<valor>

# De arquivo
oc create configmap <nome> --from-file=<arquivo>

# De diretório
oc create configmap <nome> --from-file=<diretorio>/

# Ver conteúdo
oc get cm <nome> -o yaml

# Editar ConfigMap
oc edit cm <nome>

# Deletar ConfigMap
oc delete cm <nome>
```

### Descrever ConfigMap
```bash
# Ver detalhes de um ConfigMap
oc describe configmap <nome>

# Em namespace específico
oc describe configmap <nome> -n <nome-do-projeto>

# Exemplo prático
oc describe configmap test-config -n meu-projeto
```

### Exemplos Avançados
```bash
# Múltiplos valores literais
oc create cm app-config \
  --from-literal=database.host=db.example.com \
  --from-literal=database.port=5432

# Ver apenas as chaves
oc get cm <nome> -o jsonpath='{.data}'
```

---

## 🔒 Secrets

### Criar Secrets
```bash
# Secret genérico
oc create secret generic <nome> --from-literal=<chave>=<valor>

# De arquivo
oc create secret generic <nome> --from-file=<arquivo>

# Secret para Docker Registry
oc create secret docker-registry <nome> \
  --docker-server=<registry> \
  --docker-username=<user> \
  --docker-password=<pass> \
  --docker-email=<email>

# Secret TLS
oc create secret tls <nome> --cert=<cert-file> --key=<key-file>

# Listar secrets
oc get secrets

# Ver secret (dados base64)
oc get secret <nome> -o yaml

# Decodificar secret
oc get secret <nome> -o jsonpath='{.data.<chave>}' | base64 -d

# Editar secret
oc edit secret <nome>

# Deletar secret
oc delete secret <nome>
```

### Descrever Secret
```bash
# Ver detalhes de um Secret
oc describe secret <nome>

# Em namespace específico
oc describe secret <nome> -n <nome-do-projeto>

# Exemplo prático
oc describe secret test-secret -n meu-projeto
```

### Link Secrets
```bash
# Linkar secret à service account
oc secrets link <service-account> <nome-do-secret>

# Linkar para pull de imagens
oc secrets link default <pull-secret> --for=pull

# Linkar para mount
oc secrets link <service-account> <nome-do-secret> --for=mount
```

---

## 🎯 Usando em Pods

### Como Variáveis de Ambiente
```bash
# ConfigMap
oc set env deployment/<nome> --from=configmap/<nome-cm>

# Secret
oc set env deployment/<nome> --from=secret/<nome-secret>

# Chave específica
oc set env deployment/<nome> CHAVE=valor --from=configmap/<nome-cm>
```

### Como Volumes
```bash
# Patch deployment para montar ConfigMap
oc set volume deployment/<nome> \
  --add --name=config-vol \
  --type=configmap \
  --configmap-name=<nome-cm> \
  --mount-path=/etc/config

# Montar Secret
oc set volume deployment/<nome> \
  --add --name=secret-vol \
  --type=secret \
  --secret-name=<nome-secret> \
  --mount-path=/etc/secret
```

---

## 📖 Navegação

- [← Anterior: Services e Routes](06-services-routes.md)
- [→ Próximo: Storage](08-storage.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025

