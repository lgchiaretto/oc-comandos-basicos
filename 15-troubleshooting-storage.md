# Troubleshooting de Storage

Este documento contém comandos para diagnosticar problemas de storage no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [PV e PVC](#pv-e-pvc)
3. [StorageClass](#storageclass)
4. [Problemas Comuns](#problemas-comuns)
5. [Operadores de Storage](#operadores-de-storage)
6. [Debug Avançado](#debug-avançado)
7. [Documentação Oficial](#documentação-oficial)
8. [Navegação](#navegação)
---

## PV e PVC

### Criar PVC

```bash
oc create -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-app
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  # Nenhuma linha storageClassName é informada.
  # O OpenShift usará a StorageClass marcada como "(default)".
EOF
```

### Diagnosticar PVC
```bash
# Listar todos os Persistent Volume Claims do namespace
oc get pvc
```

```bash
# Exibir persistent volume claim em formato JSON
oc get pvc -o jsonpath='{.items[?(@.status.phase=="Pending")].metadata.name}'
```

```bash
# Exibir detalhes completos do persistent volume claim
# oc describe pvc <resource-name>
oc describe pvc test-app
```

```bash
# Listar eventos filtrados por campo específico
oc get events --field-selector involvedObject.name=test-app
```

```bash
# Exibir persistent volume claim "test-app" em formato JSON
# oc get pvc <resource-name>app -o jsonpath='{.spec.volumeName}'
oc get pvc test-app -o jsonpath='{.spec.volumeName}'
```

```bash
# Exibir persistent volume claim "test-app" em formato JSON
# oc get pvc <resource-name>app -o jsonpath='{.spec.resources.requests.storage}'
oc get pvc test-app -o jsonpath='{.spec.resources.requests.storage}'
```

### Diagnosticar PV
```bash
# Listar todos os Persistent Volumes do cluster
oc get pv
```

```bash
# Exibir persistent volume em formato JSON
oc get pv -o jsonpath='{.items[?(@.status.phase=="Available")].metadata.name}'
```

```bash
# Exibir persistent volume em formato JSON
oc get pv -o jsonpath='{.items[?(@.status.phase=="Failed")].metadata.name}'
```

```bash ignore-test
# Descrever PV
oc describe pv <nome-do-pv>
```

```bash ignore-test
# Ver claim que está usando o PV
oc get pv <nome-do-pv> -o jsonpath='{.spec.claimRef.name}'
```

```bash ignore-test
# Ver access modes
oc get pv <nome-do-pv> -o jsonpath='{.spec.accessModes}'
```

### Pending PVC
```bash
# Exibir detalhes completos do persistent volume claim
# oc describe pvc <resource-name> | grep -A 10 Events
oc describe pvc test-app | grep -A 10 Events
```

```bash
# Exibir persistent volume em formato JSON
oc get pv -o jsonpath='{.items[?(@.status.phase=="Available")].metadata.name}'
```

```bash
# Verificar StorageClass
oc get sc
```

```bash ignore-test
# Verificar se StorageClass existe
oc get sc <storage-class-name>
```

```bash ignore-test
# Ver provisioner
oc get sc <storage-class-name> -o jsonpath='{.provisioner}'
```

---

## StorageClass

### Verificar StorageClasses
```bash
# Listar StorageClasses
oc get storageclass
oc get sc
```

```bash ignore-test
# Descrever StorageClass
oc describe sc <nome-da-sc>
```

```bash
# Exibir storageclass em formato JSON
oc get sc -o json | jq -r '.items[] | select(.metadata.annotations."storageclass.kubernetes.io/is-default-class"=="true") | .metadata.name'
```

```bash
# Listar storageclass com colunas customizadas
oc get sc -o custom-columns=NAME:.metadata.name,PROVISIONER:.provisioner
```
ignore-test
```bash 
# Verificar parâmetros
# oc get sc <resource-name> -o yaml
oc get sc <resource-name> -o yaml
```

### Problemas com StorageClass

```bash
# Ver CSI drivers
oc get csidrivers
oc get csinodes
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep csi
```

---

## Problemas Comuns

### Volume Não Monta
```bash
# Exibir detalhes completos do recurso
# oc describe pod <resource-name> | grep -A 10 Volumes
oc describe pod my-pod | grep -A 10 Volumes
```

```bash
# Listar eventos filtrados por campo específico
oc get events --field-selector involvedObject.name=my-pod
```

```bash
# Listar todos os Persistent Volume Claims do namespace
oc get pvc
```

```bash
# Exibir recurso "my-pod" em formato JSON
# oc get pod <resource-name>pod -o jsonpath='{.spec.nodeName}'
oc get pod my-pod -o jsonpath='{.spec.nodeName}'
```

```bash ignore-test
# Debug no node
oc debug node/<node-name>
chroot /host
# Verificar mounts
mount | grep <pv-name>
df -h
```

### ReadOnly Filesystem
```bash
# Exibir persistent volume claim "test-app" em formato JSON
# oc get pvc <resource-name>app -o jsonpath='{.spec.accessModes}'
oc get pvc test-app -o jsonpath='{.spec.accessModes}'
```

```bash ignore-test
# Verificar access mode do PV
# oc get pv <pv-name> -o jsonpath='{.spec.accessModes}'
oc get pv <pv-name> -o jsonpath='{.spec.accessModes}'
```

```bash ignore-test
# Exibir persistent volume claim "test-app" em formato JSON
# oc get pvc <resource-name>app -o jsonpath='{.spec.volumeName}'
oc get pvc test-app -o jsonpath='{.spec.volumeName}'
# oc get pod <resource-name>pod -o jsonpath='{.spec.nodeName}'
oc get pod my-pod -o jsonpath='{.spec.nodeName}'
```

### Volume Full (Cheio)
```bash ignore-test
# Executar comando dentro do pod especificado
oc exec my-pod -- df -h
```

```bash
# Exibir persistent volume claim "test-app" em formato JSON
# oc get pvc <resource-name>app -o jsonpath='{.spec.resources.requests.storage}'
oc get pvc test-app -o jsonpath='{.spec.resources.requests.storage}'
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch pvc <resource-name>app -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'
oc patch pvc test-app -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'
```

```bash ignore-test
# Verificar se expansão é permitida
oc get sc <storage-class> -o jsonpath='{.allowVolumeExpansion}'
```

```bash
# Exibir detalhes completos do persistent volume claim
# oc describe pvc <resource-name>
oc describe pvc test-app
```

### PVC Stuck Terminating
```bash ignore-test
# Exibir pods em formato JSON
oc get pods -o json | jq -r '.items[] | select(.spec.volumes[]?.persistentVolumeClaim.claimName=="test-app") | .metadata.name'
```

```bash ignore-test
# Deletar recurso forçadamente (sem período de espera)
# oc delete pod <resource-name>pod --grace-period=0 --force
oc delete pod my-pod --grace-period=0 --force
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch pvc <resource-name>app -p '{"metadata":{"finalizers":null}}'
oc patch pvc test-app -p '{"metadata":{"finalizers":null}}'
```

```bash
# Exibir persistent volume claim "test-app" em formato JSON
# oc get pvc <resource-name>app -o jsonpath='{.metadata.finalizers}'
oc get pvc test-app -o jsonpath='{.metadata.finalizers}'
```

---

## Operadores de Storage

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
# Listar recurso filtrados por label
oc exec -it $(oc get pods -l app=rook-ceph-operator -o jsonpath='{.items[*].metadata.name}' -n openshift-storage) -n openshift-storage --   ceph status --cluster=openshift-storage --conf=/var/lib/rook/openshift-storage/openshift-storage.config --keyring=/var/lib/rook/openshift-storage/client.admin.keyring
```

```bash
# Listar recurso filtrados por label
oc exec -it $(oc get pods -l app=rook-ceph-operator -o jsonpath='{.items[*].metadata.name}' -n openshift-storage) -n openshift-storage --   ceph health detail --cluster=openshift-storage --conf=/var/lib/rook/openshift-storage/openshift-storage.config --keyring=/var/lib/rook/openshift-storage/client.admin.keyring
```

```bash
# Listar recurso filtrados por label
oc exec -it $(oc get pods -l app=rook-ceph-operator -o jsonpath='{.items[*].metadata.name}' -n openshift-storage) -n openshift-storage --   ceph osd status --cluster=openshift-storage --conf=/var/lib/rook/openshift-storage/openshift-storage.config --keyring=/var/lib/rook/openshift-storage/client.admin.keyring
```

```bash ignore-test
# Coletar dados de diagnóstico completo do cluster
oc adm must-gather --image=registry.redhat.io/odf4/ocs-must-gather-rhel8:latest
```

### Local Storage Operator
```bash
# Listar recurso de todos os namespaces do cluster
oc get localvolume -A
```

```bash
# Ver pods do local storage
oc get pods -n openshift-local-storage
```

```bash
# Exibir logs de todos os pods que correspondem ao label
# oc logs -n <namespace> -l name=local-storage-operator
oc logs -n openshift-local-storage -l name=local-storage-operator
```

### CSI Drivers
```bash
# Listar CSI drivers instalados
oc get csidrivers
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep csi
```

```bash ignore-test
# Logs do CSI driver (exemplo)
oc logs -n <namespace> <csi-driver-pod> -c csi-driver
```

```bash
# Ver CSI nodes
oc get csinodes
```

```bash ignore-test
# Descrever CSI node
oc describe csinode <node-name>
```

---

## Debug Avançado

### Verificar Backend de Storage
```bash ignore-test
# Debug em node específico
oc debug node/<node-name>
chroot /host
```

```bash ignore-test
# Ver discos
lsblk
fdisk -l
```

```bash ignore-test
# Ver mounts
mount | grep pvc
df -h
```

```bash ignore-test
# Ver logs do kubelet relacionados a storage
journalctl -u kubelet | grep -i volume
```

```bash ignore-test
# Ver logs do CRI-O
journalctl -u crio | grep -i volume
```

### Comandos Úteis em Nodes
```bash ignore-test
# Dentro do debug node:
chroot /host
```

```bash ignore-test
# Ver volumes do Kubernetes
ls -la /var/lib/kubelet/pods/
```

```bash ignore-test
# Ver PVs montados
ls -la /var/lib/origin/openshift.local.volumes/
```

```bash ignore-test
# Verificar permissões
ls -laZ /var/lib/kubelet/pods/<pod-id>/volumes/
```

```bash ignore-test
# Verificar SELinux contexts
ls -laZ /path/to/mount
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage">Storage - Troubleshooting persistent storage</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support">Support - Troubleshooting</a>
---

---

## Navegação

- [← Anterior: Troubleshooting de Rede](14-troubleshooting-rede.md)
- [→ Próximo: Segurança e RBAC](16-seguranca-rbac.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
