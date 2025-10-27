# Gerenciamento de Aplicações

Este documento contém comandos para criar e gerenciar aplicações no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Criação de Aplicações](#criação-de-aplicações)
3. [Gerenciamento](#gerenciamento)
4. [Informações e Status](#informações-e-status)
5. [Atualização de Imagens](#atualização-de-imagens)
6. [Permissões e Validações](#permissões-e-validações)
7. [⏳ Aguardar Condições](#⏳-aguardar-condições)
8. [Documentação Oficial](#documentação-oficial)
9. [Navegação](#navegação)
---

## Criação de Aplicações

### A partir de Imagem Docker
```markdown
**Ação:** Criar aplicação a partir de imagem
```

```bash ignore-test
oc new-app <nome-da-imagem>
```

```markdown
**Ação:** Exemplo com imagem pública
```

```bash ignore-test
oc new-app nginx
```

```markdown
**Ação:** Criar nova aplicação a partir de imagem ou código fonte
```

```bash ignore-test
oc new-app myregistry.com/myapp:latest
```

```markdown
**Ação:** Criar aplicação com nome customizado
```

```bash ignore-test
oc new-app nginx --name=meu-nginx
```

```markdown
**Ação:** Exemplo com httpd
**Exemplo:** `oc new-app httpd:latest --name=test-app -n <namespace>`
```

```bash
oc new-app httpd:latest --name=test-app -n development
```

### A partir de Repositório Git
```markdown
**Ação:** Criar aplicação a partir de repositório Git
```

```bash ignore-test
oc new-app <url-do-repositorio-git>
```

```markdown
**Ação:** Especificando branch
```

```bash ignore-test
oc new-app <url-do-repositorio-git>#<branch>
```

```markdown
**Ação:** Exemplo prático de new-app usando s2i
```

```bash
oc new-app https://github.com/lgchiaretto/s2i-chiaretto.git --name=s2i-chiaretto
```

### Com Variáveis de Ambiente
```markdown
**Ação:** Criar aplicação com variáveis
```

```bash ignore-test
oc new-app <imagem> -e VAR1=valor1 -e VAR2=valor2
```

```markdown
**Ação:** Exemplo
```

```bash ignore-test
oc new-app mysql -e MYSQL_USER=user -e MYSQL_PASSWORD=pass
```

### A partir de Template
```markdown
**Ação:** Listar templates disponíveis no namespace openshift
```

```bash
oc get templates -n openshift
```

```markdown
**Ação:** Criar a partir de template
```

```bash ignore-test
oc new-app --template=<nome-do-template>
```

```markdown
**Ação:** Criar aplicação a partir de template
```

```bash ignore-test
oc new-app --template=mysql-persistent -p MYSQL_USER=admin
```

### Com Estratégia de Build
```markdown
**Ação:** Especificar estratégia de build
```

```bash ignore-test
oc new-app <url-git> --strategy=docker
```
```bash  ignore
oc new-app <url-git> --strategy=source
```

```markdown
**Ação:** Criar aplicação com nome customizado
```

```bash ignore-test
oc new-app . --name=test-app
```

---

## Gerenciamento

### Listar Recursos
```markdown
**Ação:** Listar todos os recursos principais do namespace
```

```bash
oc get all
```

```markdown
**Ação:** Listar recurso filtrados por label
```

```bash
oc get all -l app=test-app
```

```markdown
**Ação:** Listar todos os deployments do namespace
```

```bash
oc get deployment
```

```markdown
**Ação:** Listar todos os services do namespace atual
```

```bash
oc get svc
```

```markdown
**Ação:** Listar todas as routes expostas no namespace
```

```bash
oc get routes
```

```markdown
**Ação:** Listar routes em um namespace específico
```

```bash
oc get routes -n development
```

```markdown
**Ação:** Listar todas as ImageStreams do projeto
```

```bash
oc get is
```

```markdown
**Ação:** Listar ImageStreams em um projeto
```

```bash
oc get is -n development
```

### Deletar Aplicações
```markdown
**Ação:** Deletar recurso que correspondem ao seletor de label
```

```bash ignore-test
oc delete all -l app=test-app
```

```markdown
**Ação:** Deletar recurso que correspondem ao seletor de label
```

```bash ignore-test
oc delete all --selector app=test-app
```

```markdown
**Ação:** Deletar o recurso especificado
**Exemplo:** `oc delete deployment <deployment-name>`
```

```bash ignore-test
oc delete deployment test-app
```

### Expor Aplicação
```markdown
**Ação:** Criar route para expor service externamente
**Exemplo:** `oc expose service <service-name>`
```

```bash ignore-test
oc expose service test-app
```

```markdown
**Ação:** Criar route com hostname customizado para o service
**Exemplo:** `oc expose service <service-name> --hostname=app.example.com`
```

```bash ignore-test
oc expose service test-app --hostname=app.example.com
```

```markdown
**Ação:** Criar route com terminação TLS edge (TLS terminado no router)
**Exemplo:** `oc create route <route-name> --service=test-app`
```

```bash
oc create route edge --service=test-app
```

---

## Informações e Status

### Status do Projeto
```markdown
**Ação:** Exibir visão geral dos recursos do projeto atual
```

```bash
oc status
```

```markdown
**Ação:** Status de um projeto específico
**Exemplo:** `oc status -n <namespace>`
```

```bash
oc status -n development
```

### Descrever Recursos
```markdown
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe deployment <deployment-name>`
```

```bash
oc describe deployment test-app
```

```markdown
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe deployment <deployment-name> -n <namespace>`
```

```bash
oc describe deployment test-app -n development
```

---

## Atualização de Imagens

### Atualizar Imagem do Deployment
```markdown
**Ação:** Atualizar imagem do container no deployment/pod
**Exemplo:** `oc set image <resource-name>/test-app httpd=httpd:2.4 -n <namespace>`
```

```bash
oc set image deployment/test-app httpd=httpd:2.4 -n development
```

```markdown
**Ação:** Atualizar imagem do container no deployment/pod
**Exemplo:** `oc set image <resource-name>/test-app container1=image1:tag container2=image2:tag`
```

```bash ignore-test
oc set image deployment/test-app container1=image1:tag container2=image2:tag
```

### Patch de Deployment
```markdown
**Ação:** Aplicar merge patch ao recurso (mescla alterações)
**Exemplo:** `oc patch deployment <deployment-name> -n <namespace> --type=merge -p '{"spec":{"replicas":3}}'`
```

```bash
oc patch deployment test-app -n development --type=merge -p '{"spec":{"replicas":3}}'
```

```markdown
**Ação:** Aplicar merge patch ao recurso (mescla alterações)
**Exemplo:** `oc patch deployment <deployment-name> -n <namespace> --type=merge -p '{"spec":{"template":{"spec":{"containers":[{"name":"httpd","image":"httpd:latest"}]}}}}'`
```

```bash
oc patch deployment test-app -n development --type=merge -p '{"spec":{"template":{"spec":{"containers":[{"name":"httpd","image":"httpd:latest"}]}}}}'
```

---

## Permissões e Validações

### Verificar Permissões
```markdown
**Ação:** Verificar se usuário tem permissão para executar ação específica
```

```bash
oc auth can-i create deployments
```

```markdown
**Ação:** Verificar se usuário tem permissão para executar ação específica
**Exemplo:** `oc auth can-i create deployments -n <namespace>`
```

```bash
oc auth can-i create deployments -n development
```

```markdown
**Ação:** Verificar se usuário tem permissão para executar ação específica
**Exemplo:** `oc auth can-i delete pods -n <namespace>`
**Ação:** oc auth can-i get secrets -n <namespace>
```

```bash
oc auth can-i delete pods -n development
oc auth can-i get secrets -n development
```

---

## ⏳ Aguardar Condições

### Wait para Deployment
```markdown
**Ação:** Aguardar deployment ficar disponível
**Exemplo:** `oc wait --for=condition=available deployment/<deployment-name>`
```

```bash
oc wait --for=condition=available deployment/test-app
```

```markdown
**Ação:** Aguardar deployment ficar disponível
**Exemplo:** `oc wait --for=condition=available --timeout=60s deployment/<deployment-name>`
```

```bash
oc wait --for=condition=available --timeout=60s deployment/test-app
```

```markdown
**Ação:** Aguardar deployment ficar disponível
**Exemplo:** `oc wait --for=condition=available --timeout=60s deployment/test-app -n <namespace>`
```

```bash
oc wait --for=condition=available --timeout=60s deployment/test-app -n development
```
## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/developer-cli-odo">Developer CLI (odo)</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/deployments">Deployments</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images">Images - Using templates</a>
---

---

## Navegação

- [← Anterior: Projetos](02-projetos.md)
- [→ Próximo: Pods e Containers](04-pods-containers.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
