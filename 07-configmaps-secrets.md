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
# oc create configmap <configmap-name> --from-literal=chave=valor
oc create configmap test-app --from-literal=chave=valor
```

```bash ignore-test
# De arquivo
oc create configmap test-app --from-file=<arquivo>
```

```bash ignore-test
# De diretório
oc create configmap test-app --from-file=<diretorio>/
```

```bash
# Ver conteúdo
# oc get cm <configmap-name> -o yaml
oc get cm test-app -o yaml
```

```bash ignore-test
# Editar ConfigMap
# oc edit cm <configmap-name>
oc edit cm test-app
```

```bash
# Deletar ConfigMap
# oc delete cm <configmap-name>
oc delete cm test-app
```

### Exemplos Avançados
```bash
# Múltiplos valores literais
# oc create cm <configmap-name>
oc create cm test-app --from-literal=database.host=db.example.com --from-literal=database.port=5432
```

```bash
# Ver apenas as chaves
# oc get cm <configmap-name> -o jsonpath='{.data}'
oc get cm test-app -o jsonpath='{.data}'
```

---


### Descrever ConfigMap
```bash
# Ver detalhes de um ConfigMap
# oc describe configmap <configmap-name>
oc describe configmap test-app
```

```bash
# Em namespace específico
# oc describe configmap <configmap-name> -n <namespace>
oc describe configmap test-app -n development
```

```bash
# Exemplo prático
# oc describe configmap <configmap-name> -n <namespace>
oc describe configmap test-app -n development
```

## 🔒 Secrets

### Criar Secrets
```bash
# Secret genérico
# oc create secret <secret-name> test-app --from-literal=chave=valor
oc create secret generic test-app --from-literal=chave=valor
```

```bash ignore-test
# De arquivo
oc create secret generic test-app --from-file=<arquivo>
```

```bash ignore-test
# Secret para Docker Registry
# oc create secret <secret-name> test-app \
oc create secret docker-registry test-app \
  --docker-server=<registry> \
  --docker-username=<user> \
  --docker-password=<pass> \
  --docker-email=<email>
```

```bash ignore-test
# Secret TLS
oc create secret tls test-app --cert=<cert-file> --key=<key-file>
```

```bash
# Listar secrets
oc get secrets
```

```bash
# Ver secret (dados base64)
# oc get secret <secret-name> -o yaml
oc get secret test-app -o yaml
```

```bash
# Decodificar secret
# oc get secret <secret-name> -o jsonpath='{.data.chave}' | base64 -d
oc get secret test-app -o jsonpath='{.data.chave}' | base64 -d
```

```bash ignore-test
# Editar secret
# oc edit secret <secret-name>
oc edit secret test-app
```

```bash ignore-test
# Deletar secret
# oc delete secret <secret-name>
oc delete secret test-app
```

### Descrever Secret
```bash
# Ver detalhes de um Secret
# oc describe secret <secret-name>
oc describe secret test-app
```

```bash
# Em namespace específico
# oc describe secret <secret-name> -n <namespace>
oc describe secret test-app -n development
```

```bash
# Exemplo prático
# oc describe secret <secret-name> -n <namespace>
oc describe secret test-secret -n development
```

### Link Secrets
```bash ignore-test
# Linkar secret à service account
oc secrets link <service-account> <nome-do-secret>
```

```bash ignore-test
# Linkar para pull de imagens
oc secrets link default <pull-secret> --for=pull
```

```bash ignore-test
# Linkar para mount
oc secrets link <service-account> <nome-do-secret> --for=mount
```

---

## 🎯 Usando em Pods

### Como Variáveis de Ambiente
```bash
# ConfigMap
# oc set env <resource-name>/test-app --from=configmap/test-app
oc set env deployment/test-app --from=configmap/test-app
```

```bash
# Secret
# oc set env <resource-name>/test-app --from=secret/test-app
oc set env deployment/test-app --from=secret/test-app
```

```bash
# Chave específica
# oc set env <resource-name>/test-app minhachave=valor --from=configmap/test-app
oc set env deployment/test-app minhachave=valor --from=configmap/test-app
```

### Como Volumes
```bash
# Patch deployment para montar ConfigMap
# oc set volume <resource-name>/test-app
oc set volume --add --type=configmap deployment/test-app --configmap-name test-app --mount-path=/config
```

```bash
# Montar Secret
# oc set volume <resource-name>/test-app
oc set volume --add --type=secret deployment/test-app --secret-name test-app --mount-path=/test-app-secret
```

---

## 📖 Navegação

- [← Anterior: Services e Routes](06-services-routes.md)
- [→ Próximo: Storage](08-storage.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025

