# Certificados e CSR

Este documento contém comandos para gerenciar certificados e Certificate Signing Requests no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [CSR (Certificate Signing Requests)](#csr-(certificate-signing-requests))
3. [Certificados do Cluster](#certificados-do-cluster)
4. [Certificados de API](#certificados-de-api)
5. [Troubleshooting](#troubleshooting)
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## CSR (Certificate Signing Requests)

### Visualizar CSRs
**Listar Certificate Signing Requests pendentes**

```bash
oc get csr
```

**CSRs pendentes**

```bash ignore-test
oc get csr | grep Pending
```

**Listar certificate signing request com informações detalhadas**

```bash
oc get csr -o wide
```

**Ver CSR específico**

```bash ignore-test
oc describe csr <csr-name>
```

**Ver certificado em CSR**

```bash ignore-test
oc get csr <csr-name> -o jsonpath='{.spec.request}' | base64 -d | openssl req -text -noout
```

### Aprovar CSRs
**Aprovar CSR específico**

```bash ignore-test
oc adm certificate approve <csr-name>
```

**Aprovar Certificate Signing Request (CSR)**

```bash ignore-test
oc get csr -o name | xargs oc adm certificate approve
```

**Exibir certificate signing request em formato JSON**

```bash ignore-test
oc get csr -o json | jq -r '.items[] | select(.status == {} ) | .metadata.name' | xargs oc adm certificate approve
```

**Exibir certificate signing request em formato JSON**

```bash ignore-test
oc get csr -o json | jq -r '.items[] | select(.spec.username | contains("system:node:worker")) | select(.status == {}) | .metadata.name' | xargs oc adm certificate approve
```

### Negar CSRs
**Negar CSR**

```bash ignore-test
oc adm certificate deny <csr-name>
```

**Deletar CSR**

```bash ignore-test
oc delete csr <csr-name>
```

### Monitorar CSRs
**Listar Certificate Signing Requests pendentes**

```bash
oc get csr
```

**Listar certificate signing request ordenados por campo específico**

```bash
oc get csr --sort-by='.metadata.creationTimestamp'
```

**Exibir certificate signing request em formato JSON**

```bash ignore-test
oc get csr -o json | jq -r '.items[] | .status | keys[0] // "Pending"' | sort | uniq -c
```

---

## Certificados do Cluster

### API Server Certificates
**Ver certificados do API server**

```bash
oc get secret -n openshift-kube-apiserver
```

**Certificado do serving**

```bash
oc get secret -n openshift-kube-apiserver | grep serving
```

**Ver validade do certificado**

```bash ignore-test
oc get secret <secret-name> -n openshift-kube-apiserver -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout
```

**Ver detalhes do certificado**

```bash ignore-test
oc get secret <secret-name> -n openshift-kube-apiserver -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

### Ingress Certificates
**Certificado padrão do ingress**

```bash
oc get secret -n openshift-ingress
```

**Exibir secret "apps-cert" em formato YAML**

```bash
oc get secret apps-cert -n openshift-ingress -o yaml
```

**Exibir secret "apps-cert" em formato JSON**

```bash
oc get secret apps-cert -n openshift-ingress -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout
```

**Substituir certificado do ingress**

```bash ignore-test
oc create secret tls custom-certs --cert=<cert-file> --key=<key-file> -n openshift-ingress
```


```bash
oc patch ingresscontroller default -n openshift-ingress-operator --type=merge -p '{"spec":{"defaultCertificate":{"name":"apps-cert"}}}'
```

### Service Serving Certificates
**Listar recurso filtrados por campo específico**

```bash
oc get secrets --field-selector type=kubernetes.io/tls
```

**Ver secret específico**

```bash ignore-test
oc get secret <secret-name> -o yaml
```

**Anotar service para gerar certificado automático**

```bash ignore-test
oc annotate service <service-name> service.beta.openshift.io/serving-cert-secret-name=<secret-name>
```

**Verificar certificado gerado**

```bash ignore-test
oc get secret <secret-name>
```

---

## Certificados de API

### Custom API Certificates
**Configurar certificado customizado para API**

```bash ignore-test
oc create secret tls api-certs --cert=<cert-file> --key=<key-file> -n openshift-config
```

**Aplicar certificado**

```bash ignore-test
oc patch apiserver cluster --type=merge -p '{"spec":{"servingCerts":{"namedCertificates":[{"names":["<api-hostname>"],"servingCertificate":{"name":"api-certs"}}]}}}'
```

**Exibir recurso "cluster" em formato YAML**

```bash
oc get apiserver cluster -o yaml
```

### OAuth Certificates
**Configurar certificado para OAuth**

```bash ignore-test
oc create secret tls oauth-certs --cert=<cert-file> --key=<key-file> -n openshift-config
```

**Aplicar**

```bash ignore-test
oc patch oauths cluster --type=merge -p '{"spec":{"componentRoutes":[{"hostname":"<oauth-hostname>","name":"oauth-openshift","namespace":"openshift-authentication","servingCertKeyPairSecret":{"name":"oauth-certs"}}]}}'
```

---

## Troubleshooting

### Problemas com Certificados
**Verificar expiração de todos os certificados importantes**

```bash ignore-test
for ns in openshift-kube-apiserver openshift-ingress openshift-authentication; do
  echo "=== Namespace: $ns ==="
  oc get secrets -n $ns --field-selector type=kubernetes.io/tls -o json | \
  jq -r '.items[] | .metadata.name + ": " + (.data."tls.crt" // "" | @base64d | "openssl x509 -enddate -noout" | @sh)' | \
  while read line; do
    eval echo $line
  done
done
```

**Verificar certificado de um pod**

```bash ignore-test
oc exec my-pod -- openssl s_client -connect <host>:<port> -showcerts
```

**Verificar trust bundle**

```bash
oc get configmap -n openshift-config-managed
```

**Exibir recurso "default-ingress-cert" em formato YAML**

```bash
oc get configmap default-ingress-cert -n openshift-config-managed -o yaml
```

### Renovar Certificados
```bash
# Certificados são renovados automaticamente
# Forçar renovação deletando secrets (serão recriados)
```
* CUIDADO: Isso pode causar downtime!

```bash ignore-test
oc delete secret <secret-name> -n <namespace>
```

**Aguardar recreação**

```bash ignore-test
oc get secret <secret-name> -n <namespace>
```

**Verificar novo certificado**

```bash ignore-test
oc get secret <secret-name> -n <namespace> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout
```

### CSR Não Aprovado Automaticamente
**Ver por que CSR não foi aprovado**

```bash ignore-test
oc describe csr <csr-name>
```

**Verificar CSR signer**

```bash ignore-test
oc get csr <csr-name> -o jsonpath='{.spec.signerName}'
```

**Verificar usages**

```bash ignore-test
oc get csr <csr-name> -o jsonpath='{.spec.usages}'
```

**Ver username que criou**

```bash ignore-test
oc get csr <csr-name> -o jsonpath='{.spec.username}'
```

**Logs do cluster-signing-controller**

```bash ignore-test
oc logs -n openshift-kube-controller-manager <pod-name> | grep csr
```

### Bulk CSR Operations
**Script para aprovar CSRs de nodes periodicamente**

```bash ignore-test
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

**Exibir certificate signing request em formato JSON**

```bash ignore-test
oc get csr -o json | jq -r '.items[] | select(.metadata.creationTimestamp < "'$(date -d '7 days ago' -Ins --utc | sed 's/+00:00/Z/')'" ) | .metadata.name' | xargs oc delete csr
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance">Security and compliance - Certificate management</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization">Authentication and authorization</a>
---


## Navegação

- [← Anterior: Nodes e Machine](18-nodes-machine.md)
- [→ Próximo: Cluster Networking](20-cluster-networking.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
