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
```

```bash
# PVCs Pending
oc get pvc --field-selector=status.phase=Pending
```

```bash
# Descrever PVC
oc describe pvc <nome-do-pvc>
```

```bash
# Ver eventos relacionados
oc get events --field-selector involvedObject.name=<nome-do-pvc>
```

```bash
# Ver qual PV está bound
oc get pvc <nome-do-pvc> -o jsonpath='{.spec.volumeName}'
```

```bash
# Verificar capacidade solicitada vs disponível
oc get pvc <nome-do-pvc> -o jsonpath='{.spec.resources.requests.storage}'
```

### Diagnosticar PV
```bash
# Listar PVs
oc get pv
```

```bash
# PVs disponíveis
oc get pv --field-selector=status.phase=Available
```

```bash
# PVs com problema
oc get pv --field-selector=status.phase=Failed
```

```bash
# Descrever PV
oc describe pv <nome-do-pv>
```

```bash
# Ver claim que está usando o PV
oc get pv <nome-do-pv> -o jsonpath='{.spec.claimRef.name}'
```

```bash
# Ver access modes
oc get pv <nome-do-pv> -o jsonpath='{.spec.accessModes}'
```

### Pending PVC
```bash
# Ver por que PVC está Pending
oc describe pvc <nome-do-pvc> | grep -A 10 Events
```

```bash
# Verificar se há PV disponível
oc get pv --field-selector=status.phase=Available
```

```bash
# Verificar StorageClass
oc get sc
```

```bash
# Verificar se StorageClass existe
oc get pvc <nome-do-pvc> -o jsonpath='{.spec.storageClassName}'
oc get sc <storage-class-name>
```

```bash
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
```

```bash
# Descrever StorageClass
oc describe sc <nome-da-sc>
```

```bash
# Ver qual é a default
oc get sc -o json | jq -r '.items[] | select(.metadata.annotations."storageclass.kubernetes.io/is-default-class"=="true") | .metadata.name'
```

```bash
# Ver provisioner
oc get sc -o custom-columns=NAME:.metadata.name,PROVISIONER:.provisioner
```

```bash
# Verificar parâmetros
oc get sc test-app -o yaml
```

### Problemas com StorageClass
```bash
# Verificar se provisioner está rodando
oc get pods -A | grep -i provisioner
```

```bash
# Logs do provisioner (exemplo CSI)
oc logs -n <namespace> <provisioner-pod>
```

```bash
# Ver CSI drivers
oc get csidrivers
oc get csinodes
```

```bash
# Ver CSI pods
oc get pods -A | grep csi
```

---

## 🚨 Problemas Comuns

### Volume Não Monta
```bash
# Verificar pod que usa o volume
oc describe pod <nome-do-pod> | grep -A 10 Volumes
```

```bash
# Ver eventos de mount
oc get events --field-selector involvedObject.name=<nome-do-pod> | grep -i mount
```

```bash
# Verificar se PVC está Bound
oc get pvc
```

```bash
# Ver node do pod
oc get pod <nome-do-pod> -o jsonpath='{.spec.nodeName}'
```

```bash
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
oc get pvc test-app -o jsonpath='{.spec.accessModes}'
```

```bash
# Verificar access mode do PV
oc get pv test-app -o jsonpath='{.spec.accessModes}'
```

```bash
# Se PV for RWO e pod está em outro node
oc get pvc test-app -o jsonpath='{.spec.volumeName}'
oc get pod <nome-do-pod> -o jsonpath='{.spec.nodeName}'
```

### Volume Full (Cheio)
```bash
# Verificar uso dentro do pod
oc exec <nome-do-pod> -- df -h
```

```bash
# Verificar tamanho do PVC
oc get pvc test-app -o jsonpath='{.spec.resources.requests.storage}'
```

```bash
# Expandir PVC (se StorageClass permitir)
oc patch pvc test-app -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'
```

```bash
# Verificar se expansão é permitida
oc get sc <storage-class> -o jsonpath='{.allowVolumeExpansion}'
```

```bash
# Ver progresso da expansão
oc describe pvc test-app
```

### PVC Stuck Terminating
```bash
# Verificar se há pods usando
oc get pods -o json | jq -r '.items[] | select(.spec.volumes[]?.persistentVolumeClaim.claimName=="<pvc-name>") | .metadata.name'
```

```bash
# Deletar pods que estão usando
oc delete pod <nome-do-pod> --grace-period=0 --force
```

```bash
# Remover finalizers se necessário (CUIDADO!)
oc patch pvc test-app -p '{"metadata":{"finalizers":null}}'
```

```bash
# Ver finalizers
oc get pvc test-app -o jsonpath='{.metadata.finalizers}'
```

---

## 🔧 Operadores de Storage

### ODF (OpenShift Data Foundation)
```bash
# Verificar pods do ODF
oc get pods -n openshift-storage
```

```bash
# Status do ODF
oc get storagecluster -n openshift-storage
```

```bash
# Ver Ceph status
oc -n openshift-storage exec -it $(oc get pods -n openshift-storage -l app=rook-ceph-tools -o name) -- ceph status
```

```bash
# Ceph health
oc -n openshift-storage exec -it $(oc get pods -n openshift-storage -l app=rook-ceph-tools -o name) -- ceph health detail
```

```bash
# Ver OSDs
oc -n openshift-storage exec -it $(oc get pods -n openshift-storage -l app=rook-ceph-tools -o name) -- ceph osd status
```

```bash
# Must-gather do ODF
oc adm must-gather --image=registry.redhat.io/odf4/ocs-must-gather-rhel8:latest
```

### Local Storage Operator
```bash
# Ver local volumes
oc get localvolume -A
```

```bash
# Ver pods do local storage
oc get pods -n openshift-local-storage
```

```bash
# Logs do local storage operator
oc logs -n openshift-local-storage -l name=local-storage-operator
```

### CSI Drivers
```bash
# Listar CSI drivers instalados
oc get csidrivers
```

```bash
# Ver pods CSI
oc get pods -A | grep csi
```

```bash
# Logs do CSI driver (exemplo)
oc logs -n <namespace> <csi-driver-pod> -c csi-driver
```

```bash
# Ver CSI nodes
oc get csinodes
```

```bash
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
```

```bash
# Ver discos
lsblk
fdisk -l
```

```bash
# Ver mounts
mount | grep pvc
df -h
```

```bash
# Ver logs do kubelet relacionados a storage
journalctl -u kubelet | grep -i volume
```

```bash
# Ver logs do CRI-O
journalctl -u crio | grep -i volume
```

### Comandos Úteis em Nodes
```bash
# Dentro do debug node:
chroot /host
```

```bash
# Ver volumes do Kubernetes
ls -la /var/lib/kubelet/pods/
```

```bash
# Ver PVs montados
ls -la /var/lib/origin/openshift.local.volumes/
```

```bash
# Verificar permissões
ls -laZ /var/lib/kubelet/pods/<pod-id>/volumes/
```

```bash
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
