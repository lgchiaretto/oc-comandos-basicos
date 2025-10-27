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
```bash
# Listar BuildConfigs
oc get buildconfig
oc get bc
```

```bash
# Exibir detalhes completos do buildconfig
# oc describe bc <buildconfig-name>
oc describe bc s2i-chiaretto
```

```bash ignore-test
# Editar BuildConfig
oc edit bc <nome-do-bc>
```

```bash ignore-test
# Deletar BuildConfig
oc delete bc <nome-do-bc>
```

```bash ignore-test
# Acompanhar logs em tempo real do pod
oc logs -f bc/s2i-chiaretto
```

### Triggers
```bash
# Adicionar webhook trigger
# oc set triggers <resource-name>/s2i-chiaretto --from-github
oc set triggers bc/s2i-chiaretto --from-github
# oc set triggers <resource-name>/s2i-chiaretto --from-webhook
oc set triggers bc/s2i-chiaretto --from-webhook
```

```bash
# Remover triggers
# oc set triggers <resource-name>/s2i-chiaretto --remove-all
oc set triggers bc/s2i-chiaretto --remove-all
```

```bash
# Exibir detalhes completos do buildconfig
# oc describe bc <buildconfig-name> | grep Triggered
oc describe bc s2i-chiaretto | grep Triggered
```

---

## Builds

### Executar e Monitorar
```bash
# Iniciar novo build
oc start-build s2i-chiaretto
```

```bash ignore-test
# Build de diretório local
oc start-build <nome-do-bc> --from-dir=.
```

```bash ignore-test
# Build de arquivo local
oc start-build <nome-do-bc> --from-file=Dockerfile
```

```bash
# Listar todos os builds do projeto
oc get builds
```

```bash ignore-test
# Ver status de build específico
# oc get build <build-name>
oc get build s2i-chiaretto-2
```

```bash ignore-test
# Cancelar build em execução
# oc cancel-build <build-name>
oc cancel-build s2i-chiaretto-2
```

```bash ignore-test
# Deletar o build especificado
# oc delete build <build-name>
oc delete build s2i-chiaretto-2
```

```bash
# Listar recurso ordenados por campo específico
oc get builds --sort-by=.metadata.creationTimestamp
```


## Gerenciamento de Builds

### Cancelar Build
```bash ignore-test
# Cancelar build em execução
# oc cancel-build <build-name>
oc cancel-build s2i-chiaretto-2
```

```bash ignore-test
# Em namespace específico
# oc cancel-build s2i-chiaretto -n <namespace>
oc cancel-build s2i-chiaretto -n development
```

### Logs de BuildConfig
```bash
# Exibir logs de todos os pods que correspondem ao label
oc logs -l buildconfig=s2i-chiaretto
```

```bash
# Exibir últimas N linhas dos logs
oc logs -l buildconfig=s2i-chiaretto --tail=20
```

```bash
# Exibir últimas N linhas dos logs
# oc logs -n <namespace> -l buildconfig=s2i-chiaretto --tail=20
oc logs -n development -l buildconfig=s2i-chiaretto --tail=20
```


### Debug de Builds
```bash ignore-test
# Exibir detalhes completos do build
# oc describe build <build-name>
oc describe build s2i-chiaretto-2
```

```bash ignore-test
# Listar eventos filtrados por campo específico
oc get events --field-selector involvedObject.name=s2i-chiaretto-2
```

```bash ignore-test
# Tentar build novamente
oc start-build --from-build=s2i-chiaretto-2
```

---

## ImageStreams

### Gerenciar ImageStreams
```bash
# Listar ImageStreams
oc get imagestream
oc get is
```

```bash
# Exibir detalhes completos do imagestream
# oc describe is <imagestream-name>
oc describe is s2i-chiaretto
```

```bash
# Exibir imagestream "s2i-chiaretto" em formato JSON
# oc get is <imagestream-name> -o jsonpath='{.spec.tags[*].name}'
oc get is s2i-chiaretto -o jsonpath='{.spec.tags[*].name}'
```

```bash ignore-test
# Criar novo recurso
# oc create imagestream <imagestream-name>
oc create imagestream s2i-chiaretto
```

```bash ignore-test
# Importar imagem externa
oc import-image s2i-chiaretto --from=<registry>/<image>:<tag> --confirm
```

```bash ignore-test
# Deletar o imagestream especificado
# oc delete is <imagestream-name>
oc delete is s2i-chiaretto
```

```bash ignore-test
# Exibir imagestream "s2i-chiaretto" em formato JSON
# oc get is <imagestream-name> -o jsonpath='{.status.tags[?(@.tag=="latest")].items[0].image}'
oc get is s2i-chiaretto -o jsonpath='{.status.tags[?(@.tag=="latest")].items[0].image}'
```

### ImageStreamTags
```bash
# Listar tags
oc get imagestreamtag
oc get istag
```

```bash ignore-test
# Exibir detalhes completos do recurso
# oc describe istag <istag-name>:<tag>
oc describe istag s2i-chiaretto:latest
```

```bash ignore-test
# Criar tag
oc tag <source-is>:<source-tag> <dest-is>:<dest-tag>
```

```bash ignore-test
# Tag de imagem externa
oc tag <external-image> <is>:<tag>
```

```bash ignore-test
# Deletar tag
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
