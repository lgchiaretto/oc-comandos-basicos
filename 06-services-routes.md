# Services e Routes

Este documento contém comandos para gerenciar services e routes no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Services](#services)
3. [Investigação de Conectividade](#investigação-de-conectividade)
4. [Routes](#routes)
5. [Documentação Oficial](#documentação-oficial)
6. [Navegação](#navegação)
---

## Services

### Básico
```bash
# Listar todos os services do namespace atual
oc get services
oc get svc
```

```bash
# Exibir detalhes completos do service
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
# Deletar o service especificado
# oc delete svc <service-name>
oc delete svc test-app
```

```bash
# Ver endpoints do service
# oc get endpoints <resource-name>
oc get endpoints test-app
```

## Investigação de Conectividade


### Descrever Endpoints
```bash
# Exibir detalhes completos do endpoints
# oc describe endpoints <resource-name>
oc describe endpoints test-app
```

```bash
# Exibir detalhes completos do endpoints
# oc describe endpoints <resource-name>app -n <namespace>
oc describe endpoints test-app -n development
```

```bash
# Exemplo prático
# oc describe endpoints <resource-name>app -n <namespace>
oc describe endpoints test-app -n development
```

---

## Routes

### Criar Routes
```bash ignore-test
# Criar route para expor service externamente
# oc expose service <service-name>
oc expose service test-app
```

```bash ignore-test
# Com hostname específico
oc expose service test-app --hostname=<hostname>
```

```bash ignore-test
# Criar route com path específico para o service
# oc expose service <service-name> --path=/api
oc expose service test-app --path=/api
```

```bash ignore-test
# Criar route com terminação TLS edge (TLS terminado no router)
# oc create route <route-name> test-app --service=test-app
oc create route edge test-app --service=test-app
```

```bash ignore-test
# Criar route passthrough (TLS vai direto ao pod)
# oc create route <route-name> test-app --service=test-app
oc create route passthrough test-app --service=test-app
```

```bash ignore-test
# Criar route reencrypt (TLS terminado e re-encriptado)
# oc create route <route-name> test-app --service=test-app
oc create route reencrypt test-app --service=test-app
```

```bash ignore-test
# Com certificado customizado
oc create route edge test-app --service=<svc> --cert=<cert-file> --key=<key-file>
```

```bash
# Listar todas as routes expostas no namespace
oc get routes
```

```bash
# Exibir detalhes completos do route
# oc describe route <route-name>
oc describe route test-app
```

```bash
# Exibir route "test-app" em formato JSON
# oc get route <route-name> -o jsonpath='{.spec.host}'
oc get route test-app -o jsonpath='{.spec.host}'
```

### Gerenciar Routes
```bash ignore-test
# Abrir editor para modificar recurso interativamente
# oc edit route <route-name>
oc edit route test-app
```

```bash ignore-test
# Deletar o route especificado
# oc delete route <route-name>
oc delete route test-app
```

```bash
# Listar routes com informações detalhadas
oc get routes -o wide
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/configuring-ingress">Networking - Configuring ingress</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/configuring-routes">Networking - Configuring routes</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/understanding-networking">Networking - Understanding Services</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/configuring-routes#nw-ingress-creating-a-route-via-an-ingress_route-configuration">Secured routes</a>
---

---

## Navegação

- [← Anterior: Deployments](05-deployments-scaling.md)
- [→ Próximo: ConfigMaps e Secrets](07-configmaps-secrets.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
