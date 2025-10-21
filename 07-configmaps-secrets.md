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
```

```bash
# De literal
oc create configmap test-app --from-literal=<chave>=<valor>
```

```bash
# De arquivo
oc create configmap test-app --from-file=<arquivo>
```

```bash
# De diretório
oc create configmap test-app --from-file=<diretorio>/
```

```bash
# Ver conteúdo
oc get cm test-app -o yaml
```

```bash
# Editar ConfigMap
oc edit cm test-app
```

```bash
# Deletar ConfigMap
oc delete cm test-app
```

### Descrever ConfigMap
```bash
# Ver detalhes de um ConfigMap
oc describe configmap test-app
```

```bash
# Em namespace específico
oc describe configmap test-app -n development
```

```bash
# Exemplo prático
oc describe configmap test-config -n development
```

### Exemplos Avançados
```bash
# Múltiplos valores literais
oc create cm app-config \
  --from-literal=database.host=db.example.com \
  --from-literal=database.port=5432
```

```bash
# Ver apenas as chaves
oc get cm test-app -o jsonpath='{.data}'
```

---

## 🔒 Secrets

### Criar Secrets
```bash
# Secret genérico
oc create secret generic test-app --from-literal=<chave>=<valor>
```

```bash
# De arquivo
oc create secret generic test-app --from-file=<arquivo>
```

```bash
# Secret para Docker Registry
oc create secret docker-registry test-app \
  --docker-server=<registry> \
  --docker-username=<user> \
  --docker-password=<pass> \
  --docker-email=<email>
```

```bash
# Secret TLS
oc create secret tls test-app --cert=<cert-file> --key=<key-file>
```

```bash
# Listar secrets
oc get secrets
```

```bash
# Ver secret (dados base64)
oc get secret test-app -o yaml
```

```bash
# Decodificar secret
oc get secret test-app -o jsonpath='{.data.<chave>}' | base64 -d
```

```bash
# Editar secret
oc edit secret test-app
```

```bash
# Deletar secret
oc delete secret test-app
```

### Descrever Secret
```bash
# Ver detalhes de um Secret
oc describe secret test-app
```

```bash
# Em namespace específico
oc describe secret test-app -n development
```

```bash
# Exemplo prático
oc describe secret test-secret -n development
```

### Link Secrets
```bash
# Linkar secret à service account
oc secrets link <service-account> <nome-do-secret>
```

```bash
# Linkar para pull de imagens
oc secrets link default <pull-secret> --for=pull
```

```bash
# Linkar para mount
oc secrets link <service-account> <nome-do-secret> --for=mount
```

---

## 🎯 Usando em Pods

### Como Variáveis de Ambiente
```bash
# ConfigMap
oc set env deployment/test-app --from=configmap/<nome-cm>
```

```bash
# Secret
oc set env deployment/test-app --from=secret/<nome-secret>
```

```bash
# Chave específica
oc set env deployment/test-app CHAVE=valor --from=configmap/<nome-cm>
```

### Como Volumes
```bash
# Patch deployment para montar ConfigMap
oc set volume deployment/test-app \
  --add --name=config-vol \
  --type=configmap \
  --configmap-name=<nome-cm> \
  --mount-path=/etc/config
```

```bash
# Montar Secret
oc set volume deployment/test-app \
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

