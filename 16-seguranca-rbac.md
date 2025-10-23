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
```bash ignore-test
# Quem pode fazer determinada ação
oc adm policy who-can <verbo> <recurso>

# oc adm policy <resource-name> get pods
oc adm policy who-can get pods

# oc adm policy <resource-name> delete projects
oc adm policy who-can delete projects
```

```bash ignore-test
# Verificar minhas permissões
oc auth can-i <verbo> <recurso>
oc auth can-i create pods
oc auth can-i delete projects
```

```bash ignore-test
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
# oc describe user <username>
oc describe user admin
```

```bash
# Ver grupos de um usuário
# oc describe user <username> | grep Groups
oc describe user admin | grep Groups
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
# oc get clusterrole <role-name> -o yaml
oc get clusterrole admin -o yaml
# oc get clusterrole <role-name> -o yaml
oc get clusterrole edit -o yaml
# oc get clusterrole <role-name> -o yaml
oc get clusterrole view -o yaml
```

```bash ignore-test
# Descrever ClusterRole
oc describe clusterrole <nome-da-role>
```

```bash
# Ver permissões de uma ClusterRole
# oc describe clusterrole <role-name> | grep -A 50 PolicyRule
oc describe clusterrole admin | grep -A 50 PolicyRule
```

### Roles (Namespace)
```bash
# Listar Roles no namespace
oc get roles
```

```bash ignore-test
# Criar Role customizada
oc create role test-app --verb=<verbos> --resource=<recursos>
```

```bash
# Exemplo
# oc create role <role-name> --verb=get,list,watch --resource=pods
oc create role pod-reader --verb=get,list,watch --resource=pods
```

```bash ignore-test
# Editar Role
# oc edit role <role-name>
oc edit role test-app
```

```bash
# Deletar Role
# oc delete role <role-name>
oc delete role test-app
```

### ClusterRoleBindings
```bash
# Listar ClusterRoleBindings
oc get clusterrolebindings
```

```bash ignore-test
# Ver quem tem role cluster-admin
oc get clusterrolebinding -o json | jq -r '.items[] | select(.roleRef.name=="cluster-admin") | .metadata.name'
```

```bash ignore-test
# Adicionar usuário como cluster-admin
oc adm policy add-cluster-role-to-user cluster-admin <username>
```

```bash ignore-test
# Remover cluster-admin
oc adm policy remove-cluster-role-from-user cluster-admin <username>
```

```bash ignore-test
# Adicionar grupo
oc adm policy add-cluster-role-to-group cluster-admin <groupname>
```

### RoleBindings (Namespace)
```bash
# Listar RoleBindings
oc get rolebindings
```

```bash ignore-test
# Adicionar role a usuário no namespace
oc adm policy add-role-to-user <role> <username>
oc adm policy add-role-to-user admin <username>
oc adm policy add-role-to-user edit <username>
oc adm policy add-role-to-user view <username>
```

```bash ignore-test
# Adicionar role a grupo
oc adm policy add-role-to-group <role> <groupname>
```

```bash ignore-test
# Remover role
oc adm policy remove-role-from-user <role> <username>
```

```bash
# Ver RoleBinding específico
# oc describe rolebinding <rolebinding-name>
oc describe rolebinding test-app
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
# oc create serviceaccount <serviceaccount-name>
oc create serviceaccount test-app
```

```bash
# Descrever Service Account
# oc describe sa <serviceaccount-name>
oc describe sa test-app
```

```bash
# Ver token da SA
# oc sa <serviceaccount-name> test-app
oc sa get-token test-app
```

```bash ignore-test
# Ver secrets da SA
# oc get sa <serviceaccount-name> -o jsonpath='{.secrets[*].name}'
oc get sa test-app -o jsonpath='{.secrets[*].name}'
```

```bash
# Deletar Service Account
# oc delete sa <serviceaccount-name>
oc delete sa test-app
```

### Usar Service Accounts
```bash ignore-test
# Adicionar role a Service Account
oc adm policy add-role-to-user <role> system:serviceaccount:<namespace>:<sa-name>
```

```bash
# Exemplo: dar role edit
# oc adm policy <resource-name> <username> system:serviceaccount:myproject:mysa
oc adm policy add-role-to-user edit system:serviceaccount:myproject:mysa
```

```bash ignore-test
# ClusterRole para SA
oc adm policy add-cluster-role-to-user <role> system:serviceaccount:<namespace>:<sa-name>
```

```bash ignore-test
# Usar SA em deployment
oc set serviceaccount deployment/test-app <sa-name>
```

```bash
# Ver qual SA o pod está usando
# oc get pod <resource-name>app -o jsonpath='{.spec.serviceAccountName}'
oc get pod test-app -o jsonpath='{.spec.serviceAccountName}'
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
# oc describe scc <resource-name>
oc describe scc test-app
```

```bash
# Ver qual SCC o pod está usando
# oc get pod <resource-name>app -o yaml | grep scc
oc get pod test-app -o yaml | grep scc
```

```bash
# Ver usuários/SAs em uma SCC
# oc describe scc <resource-name> | grep Users
oc describe scc test-app | grep Users
```

### Adicionar Permissões SCC
```bash ignore-test
# Adicionar SA a uma SCC
oc adm policy add-scc-to-user <scc-name> system:serviceaccount:<namespace>:<sa-name>
```

```bash
# Exemplos comuns
# oc adm policy <resource-name> <username> system:serviceaccount:myproject:mysa
oc adm policy add-scc-to-user anyuid system:serviceaccount:myproject:mysa
# oc adm policy <resource-name> <username> system:serviceaccount:myproject:mysa
oc adm policy add-scc-to-user privileged system:serviceaccount:myproject:mysa
```

```bash ignore-test
# Adicionar grupo
oc adm policy add-scc-to-group <scc-name> <group-name>
```

```bash ignore-test
# Remover de SCC
oc adm policy remove-scc-from-user <scc-name> system:serviceaccount:<namespace>:<sa-name>
```

```bash ignore-test
# Ver quem pode usar SCC
oc describe scc <scc-name>
```

### Troubleshoot SCC
```bash
# Ver por que pod não está rodando devido a SCC
# oc describe pod <resource-name> | grep -i scc
oc describe pod test-app | grep -i scc
```

```bash ignore-test
# Ver eventos relacionados a SCC
oc get events --field-selector involvedObject.name=<pod-name> | grep -i scc
```

```bash
# Verificar capabilities do container
# oc get pod <resource-name>app -o yaml | grep -A 10 securityContext
oc get pod test-app -o yaml | grep -A 10 securityContext
```

---

## 📜 Policies e Auditoria

### Audit Logs
```bash ignore-test
# Ver audit logs (em node)
oc debug node/<node-name>
chroot /host
cat /var/log/oauth-apiserver/audit.log
cat /var/log/openshift-apiserver/audit.log
cat /var/log/kube-apiserver/audit.log
```

```bash ignore-test
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

```bash ignore-test
# Logs do OAuth
oc logs -n openshift-authentication <oauth-pod>
```

### Secrets de TLS
```bash
# Listar secrets TLS
oc get secrets --field-selector type=kubernetes.io/tls
```

```bash ignore-test
# Ver certificado
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

```bash ignore-test
# Verificar validade
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout
```

```bash ignore-test
# Criar secret TLS
oc create secret tls test-app --cert=<cert-file> --key=<key-file>
```

---

## 📖 Navegação

- [← Anterior: Troubleshooting de Storage](15-troubleshooting-storage.md)
- [→ Próximo: Cluster Operators](17-cluster-operators.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
