# 🏗️ Builds e ImageStreams

Este documento contém comandos para gerenciar builds e imagens no OpenShift.

---

## 📋 Índice

1. [BuildConfigs](#buildconfigs)
2. [Builds](#builds)
3. [ImageStreams](#imagestreams)
4. [ImageStreamTags](#imagestreamtags)

---

## 🔧 BuildConfigs

### Criar e Gerenciar
```bash
# Listar BuildConfigs
oc get buildconfig
oc get bc
```

```bash
# Descrever BuildConfig
oc describe bc <nome-do-bc>
```

```bash
# Criar build a partir de código Git
oc new-build <url-do-git>
```

```bash
# Com estratégia específica
oc new-build <url-do-git> --strategy=docker
oc new-build <url-do-git> --strategy=source
```

```bash
# Editar BuildConfig
oc edit bc <nome-do-bc>
```

```bash
# Deletar BuildConfig
oc delete bc <nome-do-bc>
```

```bash
# Ver logs do último build
oc logs -f bc/<nome-do-bc>
```

### Triggers
```bash
# Adicionar webhook trigger
oc set triggers bc/<nome> --from-github
oc set triggers bc/<nome> --from-webhook
```

```bash
# Remover triggers
oc set triggers bc/<nome> --remove-all
```

```bash
# Ver triggers
oc describe bc <nome> | grep Triggered
```

---

## 🏭 Builds

### Executar e Monitorar
```bash
# Iniciar novo build
oc start-build <nome-do-bc>
```

```bash
# Build de diretório local
oc start-build <nome-do-bc> --from-dir=.
```

```bash
# Build de arquivo local
oc start-build <nome-do-bc> --from-file=Dockerfile
```

```bash
# Listar builds
oc get builds
```

```bash
# Ver status de build específico
oc get build <nome-do-build>
```

```bash
# Ver logs do build
oc logs build/<nome-do-build>
oc logs -f build/<nome-do-build>
```

```bash
# Cancelar build em execução
oc cancel-build <nome-do-build>
```

```bash
# Deletar build
oc delete build <nome-do-build>
```

```bash
# Ver histórico de builds
oc get builds --sort-by=.metadata.creationTimestamp
```


## 🔧 Gerenciamento de Builds


### Criar BuildConfig
```bash
# Criar BuildConfig binário
oc new-build --name=<nome> --binary
```

```bash
# Em namespace específico
oc new-build --name=<nome> --binary -n development
```

```bash
# Exemplo prático
oc new-build --name=test-build --binary -n meu-projeto
```
### Cancelar Build
```bash
# Cancelar build em execução
oc cancel-build <nome-do-build>
```

```bash
# Em namespace específico
oc cancel-build <nome> -n development
```

```bash
# Exemplo prático
oc cancel-build test-app-1 -n meu-projeto
```

### Logs de BuildConfig
```bash
# Ver logs de builds por label buildconfig
oc logs -l buildconfig=<nome>
```

```bash
# Com limite de linhas
oc logs -l buildconfig=<nome> --tail=20
```

```bash
# Em namespace específico
oc logs -n development -l buildconfig=<nome> --tail=20
```

```bash
# Exemplo prático
oc logs -n meu-projeto -l buildconfig=test-app --tail=20
```


### Debug de Builds
```bash
# Ver por que build falhou
oc describe build <nome-do-build>
```

```bash
# Ver eventos relacionados ao build
oc get events --field-selector involvedObject.name=<nome-do-build>
```

```bash
# Tentar build novamente
oc start-build --from-build=<nome-do-build>
```

---

## 🖼️ ImageStreams

### Gerenciar ImageStreams
```bash
# Listar ImageStreams
oc get imagestream
oc get is
```

```bash
# Descrever ImageStream
oc describe is <nome-do-is>
```

```bash
# Ver tags disponíveis
oc get is <nome-do-is> -o jsonpath='{.spec.tags[*].name}'
```

```bash
# Criar ImageStream
oc create imagestream <nome>
```

```bash
# Importar imagem externa
oc import-image <nome> --from=<registry>/<image>:<tag> --confirm
```

```bash
# Deletar ImageStream
oc delete is <nome-do-is>
```

```bash
# Ver SHA da imagem
oc get is <nome> -o jsonpath='{.status.tags[?(@.tag=="latest")].items[0].image}'
```

### ImageStreamTags
```bash
# Listar tags
oc get imagestreamtag
oc get istag
```

```bash
# Ver detalhes de tag específica
oc describe istag <nome-do-is>:<tag>
```

```bash
# Criar tag
oc tag <source-is>:<source-tag> <dest-is>:<dest-tag>
```

```bash
# Tag de imagem externa
oc tag <external-image> <is>:<tag>
```

```bash
# Deletar tag
oc delete istag <nome-do-is>:<tag>
```

---

## 📖 Navegação

- [← Anterior: Storage](08-storage.md)
- [→ Próximo: Registry](10-registry-imagens.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
