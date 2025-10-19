# 💾 Troubleshooting de Storage

Este documento contém comandos para diagnosticar problemas de storage no OpenShift.

---

## 📋 Índice

1. [PV e PVC](#pv-e-pvc)
2. [StorageClass](#storageclass)
3. [Problemas Comuns](#problemas-comuns)
4. [Operadores de Storage](#operadores-de-storage)

---

## 📦 PV e PVC

### Diagnosticar PVC
```bash
# Listar PVCs e status
oc get pvc

# PVCs Pending
oc get pvc --field-selector=status.phase=Pending

# Descrever PVC
oc describe pvc <nome-do-pvc>

# Ver eventos relacionados
oc get events --field-selector involvedObject.name=<nome-do-pvc>

# Ver qual PV está bound
oc get pvc <nome-do-pvc> -o jsonpath='{.spec.volumeName}'

# Verificar capacidade solicitada vs disponível
oc get pvc <nome-do-pvc> -o jsonpath='{.spec.resources.requests.storage}'
```

### Diagnosticar PV
```bash
# Listar PVs
oc get pv

# PVs disponíveis
oc get pv --field-selector=status.phase=Available

# PVs com problema
oc get pv --field-selector=status.phase=Failed

# Descrever PV
oc describe pv <nome-do-pv>

# Ver claim que está usando o PV
oc get pv <nome-do-pv> -o jsonpath='{.spec.claimRef.name}'

# Ver access modes
oc get pv <nome-do-pv> -o jsonpath='{.spec.accessModes}'
```

### Pending PVC
```bash
# Ver por que PVC está Pending
oc describe pvc <nome-do-pvc> | grep -A 10 Events

# Verificar se há PV disponível
oc get pv --field-selector=status.phase=Available

# Verificar StorageClass
oc get sc

# Verificar se StorageClass existe
oc get pvc <nome-do-pvc> -o jsonpath='{.spec.storageClassName}'
oc get sc <storage-class-name>

# Ver provisioner
oc get sc <storage-class-name> -o jsonpath='{.provisioner}'
```

---

## 🏪 StorageClass

### Verificar StorageClasses
```bash
# Listar StorageClasses
oc get storageclass
oc get sc

# Descrever StorageClass
oc describe sc <nome-da-sc>

# Ver qual é a default
oc get sc -o json | jq -r '.items[] | select(.metadata.annotations."storageclass.kubernetes.io/is-default-class"=="true") | .metadata.name'

# Ver provisioner
oc get sc -o custom-columns=NAME:.metadata.name,PROVISIONER:.provisioner

# Verificar parâmetros
oc get sc <nome> -o yaml
```

### Problemas com StorageClass
```bash
# Verificar se provisioner está rodando
oc get pods -A | grep -i provisioner

# Logs do provisioner (exemplo CSI)
oc logs -n <namespace> <provisioner-pod>

# Ver CSI drivers
oc get csidrivers
oc get csinodes

# Ver CSI pods
oc get pods -A | grep csi
```

---

## 🚨 Problemas Comuns

### Volume Não Monta
```bash
# Verificar pod que usa o volume
oc describe pod <nome-do-pod> | grep -A 10 Volumes

# Ver eventos de mount
oc get events --field-selector involvedObject.name=<nome-do-pod> | grep -i mount

# Verificar se PVC está Bound
oc get pvc

# Ver node do pod
oc get pod <nome-do-pod> -o jsonpath='{.spec.nodeName}'

# Debug no node
oc debug node/<node-name>
chroot /host
# Verificar mounts
mount | grep <pv-name>
df -h
```

### ReadOnly Filesystem
```bash
# Verificar access mode do PVC
oc get pvc <nome> -o jsonpath='{.spec.accessModes}'

# Verificar access mode do PV
oc get pv <nome> -o jsonpath='{.spec.accessModes}'

# Se PV for RWO e pod está em outro node
oc get pvc <nome> -o jsonpath='{.spec.volumeName}'
oc get pod <nome-do-pod> -o jsonpath='{.spec.nodeName}'
```

### Volume Full (Cheio)
```bash
# Verificar uso dentro do pod
oc exec <nome-do-pod> -- df -h

# Verificar tamanho do PVC
oc get pvc <nome> -o jsonpath='{.spec.resources.requests.storage}'

# Expandir PVC (se StorageClass permitir)
oc patch pvc <nome> -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'

# Verificar se expansão é permitida
oc get sc <storage-class> -o jsonpath='{.allowVolumeExpansion}'

# Ver progresso da expansão
oc describe pvc <nome>
```

### PVC Stuck Terminating
```bash
# Verificar se há pods usando
oc get pods -o json | jq -r '.items[] | select(.spec.volumes[]?.persistentVolumeClaim.claimName=="<pvc-name>") | .metadata.name'

# Deletar pods que estão usando
oc delete pod <nome-do-pod> --grace-period=0 --force

# Remover finalizers se necessário (CUIDADO!)
oc patch pvc <nome> -p '{"metadata":{"finalizers":null}}'

# Ver finalizers
oc get pvc <nome> -o jsonpath='{.metadata.finalizers}'
```

---

## 🔧 Operadores de Storage

### ODF (OpenShift Data Foundation)
```bash
# Verificar pods do ODF
oc get pods -n openshift-storage

# Status do ODF
oc get storagecluster -n openshift-storage

# Ver Ceph status
oc -n openshift-storage exec -it $(oc get pods -n openshift-storage -l app=rook-ceph-tools -o name) -- ceph status

# Ceph health
oc -n openshift-storage exec -it $(oc get pods -n openshift-storage -l app=rook-ceph-tools -o name) -- ceph health detail

# Ver OSDs
oc -n openshift-storage exec -it $(oc get pods -n openshift-storage -l app=rook-ceph-tools -o name) -- ceph osd status

# Must-gather do ODF
oc adm must-gather --image=registry.redhat.io/odf4/ocs-must-gather-rhel8:latest
```

### Local Storage Operator
```bash
# Ver local volumes
oc get localvolume -A

# Ver pods do local storage
oc get pods -n openshift-local-storage

# Logs do local storage operator
oc logs -n openshift-local-storage -l name=local-storage-operator
```

### CSI Drivers
```bash
# Listar CSI drivers instalados
oc get csidrivers

# Ver pods CSI
oc get pods -A | grep csi

# Logs do CSI driver (exemplo)
oc logs -n <namespace> <csi-driver-pod> -c csi-driver

# Ver CSI nodes
oc get csinodes

# Descrever CSI node
oc describe csinode <node-name>
```

---

## 🛠️ Debug Avançado

### Verificar Backend de Storage
```bash
# Debug em node específico
oc debug node/<node-name>
chroot /host

# Ver discos
lsblk
fdisk -l

# Ver mounts
mount | grep pvc
df -h

# Ver logs do kubelet relacionados a storage
journalctl -u kubelet | grep -i volume

# Ver logs do CRI-O
journalctl -u crio | grep -i volume
```

### Comandos Úteis em Nodes
```bash
# Dentro do debug node:
chroot /host

# Ver volumes do Kubernetes
ls -la /var/lib/kubelet/pods/

# Ver PVs montados
ls -la /var/lib/origin/openshift.local.volumes/

# Verificar permissões
ls -laZ /var/lib/kubelet/pods/<pod-id>/volumes/

# Verificar SELinux contexts
ls -laZ /path/to/mount
```

---

## 📖 Navegação

- [← Anterior: Troubleshooting de Rede](14-troubleshooting-rede.md)
- [→ Próximo: Segurança e RBAC](16-seguranca-rbac.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
