# 🔒 Segurança e RBAC

Este documento contém comandos para gerenciar segurança, permissões e RBAC no OpenShift.

---

## 📋 Índice

1. [RBAC Básico](#rbac-básico)
2. [Roles e RoleBindings](#roles-e-rolebindings)
3. [Service Accounts](#service-accounts)
4. [Security Context Constraints (SCC)](#security-context-constraints-scc)
5. [Policies e Auditoria](#policies-e-auditoria)

---

## 👥 RBAC Básico

### Verificar Permissões
```bash
# Quem pode fazer determinada ação
oc adm policy who-can <verbo> <recurso>
oc adm policy who-can get pods
oc adm policy who-can delete projects
```

```bash
# Verificar minhas permissões
oc auth can-i <verbo> <recurso>
oc auth can-i create pods
oc auth can-i delete projects
```

```bash
# Como outro usuário
oc auth can-i get pods --as=<usuario>
```

```bash
# Listar minhas permissões
oc auth can-i --list
```

### Usuários e Grupos
```bash
# Listar usuários
oc get users
```

```bash
# Listar grupos
oc get groups
```

```bash
# Ver identidades
oc get identities
```

```bash
# Descrever usuário
oc describe user <username>
```

```bash
# Ver grupos de um usuário
oc describe user <username> | grep Groups
```

---

## 🎭 Roles e RoleBindings

### Cluster Roles
```bash
# Listar ClusterRoles
oc get clusterroles
```

```bash
# Roles importantes
oc get clusterrole admin -o yaml
oc get clusterrole edit -o yaml
oc get clusterrole view -o yaml
```

```bash
# Descrever ClusterRole
oc describe clusterrole <nome-da-role>
```

```bash
# Ver permissões de uma ClusterRole
oc describe clusterrole admin | grep -A 50 PolicyRule
```

### Roles (Namespace)
```bash
# Listar Roles no namespace
oc get roles
```

```bash
# Criar Role customizada
oc create role <nome> --verb=<verbos> --resource=<recursos>
```

```bash
# Exemplo
oc create role pod-reader --verb=get,list,watch --resource=pods
```

```bash
# Editar Role
oc edit role <nome>
```

```bash
# Deletar Role
oc delete role <nome>
```

### ClusterRoleBindings
```bash
# Listar ClusterRoleBindings
oc get clusterrolebindings
```

```bash
# Ver quem tem role cluster-admin
oc get clusterrolebinding -o json | jq -r '.items[] | select(.roleRef.name=="cluster-admin") | .metadata.name'
```

```bash
# Adicionar usuário como cluster-admin
oc adm policy add-cluster-role-to-user cluster-admin <username>
```

```bash
# Remover cluster-admin
oc adm policy remove-cluster-role-from-user cluster-admin <username>
```

```bash
# Adicionar grupo
oc adm policy add-cluster-role-to-group cluster-admin <groupname>
```

### RoleBindings (Namespace)
```bash
# Listar RoleBindings
oc get rolebindings
```

```bash
# Adicionar role a usuário no namespace
oc adm policy add-role-to-user <role> <username>
oc adm policy add-role-to-user admin <username>
oc adm policy add-role-to-user edit <username>
oc adm policy add-role-to-user view <username>
```

```bash
# Adicionar role a grupo
oc adm policy add-role-to-group <role> <groupname>
```

```bash
# Remover role
oc adm policy remove-role-from-user <role> <username>
```

```bash
# Ver RoleBinding específico
oc describe rolebinding <nome>
```

---

## 🤖 Service Accounts

### Gerenciar Service Accounts
```bash
# Listar Service Accounts
oc get serviceaccounts
oc get sa
```

```bash
# Criar Service Account
oc create serviceaccount <nome>
```

```bash
# Descrever Service Account
oc describe sa <nome>
```

```bash
# Ver token da SA
oc sa get-token <nome>
```

```bash
# Ver secrets da SA
oc get sa <nome> -o jsonpath='{.secrets[*].name}'
```

```bash
# Deletar Service Account
oc delete sa <nome>
```

### Usar Service Accounts
```bash
# Adicionar role a Service Account
oc adm policy add-role-to-user <role> system:serviceaccount:<namespace>:<sa-name>
```

```bash
# Exemplo: dar role edit
oc adm policy add-role-to-user edit system:serviceaccount:myproject:mysa
```

```bash
# ClusterRole para SA
oc adm policy add-cluster-role-to-user <role> system:serviceaccount:<namespace>:<sa-name>
```

```bash
# Usar SA em deployment
oc set serviceaccount deployment/<nome> <sa-name>
```

```bash
# Ver qual SA o pod está usando
oc get pod <nome> -o jsonpath='{.spec.serviceAccountName}'
```

---

## 🛡️ Security Context Constraints (SCC)

### Listar e Ver SCCs
```bash
# Listar SCCs
oc get scc
```

```bash
# SCCs principais
oc get scc restricted -o yaml
oc get scc privileged -o yaml
oc get scc anyuid -o yaml
```

```bash
# Descrever SCC
oc describe scc <nome>
```

```bash
# Ver qual SCC o pod está usando
oc get pod <nome> -o yaml | grep scc
```

```bash
# Ver usuários/SAs em uma SCC
oc describe scc <nome> | grep Users
```

### Adicionar Permissões SCC
```bash
# Adicionar SA a uma SCC
oc adm policy add-scc-to-user <scc-name> system:serviceaccount:<namespace>:<sa-name>
```

```bash
# Exemplos comuns
oc adm policy add-scc-to-user anyuid system:serviceaccount:myproject:mysa
oc adm policy add-scc-to-user privileged system:serviceaccount:myproject:mysa
```

```bash
# Adicionar grupo
oc adm policy add-scc-to-group <scc-name> <group-name>
```

```bash
# Remover de SCC
oc adm policy remove-scc-from-user <scc-name> system:serviceaccount:<namespace>:<sa-name>
```

```bash
# Ver quem pode usar SCC
oc describe scc <scc-name>
```

### Troubleshoot SCC
```bash
# Ver por que pod não está rodando devido a SCC
oc describe pod <nome> | grep -i scc
```

```bash
# Ver eventos relacionados a SCC
oc get events --field-selector involvedObject.name=<pod-name> | grep -i scc
```

```bash
# Verificar capabilities do container
oc get pod <nome> -o yaml | grep -A 10 securityContext
```

---

## 📜 Policies e Auditoria

### Audit Logs
```bash
# Ver audit logs (em node)
oc debug node/<node-name>
chroot /host
cat /var/log/oauth-apiserver/audit.log
cat /var/log/openshift-apiserver/audit.log
cat /var/log/kube-apiserver/audit.log
```

```bash
# Buscar ações de usuário específico
grep <username> /var/log/openshift-apiserver/audit.log
```

### OAuth e Autenticação
```bash
# Ver OAuth config
oc get oauth cluster -o yaml
```

```bash
# Ver identity providers
oc get oauth cluster -o jsonpath='{.spec.identityProviders}'
```

```bash
# Ver pods do OAuth
oc get pods -n openshift-authentication
```

```bash
# Logs do OAuth
oc logs -n openshift-authentication <oauth-pod>
```

### Secrets de TLS
```bash
# Listar secrets TLS
oc get secrets --field-selector type=kubernetes.io/tls
```

```bash
# Ver certificado
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

```bash
# Verificar validade
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout
```

```bash
# Criar secret TLS
oc create secret tls <nome> --cert=<cert-file> --key=<key-file>
```

---

## 📖 Navegação

- [← Anterior: Troubleshooting de Storage](15-troubleshooting-storage.md)
- [→ Próximo: Cluster Operators](17-cluster-operators.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
