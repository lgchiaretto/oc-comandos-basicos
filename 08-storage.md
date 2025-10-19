# 💾 Storage e Volumes

Este documento contém comandos para gerenciar storage no OpenShift.

---

## 📋 Índice

1. [PersistentVolumes (PV)](#persistentvolumes-pv)
2. [PersistentVolumeClaims (PVC)](#persistentvolumeclaims-pvc)
3. [StorageClasses](#storageclasses)
4. [Volumes em Pods](#volumes-em-pods)

---

## 🗄️ PersistentVolumes (PV)

```bash
# Listar PVs
oc get pv
oc get persistentvolumes

# Descrever PV
oc describe pv <nome-do-pv>

# Ver em detalhes
oc get pv <nome-do-pv> -o yaml

# Ver PVs disponíveis
oc get pv --field-selector=status.phase=Available

# Ver PVs bound
oc get pv --field-selector=status.phase=Bound

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

# Descrever PVC
oc describe pvc <nome-do-pvc>

# Criar PVC
oc create -f <pvc-definition.yaml>

# Ver status da claim
oc get pvc <nome-do-pvc> -o jsonpath='{.status.phase}'

# Deletar PVC
oc delete pvc <nome-do-pvc>

# Ver PVCs não utilizados
oc get pvc -A -o json | jq -r '.items[] | select(.status.phase=="Bound") | select(.spec.volumeName != null) | .metadata.namespace + "/" + .metadata.name'
```

### Usando em Deployments
```bash
# Adicionar volume PVC a deployment
oc set volume deployment/<nome> \
  --add --name=<volume-name> \
  --type=persistentVolumeClaim \
  --claim-name=<nome-do-pvc> \
  --mount-path=<path>

# Remover volume
oc set volume deployment/<nome> --remove --name=<volume-name>
```

---

## 🏪 StorageClasses

```bash
# Listar StorageClasses
oc get storageclass
oc get sc

# Descrever StorageClass
oc describe sc <nome-da-sc>

# Ver StorageClass padrão
oc get sc -o json | jq -r '.items[] | select(.metadata.annotations."storageclass.kubernetes.io/is-default-class"=="true") | .metadata.name'

# Definir StorageClass padrão
oc patch storageclass <nome> -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

---

## 📁 Volumes em Pods

### Tipos de Volumes
```bash
# EmptyDir
oc set volume deployment/<nome> --add --name=tmp --type=emptyDir --mount-path=/tmp

# HostPath (requer privilégios)
oc set volume deployment/<nome> --add --name=host --type=hostPath --path=/data --mount-path=/data

# Listar volumes de um deployment
oc set volume deployment/<nome>

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
