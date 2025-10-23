# 💾 Storage e Volumes

Este documento contém comandos para gerenciar storage no OpenShift.

---

## 📋 Índice

- [💾 Storage e Volumes](#-storage-e-volumes)
  - [📋 Índice](#-índice)
  - [🗄️ PersistentVolumes (PV)](#️-persistentvolumes-pv)
  - [📦 PersistentVolumeClaims (PVC)](#-persistentvolumeclaims-pvc)
    - [Criar e Gerenciar](#criar-e-gerenciar)
    - [Usando em Deployments](#usando-em-deployments)
  - [🏪 StorageClasses](#-storageclasses)
  - [📁 Volumes em Pods](#-volumes-em-pods)
    - [Tipos de Volumes](#tipos-de-volumes)
  - [📖 Navegação](#-navegação)

---

## 🗄️ PersistentVolumes (PV)

```bash
# Listar PVs
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
# Ver PVs disponíveis
oc get pv --field-selector=status.phase=Available
```

```bash
# Ver PVs bound
oc get pv --field-selector=status.phase=Bound
```

```bash ignore-test
# Deletar PV
oc delete pv <nome-do-pv>
```

---

## 📦 PersistentVolumeClaims (PVC)

### Criar e Gerenciar
```bash
# Listar PVCs
oc get pvc
oc get persistentvolumeclaims
```

```bash ignore-test
# Descrever PVC
oc describe pvc <nome-do-pvc>
```

```bash ignore-test
# Criar PVC
oc create -f <pvc-definition.yaml>
```

```bash ignore-test
# Ver status da claim
oc get pvc <nome-do-pvc> -o jsonpath='{.status.phase}'
```

```bash ignore-test
# Deletar PVC
oc delete pvc <nome-do-pvc>
```

### Usando em Deployments
```bash ignore-test
# Adicionar volume PVC a deployment
oc set volume deployment/test-app \
  --add --name=<volume-name> \
  --type=persistentVolumeClaim \
  --claim-name=<nome-do-pvc> \
  --mount-path=<path>
```

```bash ignore-test
# Remover volume
oc set volume deployment/test-app --remove --name=<volume-name>
```

---

## 🏪 StorageClasses

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
# Ver StorageClass padrão
oc get sc -o json | jq -r '.items[] | select(.metadata.annotations."storageclass.kubernetes.io/is-default-class"=="true") | .metadata.name'
```
---

## 📁 Volumes em Pods

### Tipos de Volumes
```bash
# EmptyDir
oc set volume deployment/test-app --add --name=tmp --type=emptyDir --mount-path=/tmp
```

```bash
# HostPath (requer privilégios)
oc set volume deployment/test-app --add --name=host --type=hostPath --path=/data --mount-path=/data
```

```bash
# Listar volumes de um deployment
oc set volume deployment/test-app
```

```bash ignore-test
# Ver volumes montados em pod
oc describe pod <nome-do-pod> | grep -A 5 Volumes
```

---

## 📖 Navegação

- [← Anterior: ConfigMaps e Secrets](07-configmaps-secrets.md)
- [→ Próximo: Builds e Images](09-builds-images.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
