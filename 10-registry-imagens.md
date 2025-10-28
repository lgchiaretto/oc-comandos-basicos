# Registry e Gestão de Imagens

Este documento contém comandos para gerenciar o registry interno e imagens no OpenShift.

---

## Índice

- [Registry e Gestão de Imagens](#registry-e-gestão-de-imagens)
  - [Índice](#índice)
  - [Registry Interno](#registry-interno)
    - [Acessar Registry](#acessar-registry)
    - [Habilitar Registry e adicionar PVC](#habilitar-registry-e-adicionar-pvc)
  - [Push e Pull de Imagens](#push-e-pull-de-imagens)
    - [Push de Imagens](#push-de-imagens)
    - [Pull de Imagens](#pull-de-imagens)
  - [Image Mirroring](#image-mirroring)
    - [Configurar Mirroring](#configurar-mirroring)
    - [Mirror com oc-mirror](#mirror-com-oc-mirror)
  - [Image Pruning](#image-pruning)
    - [Limpeza de Imagens](#limpeza-de-imagens)
    - [Limpeza de Builds](#limpeza-de-builds)
  - [Documentação Oficial](#documentação-oficial)
  - [Navegação](#navegação)
---

## Registry Interno

### Acessar Registry
**Ver URL do registry interno**

```bash
oc get route -n openshift-image-registry
```

**Exibir configs.imageregistry.operator.openshift.io/cluster em formato YAML**

```bash
oc get configs.imageregistry.operator.openshift.io/cluster -o yaml
```

**Ver status do registry**

```bash
oc get clusteroperator image-registry
```

### Habilitar Registry e adicionar PVC 
**Aplicar modificação parcial ao recurso usando patch**

```bash
oc patch configs.imageregistry.operator.openshift.io cluster --type merge --patch '{"spec":{"managementState":"Managed"}}'
```

**Aplicar modificação parcial ao recurso usando patch para adicionar um disco ao registry com a storageclass default**

```bash
oc patch configs.imageregistry.operator.openshift.io/cluster --type merge -p '{"spec":{"storage":{"pvc":{"claim":""}}}}'
```

**Ver pods image registry criado**

```bash
oc get pods -n openshift-image-registry
```
---

## Push e Pull de Imagens

### Push de Imagens
**Tag para registry interno**

```bash ignore-test
podman tag <imagem-local> <registry-interno>/<projeto>/test-app:<tag>
```

**Push para registry interno**

```bash ignore-test
podman push <registry-interno>/<projeto>/test-app:<tag>
```

**Usando Podman**

```bash ignore-test
podman push <imagem> <registry-interno>/<projeto>/test-app:<tag>
```

**Criar secret para registry externo**

```bash ignore-test
oc create secret docker-registry <secret-name> \
  --docker-server=<registry-url> \
  --docker-username=<user> \
  --docker-password=<pass>
```

**Linkar secret para pull**

```bash ignore-test
oc secrets link default <secret-name> --for=pull
```

### Pull de Imagens
**Pull de registry interno**

```bash ignore-test
podman pull <registry-interno>/<projeto>/test-app:<tag>
```

**Exibir imagestream "s2i-chiaretto" em formato YAML**

```bash
oc get is s2i-chiaretto -o yaml
```

**Importar imagem externa**

```bash ignore-test
oc import-image test-app:<tag> --from=<registry-externo>/<image>:<tag> --confirm
```

---

## Image Mirroring

### Configurar Mirroring
**Ver ImageContentSourcePolicy**

```bash
oc get imagecontentsourcepolicy
```

**Criar ICSP para mirror**

```bash ignore-test
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

**Exibir imagecontentsourcepolicy em formato YAML**

```bash
oc get imagecontentsourcepolicy -o yaml
```

### Mirror com oc-mirror
**Mirror de operator catalogs**

```bash ignore-test
oc mirror --config=imageset-config.yaml docker://<mirror-registry>
```

**Ver resultados do mirror**

```bash ignore-test
oc mirror list operators --catalog=<catalog-image>
```

---

## Image Pruning

### Limpeza de Imagens
**Executar image pruner manual**

```bash ignore-test
oc adm prune images --confirm
```

**Dry-run (sem deletar)**

```bash ignore-test
oc adm prune images
```

**Prune de imagens antigas**

```bash ignore-test
oc adm prune images --keep-tag-revisions=3 --keep-younger-than=60m --confirm
```

**Exibir imagepruner/cluster em formato YAML**

```bash
oc get imagepruner/cluster -o yaml
```

**Aplicar modificação parcial ao recurso usando patch**

```bash
oc patch imagepruners.imageregistry.operator.openshift.io/cluster --type merge -p '{"spec":{"schedule":"0 0 * * *","suspend":false,"keepTagRevisions":3}}'
```

**Ver jobs de pruning**

```bash
oc get jobs -n openshift-image-registry
```

### Limpeza de Builds
**Prune de builds antigos**

```bash ignore-test
oc adm prune builds --confirm
```

**Manter apenas N builds**

```bash ignore-test
oc adm prune builds --keep-complete=5 --keep-failed=1 --confirm
```

**Prune por idade**

```bash ignore-test
oc adm prune builds --keep-younger-than=48h --confirm
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/registry">Registry - Integrated OpenShift image registry</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images">Images - Managing images</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/registry/configuring-registry-operator">Image Registry Operator</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Pruning objects to reclaim resources</a>
---


## Navegação

- [← Anterior: Builds e Images](09-builds-images.md)
- [→ Próximo: Monitoramento e Logs](11-monitoramento-logs.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
