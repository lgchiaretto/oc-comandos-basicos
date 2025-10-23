# 🌐 Services e Routes

Este documento contém comandos para gerenciar services e routes no OpenShift.

---

## 📋 Índice

1. [Services](#services)
2. [Routes](#routes)
3. [TLS e Certificados](#tls-e-certificados)
4. [Endpoints](#endpoints)

---

## 🔌 Services

### Básico
```bash
# Listar services
oc get services
oc get svc
```

```bash
# Descrever service
# oc describe svc <service-name>
oc describe svc test-app
```

```bash ignore-test
# Criar service
oc expose deployment test-app --port=<porta>
```

```bash ignore-test
# Criar service com tipo específico
oc create service clusterip test-app --tcp=<porta>:<porta-destino>
```

```bash ignore-test
# Deletar service
# oc delete svc <service-name>
oc delete svc test-app
```

```bash
# Ver endpoints do service
# oc get endpoints <resource-name>
oc get endpoints test-app
```

## 🔍 Investigação de Conectividade


### Descrever Endpoints
```bash
# Ver detalhes dos endpoints de um service
# oc describe endpoints <resource-name>
oc describe endpoints test-app
```

```bash
# Em namespace específico
# oc describe endpoints <resource-name>app -n <namespace>
oc describe endpoints test-app -n development
```

```bash
# Exemplo prático
# oc describe endpoints <resource-name>app -n <namespace>
oc describe endpoints test-app -n development
```

---

## 🛣️ Routes

### Criar Routes
```bash ignore-test
# Criar route a partir de service
# oc expose service <service-name>
oc expose service test-app
```

```bash ignore-test
# Com hostname específico
oc expose service test-app --hostname=<hostname>
```

```bash ignore-test
# Com path específico
# oc expose service <service-name> --path=/api
oc expose service test-app --path=/api
```

```bash ignore-test
# Criar route com TLS edge
# oc create route <route-name> test-app --service=test-app
oc create route edge test-app --service=test-app
```

```bash ignore-test
# Route passthrough TLS
# oc create route <route-name> test-app --service=test-app
oc create route passthrough test-app --service=test-app
```

```bash ignore-test
# Route reencrypt TLS
# oc create route <route-name> test-app --service=test-app
oc create route reencrypt test-app --service=test-app
```

```bash ignore-test
# Com certificado customizado
oc create route edge test-app --service=<svc> --cert=<cert-file> --key=<key-file>
```

```bash
# Listar routes
oc get routes
```

```bash
# Descrever route
# oc describe route <route-name>
oc describe route test-app
```

```bash
# Ver URL da route
# oc get route <route-name> -o jsonpath='{.spec.host}'
oc get route test-app -o jsonpath='{.spec.host}'
```

### Gerenciar Routes
```bash ignore-test
# Editar route
# oc edit route <route-name>
oc edit route test-app
```

```bash ignore-test
# Deletar route
# oc delete route <route-name>
oc delete route test-app
```

```bash
# Ver routes em formato wide
oc get routes -o wide
```

---

## 📖 Navegação

- [← Anterior: Deployments](05-deployments-scaling.md)
- [→ Próximo: ConfigMaps e Secrets](07-configmaps-secrets.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
