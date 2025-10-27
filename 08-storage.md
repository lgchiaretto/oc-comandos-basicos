# Storage e Volumes

Este documento contém comandos para gerenciar storage no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [PersistentVolumes (PV)](#persistentvolumes-(pv))
3. [PersistentVolumeClaims (PVC)](#persistentvolumeclaims-(pvc))
4. [StorageClasses](#storageclasses)
5. [Volumes em Pods](#volumes-em-pods)
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## PersistentVolumes (PV)

```bash
# Listar todos os Persistent Volumes do cluster
oc get pv
oc get persistentvolumes
```

```bash ignore-test
# Descrever PV
oc describe pv <nome-do-pv>
```

```bash ignore-test
# Ver em detalhes
oc get pv <nome-do-pv> -o yaml
```

```bash
# Exibir persistent volume em formato JSON
oc get pv -o jsonpath='{.items[?(@.status.phase=="Available")].metadata.name}'
```

```bash
# Exibir persistent volume em formato JSON
oc get pv -o jsonpath='{.items[?(@.status.phase=="Bound")].metadata.name}'
```

```bash ignore-test
# Deletar PV
oc delete pv <nome-do-pv>
```

---

## PersistentVolumeClaims (PVC)

### Criar e Gerenciar
```bash
# Listar todos os Persistent Volume Claims do namespace
oc get pvc
oc get persistentvolumeclaims
```

```bash ignore-test
# Exibir detalhes completos do persistent volume claim
# oc describe pvc <resource-name>
oc describe pvc test-app
```

```bash ignore-test
# Criar PVC
oc create -f <pvc-definition.yaml>
```

```bash ignore-test
# Exibir persistent volume claim "test-app" em formato JSON
# oc get pvc <resource-name>app -o jsonpath='{.status.phase}'
oc get pvc test-app -o jsonpath='{.status.phase}'
```

```bash ignore-test
# Deletar o persistent volume claim especificado
# oc delete pvc <resource-name>
oc delete pvc test-app
```

### Usando em Deployments
```bash ignore-test
# Adicionar volume PVC a deployment
# oc set volume <resource-name>/test-app
oc set volume deployment/test-app \
  --add --name=<volume-name> \
  --type=persistentVolumeClaim \
  --claim-name=test-app \
  --mount-path=<path>
```

```bash ignore-test
# Remover volume
oc set volume deployment/test-app --remove --name=<volume-name>
```

---

## StorageClasses

```bash
# Listar StorageClasses
oc get storageclass
oc get sc
```

```bash ignore-test
# Descrever StorageClass
oc describe sc <nome-da-sc>
```

```bash ignore-test
# Definir StorageClass padrão
oc patch storageclass <nome-da-sc> -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

```bash ignore-test
# Exibir storageclass em formato JSON
oc get sc -o json | jq -r '.items[] | select(.metadata.annotations."storageclass.kubernetes.io/is-default-class"=="true") | .metadata.name'
```
---

## Volumes em Pods

### Tipos de Volumes
```bash
# EmptyDir
# oc set volume <resource-name>/test-app --add --add --name=emptydir --type=emptyDir --mount-path=/emptydir
oc set volume deployment/test-app --add --name=emptydir --type=emptyDir --mount-path=/emptydir
```

```bash ignore-test
# HostPath (requer privilégios)
# oc set volume <resource-name>/test-app --add --name=host --type=hostPath --path=/data --mount-path=/data
oc set volume deployment/test-app --add --name=host --type=hostPath --path=/data --mount-path=/data
```

```bash
# Listar volumes de um deployment
# oc set volume <resource-name>/test-app
oc set volume deployment/test-app
```

```bash
# Exibir detalhes completos do recurso
# oc describe pod <resource-name> | grep -A 5 Volumes
oc describe pod my-pod | grep -A 5 Volumes
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage">Storage</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage/dynamic-provisioning">Storage - Dynamic provisioning</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage/understanding-persistent-storage">Understanding persistent storage</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage/expanding-persistent-volumes">Expanding persistent volumes</a>
---

---

## Navegação

- [← Anterior: ConfigMaps e Secrets](07-configmaps-secrets.md)
- [→ Próximo: Builds e Images](09-builds-images.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
