# Segurança e RBAC

Este documento contém comandos para gerenciar segurança, permissões e RBAC no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [RBAC Básico](#rbac-básico)
3. [Roles e RoleBindings](#roles-e-rolebindings)
4. [Service Accounts](#service-accounts)
5. [Security Context Constraints (SCC)](#security-context-constraints-(scc))
6. [Policies e Auditoria](#policies-e-auditoria)
7. [Documentação Oficial](#documentação-oficial)
8. [Navegação](#navegação)
---

## RBAC Básico

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
# Verificar se usuário tem permissão para executar ação específica
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
# Exibir detalhes completos do recurso
# oc describe user <username>
oc describe user chiaretto
```

---

## Roles e RoleBindings

### Cluster Roles
```bash
# Listar ClusterRoles
oc get clusterroles
```

```bash
# Exibir cluster role "admin" em formato YAML
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
# Exibir detalhes completos do cluster role
# oc describe clusterrole <role-name> | grep -A 50 PolicyRule
oc describe clusterrole admin | grep -A 50 PolicyRule
```

### Roles (Namespace)
```bash
# Listar roles customizados do namespace
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
# Abrir editor para modificar recurso interativamente
# oc edit role <role-name>
oc edit role pod-reader
```

```bash
# Deletar o role especificado
# oc delete role <role-name>
oc delete role pod-reader
```

### ClusterRoleBindings
```bash
# Listar ClusterRoleBindings
oc get clusterrolebindings
```

```bash ignore-test
# Exibir recurso em formato JSON
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
# Listar vinculações de roles no namespace atual
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
# Exibir detalhes completos do recurso
# oc describe rolebinding <rolebinding-name>
oc describe rolebinding admin
```

---

## Service Accounts

### Gerenciar Service Accounts
```bash
# Listar Service Accounts
oc get serviceaccounts
oc get sa
```

```bash
# Criar novo recurso
# oc create serviceaccount <serviceaccount-name>
oc create serviceaccount test-app
```

```bash
# Exibir detalhes completos do serviceaccount
# oc describe sa <serviceaccount-name>
oc describe sa test-app
```

```bash ignore-test
# Exibir serviceaccount "test-app" em formato JSON
# oc get sa <serviceaccount-name> -o jsonpath='{.secrets[*].name}'
oc get sa test-app -o jsonpath='{.secrets[*].name}'
```

```bash ignore-test
# Deletar o serviceaccount especificado
# oc delete sa <serviceaccount-name>
oc delete sa test-app
```

### Usar Service Accounts
```bash ignore-test
# Adicionar role a Service Account
oc adm policy add-role-to-user <role> system:serviceaccount:development:test-app
```

```bash
# Exemplo: dar role edit
# oc adm policy <resource-name> <username> system:serviceaccount:development:test-app
oc adm policy add-role-to-user edit system:serviceaccount:development:test-app
```

```bash ignore-test
# ClusterRole para SA
oc adm policy add-cluster-role-to-user <role> system:serviceaccount:development:test-app
```

```bash ignore-test
# Usar SA em deployment
# oc set serviceaccount <serviceaccount-name>/test-app test-app
oc set serviceaccount deployment/test-app test-app
```

```bash ignore-test
# Exibir recurso "test-app" em formato JSON
# oc get pod <resource-name>app -o jsonpath='{.spec.serviceAccountName}'
oc get pod test-app -o jsonpath='{.spec.serviceAccountName}'
```

---

## Security Context Constraints (SCC)

### Listar e Ver SCCs
```bash
# Listar SCCs
oc get scc
```

```bash
# Exibir recurso "restricted" em formato YAML
oc get scc restricted -o yaml
oc get scc privileged -o yaml
oc get scc anyuid -o yaml
```

```bash
# Exibir detalhes completos do recurso
# oc describe scc <resource-name>
oc describe scc restricted
```

```bash --ignore-test
# Ver qual SCC o pod está usando
# oc get pod <resource-name>app -o yaml | grep scc
oc get pod test-app -o yaml | grep scc
```

```bash
# Exibir detalhes completos do recurso
# oc describe scc <resource-name> | grep Users
oc describe scc restricted | grep Users
```

### Adicionar Permissões SCC
```bash
# Exemplos comuns e use com moderação
# oc adm policy <resource-name> <username> system:serviceaccount:<namespace>:<sa-name>
oc adm policy add-scc-to-user anyuid system:serviceaccount:development:test-app
# oc adm policy <resource-name> <username> system:serviceaccount:<namespace>:<sa-name>
oc adm policy add-scc-to-user privileged system:serviceaccount:development:test-app
```

```bash
# Adicionar grupo
# oc adm policy <resource-name> <group-name> "cn=ocpusers,cn=users,dc=chiaretto,dc=home"
oc adm policy add-scc-to-group restricted "cn=ocpusers,cn=users,dc=chiaretto,dc=home"
```

```bash
# Remover SCC de grupo
# oc adm policy <resource-name> <group-name> "cn=ocpusers,cn=users,dc=chiaretto,dc=home"
oc adm policy remove-scc-from-group restricted "cn=ocpusers,cn=users,dc=chiaretto,dc=home"
```

```bash
# Exibir detalhes completos do recurso
# oc describe scc <resource-name>
oc describe scc restricted
```

### Troubleshoot SCC
```bash
# Exibir detalhes completos do recurso
# oc describe pod <resource-name> | grep -i scc
oc describe pod test-app | grep -i scc
```

```bash ignore-test
# Ver eventos relacionados a SCC
oc get events --field-selector involvedObject.name=<pod-name> | grep -i scc
```

```bash ignore-test
# Listar recurso de todos os namespaces do cluster
# oc get pod <resource-name>app -o yaml | grep -A 10 securityContext
oc get pod test-app -o yaml | grep -A 10 securityContext
```

---

## Policies e Auditoria

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
# Exibir recurso "cluster" em formato YAML
oc get oauth cluster -o yaml
```

```bash
# Exibir recurso "cluster" em formato JSON
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
# Listar recurso filtrados por campo específico
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

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization">Authentication and authorization</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance">Security and compliance - Security Context Constraints</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization/using-rbac">RBAC - Using RBAC to define and apply permissions</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization/understanding-and-creating-service-accounts">Service Accounts</a>
---

---

## Navegação

- [← Anterior: Troubleshooting de Storage](15-troubleshooting-storage.md)
- [→ Próximo: Cluster Operators](17-cluster-operators.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
