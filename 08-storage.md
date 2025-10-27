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

**Listar todos os Persistent Volumes do cluster**

```bash
oc get pv
oc get persistentvolumes
```

**Descrever PV**

```bash ignore-test
oc describe pv <nome-do-pv>
```

**Ver em detalhes**

```bash ignore-test
oc get pv <nome-do-pv> -o yaml
```

**Exibir persistent volume em formato JSON**

```bash
oc get pv -o jsonpath='{.items[?(@.status.phase=="Available")].metadata.name}'
```

**Exibir persistent volume em formato JSON**

```bash
oc get pv -o jsonpath='{.items[?(@.status.phase=="Bound")].metadata.name}'
```

**Deletar PV**

```bash ignore-test
oc delete pv <nome-do-pv>
```

---

## PersistentVolumeClaims (PVC)

### Criar e Gerenciar
**Listar todos os Persistent Volume Claims do namespace**

```bash
oc get pvc
oc get persistentvolumeclaims
```

**Exibir detalhes completos do persistent volume claim**

**Exemplo:** `oc describe pvc <resource-name>`

```bash ignore-test
oc describe pvc test-app
```

**Criar PVC**

```bash ignore-test
oc create -f <pvc-definition.yaml>
```

**Exibir persistent volume claim "test-app" em formato JSON**

**Exemplo:** `oc get pvc <resource-name>app -o jsonpath='{.status.phase}'`

```bash ignore-test
oc get pvc test-app -o jsonpath='{.status.phase}'
```

**Deletar o persistent volume claim especificado**

**Exemplo:** `oc delete pvc <resource-name>`

```bash ignore-test
oc delete pvc test-app
```

### Usando em Deployments
**Adicionar volume PVC a deployment**

**Exemplo:** `oc set volume <resource-name>/test-app`

```bash ignore-test
oc set volume deployment/test-app \
  --add --name=<volume-name> \
  --type=persistentVolumeClaim \
  --claim-name=test-app \
  --mount-path=<path>
```

**Remover volume**

```bash ignore-test
oc set volume deployment/test-app --remove --name=<volume-name>
```

---

## StorageClasses

**Listar StorageClasses**

```bash
oc get storageclass
oc get sc
```

**Descrever StorageClass**

```bash ignore-test
oc describe sc <nome-da-sc>
```

**Definir StorageClass padrão**

```bash ignore-test
oc patch storageclass <nome-da-sc> -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

**Exibir storageclass em formato JSON**

```bash ignore-test
oc get sc -o json | jq -r '.items[] | select(.metadata.annotations."storageclass.kubernetes.io/is-default-class"=="true") | .metadata.name'
```
---

## Volumes em Pods

### Tipos de Volumes
**EmptyDir**

**Exemplo:** `oc set volume <resource-name>/test-app --add --add --name=emptydir --type=emptyDir --mount-path=/emptydir`

```bash
oc set volume deployment/test-app --add --name=emptydir --type=emptyDir --mount-path=/emptydir
```

**HostPath (requer privilégios)**

**Exemplo:** `oc set volume <resource-name>/test-app --add --name=host --type=hostPath --path=/data --mount-path=/data`

```bash ignore-test
oc set volume deployment/test-app --add --name=host --type=hostPath --path=/data --mount-path=/data
```

**Listar volumes de um deployment**

**Exemplo:** `oc set volume <resource-name>/test-app`

```bash
oc set volume deployment/test-app
```

**Exibir detalhes completos do recurso**

**Exemplo:** `oc describe pod <resource-name> | grep -A 5 Volumes`

```bash
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
