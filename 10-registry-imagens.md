# Registry e Gestão de Imagens

Este documento contém comandos para gerenciar o registry interno e imagens no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Registry Interno](#registry-interno)
3. [Push e Pull de Imagens](#push-e-pull-de-imagens)
4. [Image Mirroring](#image-mirroring)
5. [Image Pruning](#image-pruning)
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## Registry Interno

### Acessar Registry
**Ação:** Ver URL do registry interno

```bash
oc get route -n openshift-image-registry
```

**Ação:** Exibir recurso em formato YAML

```bash
oc get configs.imageregistry.operator.openshift.io/cluster -o yaml
```

**Ação:** Ver status do registry
**Exemplo:** `oc get clusteroperator <resource-name>`

```bash
oc get clusteroperator image-registry
```

### Configurar Registry
**Ação:** Aplicar modificação parcial ao recurso usando patch

```bash
oc patch configs.imageregistry.operator.openshift.io/cluster --type merge -p '{"spec":{"defaultRoute":true}}'
```

**Ação:** Ver route criada

```bash
oc get route -n openshift-image-registry
```

**Ação:** Aplicar modificação parcial ao recurso usando patch

```bash
oc patch configs.imageregistry.operator.openshift.io/cluster --type merge -p '{"spec":{"storage":{"pvc":{"claim":""}}}}'
```

---

## Push e Pull de Imagens

### Push de Imagens
**Ação:** Tag para registry interno

```bash ignore-test
docker tag <imagem-local> <registry-interno>/<projeto>/test-app:<tag>
```

**Ação:** Push para registry interno

```bash ignore-test
docker push <registry-interno>/<projeto>/test-app:<tag>
```

**Ação:** Usando Podman

```bash ignore-test
podman push <imagem> <registry-interno>/<projeto>/test-app:<tag>
```

**Ação:** Criar secret para registry externo

```bash ignore-test
oc create secret docker-registry <secret-name> \
  --docker-server=<registry-url> \
  --docker-username=<user> \
  --docker-password=<pass>
```

**Ação:** Linkar secret para pull

```bash ignore-test
oc secrets link default <secret-name> --for=pull
```

### Pull de Imagens
**Ação:** Pull de registry interno

```bash ignore-test
docker pull <registry-interno>/<projeto>/test-app:<tag>
```

**Ação:** Exibir imagestream "s2i-chiaretto" em formato YAML
**Exemplo:** `oc get is <imagestream-name> -o yaml`

```bash
oc get is s2i-chiaretto -o yaml
```

**Ação:** Importar imagem externa

```bash ignore-test
oc import-image test-app:<tag> --from=<registry-externo>/<image>:<tag> --confirm
```

---

## Image Mirroring

### Configurar Mirroring
**Ação:** Ver ImageContentSourcePolicy

```bash
oc get imagecontentsourcepolicy
```

**Ação:** Criar ICSP para mirror

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

**Ação:** Exibir recurso em formato YAML

```bash
oc get imagecontentsourcepolicy -o yaml
```

### Mirror com oc-mirror
**Ação:** Mirror de operator catalogs

```bash ignore-test
oc mirror --config=imageset-config.yaml docker://<mirror-registry>
```

**Ação:** Ver resultados do mirror

```bash ignore-test
oc mirror list operators --catalog=<catalog-image>
```

---

## Image Pruning

### Limpeza de Imagens
**Ação:** Executar image pruner manual

```bash ignore-test
oc adm prune images --confirm
```

**Ação:** Dry-run (sem deletar)
**Exemplo:** `oc adm prune <resource-name>`

```bash ignore-test
oc adm prune images
```

**Ação:** Prune de imagens antigas

```bash ignore-test
oc adm prune images --keep-tag-revisions=3 --keep-younger-than=60m --confirm
```

**Ação:** Exibir recurso em formato YAML

```bash
oc get imagepruner/cluster -o yaml
```

**Ação:** Aplicar modificação parcial ao recurso usando patch

```bash
oc patch imagepruners.imageregistry.operator.openshift.io/cluster --type merge -p '{"spec":{"schedule":"0 0 * * *","suspend":false,"keepTagRevisions":3}}'
```

**Ação:** Ver jobs de pruning

```bash
oc get jobs -n openshift-image-registry
```

### Limpeza de Builds
**Ação:** Prune de builds antigos

```bash ignore-test
oc adm prune builds --confirm
```

**Ação:** Manter apenas N builds

```bash ignore-test
oc adm prune builds --keep-complete=5 --keep-failed=1 --confirm
```

**Ação:** Prune por idade

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

---

## Navegação

- [← Anterior: Builds e Images](09-builds-images.md)
- [→ Próximo: Monitoramento e Logs](11-monitoramento-logs.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
