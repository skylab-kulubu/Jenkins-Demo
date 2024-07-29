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
ardından grup değerlerini güncellemek için aşağıdaki komutu çalıştırın
```bash
newgrp docker
```

Sisteminiz Docker kullanımı için hazır!
