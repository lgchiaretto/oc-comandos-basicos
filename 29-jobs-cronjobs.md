#  Jobs e CronJobs

Este documento contém comandos para gerenciar Jobs e CronJobs no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Jobs](#jobs)
3. [CronJobs](#cronjobs)
4. [Troubleshooting](#troubleshooting)
5. [Documentação Oficial](#documentação-oficial)
6. [Navegação](#navegação)
---

## Jobs

### Criar Jobs
**Ação:** Criar novo Job para execução única de tarefa
**Exemplo:** `oc create job <job-name> --image=quay.io/chiaretto/netshoot -- echo "Hello World"`
```

```bash
oc create job test-app-job --image=quay.io/chiaretto/netshoot -- echo "Hello World"
```

**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: test-app-job-yaml
spec:
  template:
    spec:
      containers:
      - name: job
        image: quay.io/chiaretto/netshoot
        command: ["echo", "Hello from Job"]
      restartPolicy: Never
  backoffLimit: 4
EOF
```

**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: retry-job
spec:
  template:
    spec:
      containers:
      - name: job
        image: quay.io/chiaretto/netshoot
        command: ["sh", "-c", "exit 1"]  # Vai falhar
      restartPolicy: Never
  backoffLimit: 3  # Tentar 3 vezes
EOF
```

### Gerenciar Jobs
**Ação:** Listar jobs
```

```bash
oc get jobs
```

**Ação:** Exibir detalhes completos do job
**Exemplo:** `oc describe job <job-name>`
```

```bash
oc describe job test-app-job
```

**Ação:** Exibir logs do pod especificado
```

```bash ignore-test
oc logs job/test-app-job
```

**Ação:** Listar pods filtrados por label
```

```bash
oc get pods -l job-name=test-app-job
```

**Ação:** Deletar o job especificado
**Exemplo:** `oc delete job <job-name>`
```

```bash
oc delete job test-app-job
```

**Ação:** Deletar job e aguardar exclusão de recursos dependentes
**Exemplo:** `oc delete job <job-name> --cascade=foreground`
```

```bash ignore-test
oc delete job test-app --cascade=foreground
```

### Jobs Paralelos
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: parallel-job
spec:
  parallelism: 3  # 3 pods simultâneos
  completions: 9  # Total de 9 execuções
  template:
    spec:
      containers:
      - name: job
        image: quay.io/chiaretto/netshoot
        command: ["sh", "-c", "echo Processing && sleep 5"]
      restartPolicy: Never
EOF
```

**Ação:** Monitorar
**Exemplo:** `oc get job <job-name>`
```

```bash ignore-test
oc get job parallel-job
oc get pods -l job-name=parallel-job
```

### Jobs com TTL
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash ignore-test
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: ttl-job
spec:
  ttlSecondsAfterFinished: 100  # Deletar após 100s
  template:
    spec:
      containers:
      - name: job
        image: quay.io/chiaretto/netshoot
        command: ["echo", "This job will be deleted"]
      restartPolicy: Never
EOF
```

---

##  CronJobs

### Criar CronJobs
**Ação:** Criar novo Job para execução única de tarefa
**Exemplo:** `oc create cronjob <job-name> --image=quay.io/chiaretto/netshoot --schedule="*/5 * * * *" -- echo "Hello every 5 minutes"`
```

```bash
oc create cronjob test-app-job --image=quay.io/chiaretto/netshoot --schedule="*/5 * * * *" -- echo "Hello every 5 minutes"
```

**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash ignore-test
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: CronJob
metadata:
  name: test-app
spec:
  schedule: "0 2 * * *"  # Diariamente às 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: job
            image: quay.io/chiaretto/netshoot
            command: ["sh", "-c", "date; echo Hello from CronJob"]
          restartPolicy: OnFailure
EOF
```

### Gerenciar CronJobs
**Ação:** Listar cronjobs
```

```bash
oc get cronjobs
oc get cj
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe cronjob <job-name>`
```

```bash ignore-test
oc describe cronjob test-app-job
```

**Ação:** Ver jobs criados pelo cronjob
```

```bash ignore-test
oc get jobs -l cronjob=<cronjob-name>
```

**Ação:** Ver último job
```

```bash ignore-test
oc get jobs --sort-by=.metadata.creationTimestamp | grep <cronjob-name> | tail -1
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch cronjob <job-name> -p '{"spec":{"suspend":true}}'`
```

```bash ignore-test
oc patch cronjob test-app-job -p '{"spec":{"suspend":true}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch cronjob <job-name> -p '{"spec":{"suspend":false}}'`
```

```bash ignore-test
oc patch cronjob test-app-job -p '{"spec":{"suspend":false}}'
```

**Ação:** Deletar o recurso especificado
**Exemplo:** `oc delete cronjob <job-name>`
```

```bash
oc delete cronjob test-app-job
```

**Ação:** Deletar recurso e aguardar exclusão de recursos dependentes
**Exemplo:** `oc delete cronjob <job-name> --cascade=foreground`
```

```bash ignore-test
oc delete cronjob test-app --cascade=foreground
```

### CronJob Avançado
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-cronjob
spec:
  schedule: "0 3 * * *"  # 3 AM diariamente
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  concurrencyPolicy: Forbid  # Não permitir execução simultânea
  startingDeadlineSeconds: 300  # Começar até 5 min após schedule
  suspend: false
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: registry.redhat.io/rhel8/support-tools
            command:
            - /bin/sh
            - -c
            - |
              echo "Starting backup at \$(date)"
              # Seu script de backup aqui
              echo "Backup completed at \$(date)"
          restartPolicy: OnFailure
      backoffLimit: 2
      activeDeadlineSeconds: 3600  # Timeout de 1 hora
EOF
```

### Concurrency Policy
**Ação:** Allow - Permitir jobs simultâneos (padrão)
```

```bash
concurrencyPolicy: Allow
```

**Ação:** Forbid - Não permitir simultâneos (pula se ainda rodando)
```

```bash
concurrencyPolicy: Forbid
```

**Ação:** Replace - Cancela job atual e inicia novo
```

```bash
concurrencyPolicy: Replace
```

---

## Troubleshooting

### Debug de Jobs
**Ação:** Exibir job "test-app-job" em formato YAML
**Exemplo:** `oc get job <job-name> -o yaml`
```

```bash ignore-test
oc get job test-app-job -o yaml
```

**Ação:** Exibir job "test-app-job" em formato JSON
**Exemplo:** `oc get job <job-name> -o jsonpath='{.status.conditions}'`
```

```bash ignore-test
oc get job test-app-job -o jsonpath='{.status.conditions}'
```

**Ação:** Exibir detalhes completos do job
**Exemplo:** `oc describe job <job-name>`
```

```bash ignore-test
oc describe job test-app-job
```

**Ação:** Exibir logs da instância anterior do container (após crash)
```

```bash ignore-test
oc logs $POD --previous
```

**Ação:** Listar eventos filtrados por campo específico
```

```bash ignore-test
oc get events --field-selector involvedObject.name=test-app-job
```

### Debug de CronJobs
**Ação:** Exibir recurso "test-app-job" em formato YAML
**Exemplo:** `oc get cronjob <job-name> -o yaml`
```

```bash ignore-test
oc get cronjob test-app-job -o yaml
```

**Ação:** Exibir recurso "test-app-job" em formato JSON
**Exemplo:** `oc get cronjob <job-name> -o jsonpath='{.status.lastScheduleTime}'`
```

```bash ignore-test
oc get cronjob test-app-job -o jsonpath='{.status.lastScheduleTime}'
```

**Ação:** Criar job manual para testar
```

```bash ignore-test
oc create job test-job --from=cronjob/<cronjob-name>
```

**Ação:** Listar recurso ordenados por campo específico
```

```bash ignore-test
oc get jobs --sort-by=.metadata.creationTimestamp -l cronjob=test-app-job
```

**Ação:** Listar recurso ordenados por campo específico
```

```bash ignore-test
LAST_JOB=$(oc get jobs --sort-by=.metadata.creationTimestamp -l cronjob=test-app-job -o name | tail -1)
oc logs $LAST_JOB
```

### Jobs Travados
**Ação:** Exibir recurso em formato JSON
```

```bash
oc get jobs -o json | jq -r '.items[] | select(.status.active > 0) | "\(.metadata.name) - \(.metadata.creationTimestamp)"'
```

**Ação:** Exibir recurso em formato JSON
```

```bash ignore-test
oc get jobs -o json | jq -r '.items[] | select(.status.completionTime != null) | select(.status.completionTime < "'$(date -d '7 days ago' -Ins --utc | sed 's/+00:00/Z/')'" ) | .metadata.name' | xargs oc delete job
```

**Ação:** Ou com script
```

```bash ignore-test
for job in $(oc get jobs -o name); do
  STATUS=$(oc get $job -o jsonpath='{.status.succeeded}')
  if [ "$STATUS" == "1" ]; then
    echo "Deleting completed job: $job"
    oc delete $job
  fi
done
```

---

### Limpeza de Recursos
```bash ignore-test
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cleanup-old-pods
spec:
  schedule: "0 */6 * * *"  # A cada 6 horas
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: cleanup-sa
          containers:
          - name: cleanup
            image: registry.redhat.io/openshift4/ose-cli:latest
            command:
            - /bin/bash
            - -c
            - |
              echo "Starting cleanup..."
              # Deletar pods completados
              oc delete pods --field-selector=status.phase==Succeeded -A
              # Deletar jobs antigos
              oc get jobs -A -o json | jq -r '.items[] | select(.status.completionTime != null) | "\(.metadata.namespace) \(.metadata.name)"' | while read ns name; do
                oc delete job $name -n $ns
              done
              echo "Cleanup completed"
          restartPolicy: OnFailure
EOF
```
## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes - Working with jobs</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications - Jobs and CronJobs</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes</a>
---

---

## Navegação

- [← Anterior: Patch e Edit](28-patch-edit.md)
- [→ Próximo: Operators e Operandos](30-operators-operandos.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
