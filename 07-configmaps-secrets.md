# ConfigMaps e Secrets

Este documento contém comandos para gerenciar ConfigMaps e Secrets no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [ConfigMaps](#configmaps)
3. [Secrets](#secrets)
4. [Usando em Pods](#usando-em-pods)
5. [Documentação Oficial](#documentação-oficial)
6. [Navegação](#navegação)
---

## ConfigMaps

### Criar ConfigMaps
**Ação:** Listar ConfigMaps
```

```bash
oc get configmaps
oc get cm
```

**Ação:** Criar novo recurso
**Exemplo:** `oc create configmap <configmap-name> --from-literal=chave=valor`
```

```bash
oc create configmap test-app --from-literal=chave=valor
```

**Ação:** De arquivo
```

```bash ignore-test
oc create configmap test-app --from-file=<arquivo>
```

**Ação:** De diretório
```

```bash ignore-test
oc create configmap test-app --from-file=<diretorio>/
```

**Ação:** Exibir configmap "test-app" em formato YAML
**Exemplo:** `oc get cm <configmap-name> -o yaml`
```

```bash
oc get cm test-app -o yaml
```

**Ação:** Abrir editor para modificar recurso interativamente
**Exemplo:** `oc edit cm <configmap-name>`
```

```bash ignore-test
oc edit cm test-app
```

**Ação:** Deletar o configmap especificado
**Exemplo:** `oc delete cm <configmap-name>`
```

```bash
oc delete cm test-app
```

### Exemplos Avançados
**Ação:** Criar novo configmap
**Exemplo:** `oc create cm <configmap-name>`
```

```bash
oc create cm test-app --from-literal=database.host=db.example.com --from-literal=database.port=5432
```

**Ação:** Exibir configmap "test-app" em formato JSON
**Exemplo:** `oc get cm <configmap-name> -o jsonpath='{.data}'`
```

```bash
oc get cm test-app -o jsonpath='{.data}'
```

---


### Descrever ConfigMap
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe configmap <configmap-name>`
```

```bash
oc describe configmap test-app
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe configmap <configmap-name> -n <namespace>`
```

```bash
oc describe configmap test-app -n development
```

**Ação:** Exemplo prático
**Exemplo:** `oc describe configmap <configmap-name> -n <namespace>`
```

```bash
oc describe configmap test-app -n development
```

## Secrets

### Criar Secrets
**Ação:** Criar novo secret
**Exemplo:** `oc create secret <secret-name> test-app --from-literal=chave=valor`
```

```bash
oc create secret generic test-app --from-literal=chave=valor
```

**Ação:** De arquivo
```

```bash ignore-test
oc create secret generic test-app --from-file=<arquivo>
```

**Ação:** Criar novo secret
**Exemplo:** `oc create secret <secret-name> test-app \`
```

```bash ignore-test
oc create secret docker-registry test-app \
  --docker-server=<registry> \
  --docker-username=<user> \
  --docker-password=<pass> \
  --docker-email=<email>
```

**Ação:** Secret TLS
```

```bash ignore-test
oc create secret tls test-app --cert=<cert-file> --key=<key-file>
```

**Ação:** Listar todos os secrets do namespace atual
```

```bash
oc get secrets
```

**Ação:** Exibir secret "test-app" em formato YAML
**Exemplo:** `oc get secret <secret-name> -o yaml`
```

```bash
oc get secret test-app -o yaml
```

**Ação:** Exibir secret "test-app" em formato JSON
**Exemplo:** `oc get secret <secret-name> -o jsonpath='{.data.chave}' | base64 -d`
```

```bash
oc get secret test-app -o jsonpath='{.data.chave}' | base64 -d
```

**Ação:** Abrir editor para modificar recurso interativamente
**Exemplo:** `oc edit secret <secret-name>`
```

```bash ignore-test
oc edit secret test-app
```

**Ação:** Deletar o secret especificado
**Exemplo:** `oc delete secret <secret-name>`
```

```bash ignore-test
oc delete secret test-app
```

### Descrever Secret
**Ação:** Exibir detalhes completos do secret
**Exemplo:** `oc describe secret <secret-name>`
```

```bash
oc describe secret test-app
```

**Ação:** Exibir detalhes completos do secret
**Exemplo:** `oc describe secret <secret-name> -n <namespace>`
```

```bash
oc describe secret test-app -n development
```

**Ação:** Exemplo prático
**Exemplo:** `oc describe secret <secret-name> -n <namespace>`
```

```bash
oc describe secret test-app -n development
```

### Link Secrets
**Ação:** Linkar secret à service account
```

```bash ignore-test
oc secrets link <service-account> <nome-do-secret>
```

**Ação:** Linkar para pull de imagens
```

```bash ignore-test
oc secrets link default <pull-secret> --for=pull
```

**Ação:** Linkar para mount
```

```bash ignore-test
oc secrets link <service-account> <nome-do-secret> --for=mount
```

---

## Usando em Pods

### Como Variáveis de Ambiente
**Ação:** Definir/atualizar variáveis de ambiente no recurso
**Exemplo:** `oc set env <resource-name>/test-app --from=configmap/test-app`
```

```bash
oc set env deployment/test-app --from=configmap/test-app
```

**Ação:** Definir/atualizar variáveis de ambiente no recurso
**Exemplo:** `oc set env <resource-name>/test-app --from=secret/test-app`
```

```bash
oc set env deployment/test-app --from=secret/test-app
```

**Ação:** Definir/atualizar variáveis de ambiente no recurso
**Exemplo:** `oc set env <resource-name>/test-app minhachave=valor --from=configmap/test-app`
```

```bash
oc set env deployment/test-app minhachave=valor --from=configmap/test-app
```

### Como Volumes
**Ação:** Patch deployment para montar ConfigMap
**Exemplo:** `oc set volume <resource-name>/test-app`
```

```bash
oc set volume --add --type=configmap deployment/test-app --configmap-name test-app --mount-path=/config
```

**Ação:** Montar Secret
**Exemplo:** `oc set volume <resource-name>/test-app`
```

```bash
oc set volume --add --type=secret deployment/test-app --secret-name test-app --mount-path=/test-app-secret
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes - ConfigMaps and Secrets</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/working-with-pods">Nodes - Working with pods</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance">Security and compliance</a>
---

---

## Navegação

- [← Anterior: Services e Routes](06-services-routes.md)
- [→ Próximo: Storage](08-storage.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025

