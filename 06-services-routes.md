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

# Descrever service
oc describe svc <nome-do-service>

# Criar service
oc expose deployment <nome-do-deployment> --port=<porta>

# Criar service com tipo específico
oc create service clusterip <nome> --tcp=<porta>:<porta-destino>

# Deletar service
oc delete svc <nome-do-service>

# Ver endpoints do service
oc get endpoints <nome-do-service>
```

---

## 🛣️ Routes

### Criar Routes
```bash
# Criar route a partir de service
oc expose service <nome-do-service>

# Com hostname específico
oc expose service <nome-do-service> --hostname=<hostname>

# Com path específico
oc expose service <nome-do-service> --path=/api

# Listar routes
oc get routes

# Descrever route
oc describe route <nome-da-route>

# Ver URL da route
oc get route <nome-da-route> -o jsonpath='{.spec.host}'
```

### Routes com TLS
```bash
# Criar route com TLS edge
oc create route edge <nome-da-route> --service=<nome-do-service>

# Route passthrough TLS
oc create route passthrough <nome-da-route> --service=<nome-do-service>

# Route reencrypt TLS
oc create route reencrypt <nome-da-route> --service=<nome-do-service>

# Com certificado customizado
oc create route edge <nome> --service=<svc> --cert=<cert-file> --key=<key-file>
```

### Gerenciar Routes
```bash
# Editar route
oc edit route <nome-da-route>

# Deletar route
oc delete route <nome-da-route>

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
