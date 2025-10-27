# Builds e ImageStreams

Este documento contém comandos para gerenciar builds e imagens no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [BuildConfigs](#buildconfigs)
3. [Builds](#builds)
4. [Gerenciamento de Builds](#gerenciamento-de-builds)
5. [ImageStreams](#imagestreams)
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## BuildConfigs

### Criar e Gerenciar
**Listar BuildConfigs**

```bash
oc get buildconfig
oc get bc
```

**Exibir detalhes completos do buildconfig**

**Exemplo:** `oc describe bc <buildconfig-name>`

```bash
oc describe bc s2i-chiaretto
```

**Editar BuildConfig**

```bash ignore-test
oc edit bc <nome-do-bc>
```

**Deletar BuildConfig**

```bash ignore-test
oc delete bc <nome-do-bc>
```

**Acompanhar logs em tempo real do pod**

```bash ignore-test
oc logs -f bc/s2i-chiaretto
```

### Triggers
**Adicionar webhook trigger**

**Exemplo:** `oc set triggers <resource-name>/s2i-chiaretto --from-github`
**oc set triggers <resource-name>/s2i-chiaretto --from-webhook**

```bash
oc set triggers bc/s2i-chiaretto --from-github
oc set triggers bc/s2i-chiaretto --from-webhook
```

**Remover triggers**

**Exemplo:** `oc set triggers <resource-name>/s2i-chiaretto --remove-all`

```bash
oc set triggers bc/s2i-chiaretto --remove-all
```

**Exibir detalhes completos do buildconfig**

**Exemplo:** `oc describe bc <buildconfig-name> | grep Triggered`

```bash
oc describe bc s2i-chiaretto | grep Triggered
```

---

## Builds

### Executar e Monitorar
**Iniciar novo build**

```bash
oc start-build s2i-chiaretto
```

**Build de diretório local**

```bash ignore-test
oc start-build <nome-do-bc> --from-dir=.
```

**Build de arquivo local**

```bash ignore-test
oc start-build <nome-do-bc> --from-file=Dockerfile
```

**Listar todos os builds do projeto**

```bash
oc get builds
```

**Ver status de build específico**

**Exemplo:** `oc get build <build-name>`

```bash ignore-test
oc get build s2i-chiaretto-2
```

**Cancelar build em execução**

**Exemplo:** `oc cancel-build <build-name>`

```bash ignore-test
oc cancel-build s2i-chiaretto-2
```

**Deletar o build especificado**

**Exemplo:** `oc delete build <build-name>`

```bash ignore-test
oc delete build s2i-chiaretto-2
```

**Listar recurso ordenados por campo específico**

```bash
oc get builds --sort-by=.metadata.creationTimestamp
```


## Gerenciamento de Builds

### Cancelar Build
**Cancelar build em execução**

**Exemplo:** `oc cancel-build <build-name>`

```bash ignore-test
oc cancel-build s2i-chiaretto-2
```

**Em namespace específico**

**Exemplo:** `oc cancel-build s2i-chiaretto -n <namespace>`

```bash ignore-test
oc cancel-build s2i-chiaretto -n development
```

### Logs de BuildConfig
**Exibir logs de todos os pods que correspondem ao label**

```bash
oc logs -l buildconfig=s2i-chiaretto
```

**Exibir últimas N linhas dos logs**

```bash
oc logs -l buildconfig=s2i-chiaretto --tail=20
```

**Exibir últimas N linhas dos logs**

**Exemplo:** `oc logs -n <namespace> -l buildconfig=s2i-chiaretto --tail=20`

```bash
oc logs -n development -l buildconfig=s2i-chiaretto --tail=20
```


### Debug de Builds
**Exibir detalhes completos do build**

**Exemplo:** `oc describe build <build-name>`

```bash ignore-test
oc describe build s2i-chiaretto-2
```

**Listar eventos filtrados por campo específico**

```bash ignore-test
oc get events --field-selector involvedObject.name=s2i-chiaretto-2
```

**Tentar build novamente**

```bash ignore-test
oc start-build --from-build=s2i-chiaretto-2
```

---

## ImageStreams

### Gerenciar ImageStreams
**Listar ImageStreams**

```bash
oc get imagestream
oc get is
```

**Exibir detalhes completos do imagestream**

**Exemplo:** `oc describe is <imagestream-name>`

```bash
oc describe is s2i-chiaretto
```

**Exibir imagestream "s2i-chiaretto" em formato JSON**

**Exemplo:** `oc get is <imagestream-name> -o jsonpath='{.spec.tags[*].name}'`

```bash
oc get is s2i-chiaretto -o jsonpath='{.spec.tags[*].name}'
```

**Criar novo recurso**

**Exemplo:** `oc create imagestream <imagestream-name>`

```bash ignore-test
oc create imagestream s2i-chiaretto
```

**Importar imagem externa**

```bash ignore-test
oc import-image s2i-chiaretto --from=<registry>/<image>:<tag> --confirm
```

**Deletar o imagestream especificado**

**Exemplo:** `oc delete is <imagestream-name>`

```bash ignore-test
oc delete is s2i-chiaretto
```

**Exibir imagestream "s2i-chiaretto" em formato JSON**

**Exemplo:** `oc get is <imagestream-name> -o jsonpath='{.status.tags[?(@.tag=="latest")].items[0].image}'`

```bash ignore-test
oc get is s2i-chiaretto -o jsonpath='{.status.tags[?(@.tag=="latest")].items[0].image}'
```

### ImageStreamTags
**Listar tags**

```bash
oc get imagestreamtag
oc get istag
```

**Exibir detalhes completos do recurso**

**Exemplo:** `oc describe istag <istag-name>:<tag>`

```bash ignore-test
oc describe istag s2i-chiaretto:latest
```

**Criar tag**

```bash ignore-test
oc tag <source-is>:<source-tag> <dest-is>:<dest-tag>
```

**Tag de imagem externa**

```bash ignore-test
oc tag <external-image> <is>:<tag>
```

**Deletar tag**

```bash ignore-test
oc delete istag s2i-chiaretto:<tag>
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications - Builds</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images">Images - Managing images</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications - Build configuration</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images">Images - ImageStreams</a>
---

---

## Navegação

- [← Anterior: Storage](08-storage.md)
- [→ Próximo: Registry](10-registry-imagens.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
