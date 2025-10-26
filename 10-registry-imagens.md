# Registry e Gestão de Imagens

Este documento contém comandos para gerenciar o registry interno e imagens no OpenShift.

---

## Índice

1. [Registry Interno](#registry-interno)
2. [Push e Pull de Imagens](#push-e-pull-de-imagens)
3. [Image Mirroring](#image-mirroring)
4. [Image Pruning](#image-pruning)
---

## Registry Interno

### Acessar Registry
```bash
# Ver URL do registry interno
oc get route -n openshift-image-registry
```

```bash
# Ver info do registry
oc get configs.imageregistry.operator.openshift.io/cluster -o yaml
```

```bash
# Ver status do registry
# oc get clusteroperator <resource-name>
oc get clusteroperator image-registry
```

### Configurar Registry
```bash
# Expor registry externamente
oc patch configs.imageregistry.operator.openshift.io/cluster --type merge -p '{"spec":{"defaultRoute":true}}'
```

```bash
# Ver route criada
oc get route -n openshift-image-registry
```

```bash
# Configurar storage para registry
oc patch configs.imageregistry.operator.openshift.io/cluster --type merge -p '{"spec":{"storage":{"pvc":{"claim":""}}}}'
```

---

## Push e Pull de Imagens

### Push de Imagens
```bash ignore-test
# Tag para registry interno
docker tag <imagem-local> <registry-interno>/<projeto>/test-app:<tag>
```

```bash ignore-test
# Push para registry interno
docker push <registry-interno>/<projeto>/test-app:<tag>
```

```bash ignore-test
# Usando Podman
podman push <imagem> <registry-interno>/<projeto>/test-app:<tag>
```

```bash ignore-test
# Criar secret para registry externo
oc create secret docker-registry <secret-name> \
  --docker-server=<registry-url> \
  --docker-username=<user> \
  --docker-password=<pass>
```

```bash ignore-test
# Linkar secret para pull
oc secrets link default <secret-name> --for=pull
```

### Pull de Imagens
```bash ignore-test
# Pull de registry interno
docker pull <registry-interno>/<projeto>/test-app:<tag>
```

```bash
# Ver imagens disponíveis em ImageStream
# oc get is <imagestream-name> -o yaml
oc get is s2i-chiaretto -o yaml
```

```bash ignore-test
# Importar imagem externa
oc import-image test-app:<tag> --from=<registry-externo>/<image>:<tag> --confirm
```

---

## Image Mirroring

### Configurar Mirroring
```bash
# Ver ImageContentSourcePolicy
oc get imagecontentsourcepolicy
```

```bash ignore-test
# Criar ICSP para mirror
cat <<EOF | oc apply -f -
apiVersion: operator.openshift.io/v1alpha1
kind: ImageContentSourcePolicy
metadata:
  name: mirror-config
spec:
  repositoryDigestMirrors:
  - mirrors:
    - <mirror-registry>/<repo>
    source: <original-registry>/<repo>
EOF
```

```bash
# Ver configuração de mirror
oc get imagecontentsourcepolicy -o yaml
```

### Mirror com oc-mirror
```bash ignore-test
# Mirror de operator catalogs
oc mirror --config=imageset-config.yaml docker://<mirror-registry>
```

```bash ignore-test
# Ver resultados do mirror
oc mirror list operators --catalog=<catalog-image>
```

---

## Image Pruning

### Limpeza de Imagens
```bash ignore-test
# Executar image pruner manual
oc adm prune images --confirm
```

```bash ignore-test
# Dry-run (sem deletar)
# oc adm prune <resource-name>
oc adm prune images
```

```bash ignore-test
# Prune de imagens antigas
oc adm prune images --keep-tag-revisions=3 --keep-younger-than=60m --confirm
```

```bash
# Ver configuração de pruner automático
oc get imagepruner/cluster -o yaml
```

```bash
# Configurar pruner automático
oc patch imagepruners.imageregistry.operator.openshift.io/cluster --type merge -p '{"spec":{"schedule":"0 0 * * *","suspend":false,"keepTagRevisions":3}}'
```

```bash
# Ver jobs de pruning
oc get jobs -n openshift-image-registry
```

### Limpeza de Builds
```bash ignore-test
# Prune de builds antigos
oc adm prune builds --confirm
```

```bash ignore-test
# Manter apenas N builds
oc adm prune builds --keep-complete=5 --keep-failed=1 --confirm
```

```bash ignore-test
# Prune por idade
oc adm prune builds --keep-younger-than=48h --confirm
```


## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/registry" target="_blank">Registry - Integrated OpenShift image registry</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images" target="_blank">Images - Managing images</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images/image-streams" target="_blank">Images - Image streams</a>

---

## Navegação

- [← Anterior: Builds e Images](09-builds-images.md)
- [→ Próximo: Monitoramento e Logs](11-monitoramento-logs.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
