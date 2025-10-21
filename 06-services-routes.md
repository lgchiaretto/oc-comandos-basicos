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
oc describe svc test-app
```

```bash
# Criar service
oc expose deployment test-app --port=<porta>
```

```bash
# Criar service com tipo específico
oc create service clusterip test-app --tcp=<porta>:<porta-destino>
```

```bash
# Deletar service
oc delete svc test-app
```

```bash
# Ver endpoints do service
oc get endpoints test-app
```

## 🔍 Investigação de Conectividade


### Descrever Endpoints
```bash
# Ver detalhes dos endpoints de um service
oc describe endpoints test-app
```

```bash
# Em namespace específico
oc describe endpoints test-app -n development
```

```bash
# Exemplo prático
oc describe endpoints test-app -n development
```

---

## 🛣️ Routes

### Criar Routes
```bash
# Criar route a partir de service
oc expose service test-app
```

```bash
# Com hostname específico
oc expose service test-app --hostname=<hostname>
```

```bash
# Com path específico
oc expose service test-app --path=/api
```

```bash
# Listar routes
oc get routes
```

```bash
# Descrever route
oc describe route test-app>
```

```bash
# Ver URL da route
oc get route test-app> -o jsonpath='{.spec.host}'
```

### Routes com TLS
```bash
# Criar route com TLS edge
oc create route edge test-app> --service=test-app
```

```bash
# Route passthrough TLS
oc create route passthrough test-app> --service=test-app
```

```bash
# Route reencrypt TLS
oc create route reencrypt test-app> --service=test-app
```

```bash
# Com certificado customizado
oc create route edge test-app --service=<svc> --cert=<cert-file> --key=<key-file>
```

### Gerenciar Routes
```bash
# Editar route
oc edit route test-app>
```

```bash
# Deletar route
oc delete route test-app>
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
