# 🔐 Certificados e CSR

Este documento contém comandos para gerenciar certificados e Certificate Signing Requests no OpenShift.

---

## 📋 Índice

1. [📝 CSR (Certificate Signing Requests)](#csr-certificate-signing-requests)
2. [🔒 Certificados do Cluster](#certificados-do-cluster)
3. [🌐 Certificados de API](#certificados-de-api)
4. [🔧 Troubleshooting](#troubleshooting)
---

## 📝 CSR (Certificate Signing Requests)

### Visualizar CSRs
```bash
# Listar todos os CSRs
oc get csr
```

```bash ignore-test
# CSRs pendentes
oc get csr | grep Pending
```

```bash
# Com mais detalhes
oc get csr -o wide
```

```bash ignore-test
# Ver CSR específico
oc describe csr <csr-name>
```

```bash ignore-test
# Ver certificado em CSR
oc get csr <csr-name> -o jsonpath='{.spec.request}' | base64 -d | openssl req -text -noout
```

### Aprovar CSRs
```bash ignore-test
# Aprovar CSR específico
oc adm certificate approve <csr-name>
```

```bash ignore-test
# Aprovar todos os CSRs pendentes (CUIDADO!)
oc get csr -o name | xargs oc adm certificate approve
```

```bash ignore-test
# Aprovar apenas CSRs de nodes
oc get csr -o json | jq -r '.items[] | select(.status == {} ) | .metadata.name' | xargs oc adm certificate approve
```

```bash ignore-test
# Aprovar CSRs específicos de worker nodes
oc get csr -o json | jq -r '.items[] | select(.spec.username | contains("system:node:worker")) | select(.status == {}) | .metadata.name' | xargs oc adm certificate approve
```

### Negar CSRs
```bash ignore-test
# Negar CSR
oc adm certificate deny <csr-name>
```

```bash ignore-test
# Deletar CSR
oc delete csr <csr-name>
```

### Monitorar CSRs
```bash
# Watch CSRs
oc get csr
```

```bash
# Ver CSRs criados nas últimas horas
oc get csr --sort-by='.metadata.creationTimestamp'
```

```bash ignore-test
# Count de CSRs por status
oc get csr -o json | jq -r '.items[] | .status | keys[0] // "Pending"' | sort | uniq -c
```

---

## 🔒 Certificados do Cluster

### API Server Certificates
```bash
# Ver certificados do API server
oc get secret -n openshift-kube-apiserver
```

```bash
# Certificado do serving
oc get secret -n openshift-kube-apiserver | grep serving
```

```bash ignore-test
# Ver validade do certificado
oc get secret <secret-name> -n openshift-kube-apiserver -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout
```

```bash ignore-test
# Ver detalhes do certificado
oc get secret <secret-name> -n openshift-kube-apiserver -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

### Ingress Certificates
```bash
# Certificado padrão do ingress
oc get secret -n openshift-ingress
```

```bash
# Router default certificate
# oc get secret <secret-name> -n <namespace> -o yaml
oc get secret apps-cert -n openshift-ingress -o yaml
```

```bash
# Ver validade do certificado default
# oc get secret <secret-name> -n <namespace> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout
oc get secret apps-cert -n openshift-ingress -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout
```

```bash ignore-test
# Substituir certificado do ingress
oc create secret tls custom-certs --cert=<cert-file> --key=<key-file> -n openshift-ingress
```

```bash
# oc patch ingresscontroller default -n <namespace> --type=merge -p '{"spec":{"defaultCertificate":{"name":"apps-cert"}}}'
oc patch ingresscontroller default -n openshift-ingress-operator --type=merge -p '{"spec":{"defaultCertificate":{"name":"apps-cert"}}}'
```

### Service Serving Certificates
```bash
# Secrets de service serving
oc get secrets --field-selector type=kubernetes.io/tls
```

```bash ignore-test
# Ver secret específico
oc get secret <secret-name> -o yaml
```

```bash ignore-test
# Anotar service para gerar certificado automático
oc annotate service <service-name> service.beta.openshift.io/serving-cert-secret-name=<secret-name>
```

```bash ignore-test
# Verificar certificado gerado
oc get secret <secret-name>
```

---

## 🌐 Certificados de API

### Custom API Certificates
```bash ignore-test
# Configurar certificado customizado para API
oc create secret tls api-certs --cert=<cert-file> --key=<key-file> -n openshift-config
```

```bash ignore-test
# Aplicar certificado
oc patch apiserver cluster --type=merge -p '{"spec":{"servingCerts":{"namedCertificates":[{"names":["<api-hostname>"],"servingCertificate":{"name":"api-certs"}}]}}}'
```

```bash
# Ver configuração
oc get apiserver cluster -o yaml
```

### OAuth Certificates
```bash ignore-test
# Configurar certificado para OAuth
oc create secret tls oauth-certs --cert=<cert-file> --key=<key-file> -n openshift-config
```

```bash ignore-test
# Aplicar
oc patch oauths cluster --type=merge -p '{"spec":{"componentRoutes":[{"hostname":"<oauth-hostname>","name":"oauth-openshift","namespace":"openshift-authentication","servingCertKeyPairSecret":{"name":"oauth-certs"}}]}}'
```

---

## 🔧 Troubleshooting

### Problemas com Certificados
```bash ignore-test
# Verificar expiração de todos os certificados importantes
for ns in openshift-kube-apiserver openshift-ingress openshift-authentication; do
  echo "=== Namespace: $ns ==="
  oc get secrets -n $ns --field-selector type=kubernetes.io/tls -o json | \
  jq -r '.items[] | .metadata.name + ": " + (.data."tls.crt" // "" | @base64d | "openssl x509 -enddate -noout" | @sh)' | \
  while read line; do
    eval echo $line
  done
done
```

```bash ignore-test
# Verificar certificado de um pod
oc exec <pod-name> -- openssl s_client -connect <host>:<port> -showcerts
```

```bash
# Verificar trust bundle
oc get configmap -n openshift-config-managed
```

```bash
# Ver CA bundle
# oc get configmap <configmap-name> -n <namespace> -o yaml
oc get configmap default-ingress-cert -n openshift-config-managed -o yaml
```

### Renovar Certificados
```bash
# Certificados são renovados automaticamente
# Forçar renovação deletando secrets (serão recriados)
```

```bash ignore-test
# CUIDADO: Isso pode causar downtime!
oc delete secret <secret-name> -n <namespace>
```

```bash ignore-test
# Aguardar recreação
oc get secret <secret-name> -n <namespace>
```

```bash ignore-test
# Verificar novo certificado
oc get secret <secret-name> -n <namespace> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout
```

### CSR Não Aprovado Automaticamente
```bash ignore-test
# Ver por que CSR não foi aprovado
oc describe csr <csr-name>
```

```bash ignore-test
# Verificar CSR signer
oc get csr <csr-name> -o jsonpath='{.spec.signerName}'
```

```bash ignore-test
# Verificar usages
oc get csr <csr-name> -o jsonpath='{.spec.usages}'
```

```bash ignore-test
# Ver username que criou
oc get csr <csr-name> -o jsonpath='{.spec.username}'
```

```bash ignore-test
# Logs do cluster-signing-controller
oc logs -n openshift-kube-controller-manager <pod-name> | grep csr
```

### Bulk CSR Operations
```bash ignore-test
# Script para aprovar CSRs de nodes periodicamente
cat > /tmp/approve-csrs.sh << 'EOF'
#!/bin/bash
while true; do
  echo "=== $(date) ==="
  oc get csr -o json | jq -r '.items[] | select(.status == {}) | select(.spec.username | contains("system:node:")) | .metadata.name' | xargs --no-run-if-empty oc adm certificate approve
  sleep 10
done
EOF
```

```bash ignore-test
chmod +x /tmp/approve-csrs.sh
/tmp/approve-csrs.sh &
```

```bash ignore-test
# Verificar CSRs antigos para limpeza
oc get csr -o json | jq -r '.items[] | select(.metadata.creationTimestamp < "'$(date -d '7 days ago' -Ins --utc | sed 's/+00:00/Z/')'" ) | .metadata.name' | xargs oc delete csr
```

---

## 📚 Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- [Certificate management](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance/certificate-management)

---

## 📖 Navegação

- [← Anterior: Nodes e Machine](18-nodes-machine.md)
- [→ Próximo: Cluster Networking](20-cluster-networking.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
