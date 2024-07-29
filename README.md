<div align="center">
  <img src="https://img.shields.io/badge/Jenkins-49728B?style=for-the-badge&logo=jenkins&logoColor=white"> </img><img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"></img> <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white"></img> <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"></img>
</div>

# Jenkins CI/CD Demo

[Medium](https://medium.com/@farukomererdem2003/docker-jenkins-i%CC%87le-ci-cd-pipeline-olu%C5%9Fturmak-6f58d83f267b) yazısından okumak için.

## Docker Kurulumu
Eğer sisteminizde önceden `sudo apt-get install docker.io`, `sudo dnf install docker` ve `sudo yum install docker` gibi komutları kullanarak paket yöneticisi ile Docker yüklenmiş bir sistemde çalışıyorsanız aşağıdaki komut ile Docker'ı sisteminizden tamamen silin.

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```
Bu komut yalnızca Debian tabanlı sistemlerde çalışacaktır! Diğer Linux dağıtımları için;

RHEL
```bash
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine \
                  podman \
                  runc
```

Fedora
```bash
sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
```

Ardından aşağıdaki komutu veya Docker resmi kurulum scriptini kullanabilirsiniz, kurulum scripti için;

```bash
curl https://get.docker.com | bash
```
Bütün kurulumlar gerçekleştikten sonra kullanıcınızı aşağıdaki komut ile `docker` grubuna ekleyerek `docker` komutunu kullanabilmesini sağlayın.
```bash
sudo usermod -aG docker $USER
```

> -a etiketi üyesi olunan gruplara ekleme yapmamızı sağlamakta.
> -G kullanıcının dahil olduğu grup değerini değiştirmemizi sağlamakta.

ardından grup değerlerini güncellemek için aşağıdaki komutu çalıştırın
```bash
newgrp docker
```

Sisteminiz Docker kullanımı için hazır!

## Jenkins Kurulumu
Jenkins'i Docker konteynerı olarak çalıştıracağız fakat aynı makineye Jenkins ajanı da kuracağımız için aşağıdaki komut ile Debian/Ubuntu tabanlı makinelerinize Java Runtime Environment kurulumunu gerçekleştirebilirsizin.
```bash
sudo apt install default-jre
```

Fedora kurulumu için [kaynağı](https://docs.fedoraproject.org/en-US/quick-docs/installing-java/) inceleyebilirsiniz.

Adından Jenkins için bir kullanıcı oluşturuyoruz, bu sayede `Least Privilege` yasasına uyarak sistemi güvenli çalıştırmaya devam edeceğiz.
```bash
sudo useradd -m -G docker -s /bin/bash -U jenkins &&\
sudo passwd jenkins
```

> -m kullanıcı için ev dizini açmak istediğimzi belirtir.
> -G kullanıcıyı oluştururken dahil etmek istediğimiz grupları belirtir
> -s kullanıcının default shell değerini atar
> -U kullanıcı oluşturulurken kullanıcının adıyla aynı ada sahip bir kullanıcı grubu oluşturur.

Son olarak Jenkins'i sistemimize Docker kullanarak yükleyelim

```bash
docker pull jenkins/jenkins:latest
```
> `docker pull` komutu Docker Hub üzerinden image çekeceğimizi belirtir
> `jenkins/jenkins` kullanacağımız image değeridir
> `latest` en son sürüm imagei kullanmak istediğimizi belirtir, herhangi bir sürüm belirtmek istiyorsanız image isminden sonra `:` yazıp sürüm değerini belirtebilirisiniz.

Jenkins'in diğer versiyonları için [Jenkins Docker Hub](https://hub.docker.com/r/jenkins/jenkins) sayfasına göz atabilirsiniz.

Jenkins'i çalıştırmak için aşağıdaki komutu kullanabilirisiniz;
```bash
docker run \
-p 8080:8080 \
-p 50000:50000 \
--restart=on-failure \
jenkins/jenkins:latest
```
veya `docker compose` kullanacaksanız
```YAML
services:
    jenkins:
        image: jenkins:latest
        ports:
            - "8080:8080"
            - "50000:50000"
        restart-policy:
            condition: on-failure
            delay: 5s
```
