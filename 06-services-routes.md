# Services e Routes

Este documento contém comandos para gerenciar services e routes no OpenShift.

---

## Índice

- [Services e Routes](#services-e-routes)
  - [Índice](#índice)
  - [Services](#services)
    - [Básico](#básico)
  - [Investigação de Conectividade](#investigação-de-conectividade)
    - [Descrever Endpoints](#descrever-endpoints)
  - [Routes](#routes)
    - [Criar Routes](#criar-routes)
    - [Gerenciar Routes](#gerenciar-routes)
  - [Documentação Oficial](#documentação-oficial)
  - [Navegação](#navegação)
---

## Services

### Básico
**Listar todos os services do namespace atual**

```bash
oc get services
oc get svc
```

**Exibir detalhes completos do service**

```bash
oc describe svc test-app
```

**Criar service**

```bash ignore-test
oc expose deployment test-app --port=<porta>
```

**Criar service com tipo específico**

```bash ignore-test
oc create service clusterip test-app --tcp=<porta>:<porta-destino>
```

**Deletar o service especificado**

```bash ignore-test
oc delete svc test-app
```

**Ver endpoints do service**

```bash
oc get endpoints test-app
```

## Investigação de Conectividade


### Descrever Endpoints
**Exibir detalhes completos do endpoints**

```bash
oc describe endpoints test-app
```

**Exibir detalhes completos do endpoints**

```bash
oc describe endpoints test-app -n development
```

**Exemplo prático**

```bash
oc describe endpoints test-app -n development
```

---

## Routes

### Criar Routes
**Criar route para expor service externamente**

```bash ignore-test
oc expose service test-app
```

**Com hostname específico**

```bash ignore-test
oc expose service test-app --hostname=<hostname>
```

**Criar route com path específico para o service**

```bash ignore-test
oc expose service test-app --path=/api
```

**Criar route com terminação TLS edge (TLS terminado no router)**

```bash ignore-test
oc create route edge test-app --service=test-app
```

**Criar route passthrough (TLS vai direto ao pod)**

```bash ignore-test
oc create route passthrough test-app --service=test-app
```

**Criar route reencrypt (TLS terminado e re-encriptado)**

```bash ignore-test
oc create route reencrypt test-app --service=test-app
```

**Com certificado customizado**

```bash ignore-test
oc create route edge test-app --service=<svc> --cert=<cert-file> --key=<key-file>
```

**Listar todas as routes expostas no namespace**

```bash
oc get routes
```

**Exibir detalhes completos do route**

```bash
oc describe route test-app
```

**Exibir route "test-app" em formato JSON**

```bash
oc get route test-app -o jsonpath='{.spec.host}'
```

### Gerenciar Routes
**Abrir editor para modificar recurso interativamente**

```bash ignore-test
oc edit route test-app
```

**Deletar o route especificado**

```bash ignore-test
oc delete route test-app
```

**Listar routes com informações detalhadas**

```bash
oc get routes -o wide
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/configuring-ingress">Networking - Configuring ingress</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/configuring-routes">Networking - Configuring routes</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/understanding-networking">Networking - Understanding Services</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/configuring-routes#nw-ingress-creating-a-route-via-an-ingress_route-configuration">Secured routes</a>
---


## Navegação

- [← Anterior: Deployments](05-deployments-scaling.md)
- [→ Próximo: ConfigMaps e Secrets](07-configmaps-secrets.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
