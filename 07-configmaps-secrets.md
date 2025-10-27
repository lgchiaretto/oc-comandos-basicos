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
**Listar ConfigMaps**

```bash
oc get configmaps
oc get cm
```

**Criar novo recurso**

**Exemplo:** `oc create configmap <configmap-name> --from-literal=chave=valor`

```bash
oc create configmap test-app --from-literal=chave=valor
```

**De arquivo**

```bash ignore-test
oc create configmap test-app --from-file=<arquivo>
```

**De diretório**

```bash ignore-test
oc create configmap test-app --from-file=<diretorio>/
```

**Exibir configmap "test-app" em formato YAML**

**Exemplo:** `oc get cm <configmap-name> -o yaml`

```bash
oc get cm test-app -o yaml
```

**Abrir editor para modificar recurso interativamente**

**Exemplo:** `oc edit cm <configmap-name>`

```bash ignore-test
oc edit cm test-app
```

**Deletar o configmap especificado**

**Exemplo:** `oc delete cm <configmap-name>`

```bash
oc delete cm test-app
```

### Exemplos Avançados
**Criar novo configmap**

**Exemplo:** `oc create cm <configmap-name>`

```bash
oc create cm test-app --from-literal=database.host=db.example.com --from-literal=database.port=5432
```

**Exibir configmap "test-app" em formato JSON**

**Exemplo:** `oc get cm <configmap-name> -o jsonpath='{.data}'`

```bash
oc get cm test-app -o jsonpath='{.data}'
```

---


### Descrever ConfigMap
**Exibir detalhes completos do recurso**

**Exemplo:** `oc describe configmap <configmap-name>`

```bash
oc describe configmap test-app
```

**Exibir detalhes completos do recurso**

**Exemplo:** `oc describe configmap <configmap-name> -n <namespace>`

```bash
oc describe configmap test-app -n development
```

**Exemplo prático**

**Exemplo:** `oc describe configmap <configmap-name> -n <namespace>`

```bash
oc describe configmap test-app -n development
```

## Secrets

### Criar Secrets
**Criar novo secret**

**Exemplo:** `oc create secret <secret-name> test-app --from-literal=chave=valor`

```bash
oc create secret generic test-app --from-literal=chave=valor
```

**De arquivo**

```bash ignore-test
oc create secret generic test-app --from-file=<arquivo>
```

**Criar novo secret**

**Exemplo:** `oc create secret <secret-name> test-app \`

```bash ignore-test
oc create secret docker-registry test-app \
  --docker-server=<registry> \
  --docker-username=<user> \
  --docker-password=<pass> \
  --docker-email=<email>
```

**Secret TLS**

```bash ignore-test
oc create secret tls test-app --cert=<cert-file> --key=<key-file>
```

**Listar todos os secrets do namespace atual**

```bash
oc get secrets
```

**Exibir secret "test-app" em formato YAML**

**Exemplo:** `oc get secret <secret-name> -o yaml`

```bash
oc get secret test-app -o yaml
```

**Exibir secret "test-app" em formato JSON**

**Exemplo:** `oc get secret <secret-name> -o jsonpath='{.data.chave}' | base64 -d`

```bash
oc get secret test-app -o jsonpath='{.data.chave}' | base64 -d
```

**Abrir editor para modificar recurso interativamente**

**Exemplo:** `oc edit secret <secret-name>`

```bash ignore-test
oc edit secret test-app
```

**Deletar o secret especificado**

**Exemplo:** `oc delete secret <secret-name>`

```bash ignore-test
oc delete secret test-app
```

### Descrever Secret
**Exibir detalhes completos do secret**

**Exemplo:** `oc describe secret <secret-name>`

```bash
oc describe secret test-app
```

**Exibir detalhes completos do secret**

**Exemplo:** `oc describe secret <secret-name> -n <namespace>`

```bash
oc describe secret test-app -n development
```

**Exemplo prático**

**Exemplo:** `oc describe secret <secret-name> -n <namespace>`

```bash
oc describe secret test-app -n development
```

### Link Secrets
**Linkar secret à service account**

```bash ignore-test
oc secrets link <service-account> <nome-do-secret>
```

**Linkar para pull de imagens**

```bash ignore-test
oc secrets link default <pull-secret> --for=pull
```

**Linkar para mount**

```bash ignore-test
oc secrets link <service-account> <nome-do-secret> --for=mount
```

---

## Usando em Pods

### Como Variáveis de Ambiente
**Definir/atualizar variáveis de ambiente no recurso**

**Exemplo:** `oc set env <resource-name>/test-app --from=configmap/test-app`

```bash
oc set env deployment/test-app --from=configmap/test-app
```

**Definir/atualizar variáveis de ambiente no recurso**

**Exemplo:** `oc set env <resource-name>/test-app --from=secret/test-app`

```bash
oc set env deployment/test-app --from=secret/test-app
```

**Definir/atualizar variáveis de ambiente no recurso**

**Exemplo:** `oc set env <resource-name>/test-app minhachave=valor --from=configmap/test-app`

```bash
oc set env deployment/test-app minhachave=valor --from=configmap/test-app
```

### Como Volumes
**Patch deployment para montar ConfigMap**

**Exemplo:** `oc set volume <resource-name>/test-app`

```bash
oc set volume --add --type=configmap deployment/test-app --configmap-name test-app --mount-path=/config
```

**Montar Secret**

**Exemplo:** `oc set volume <resource-name>/test-app`

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

