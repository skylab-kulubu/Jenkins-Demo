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
--name jenkins \
jenkins/jenkins:latest
```
veya `docker compose` kullanacaksanız
```YAML
services:
    jenkins:
        image: jenkins:latest
        container_name: jenkins
        ports:
            - "8080:8080"
            - "50000:50000"
        restart-policy:
            condition: on-failure
            delay: 5s
```

### Jenkins Arayüzüne Giriş
İlk giriş için kullanıcı şifresini öğrenmek için;
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

> `docker exec` çalışan Docker konteynerında shell komutu çalıştırmamızı sağlar.

> `jenkins` komutumuzda konteynerin adını belirtmekte, bunun yerine `docker ps` komutunu çalıştırdıktan sonra Jenkins konteynerinin `Image ID` değerini de kullanabilirsiniz.

> `cat /var/jenkins_home/secrets/initialAdminPassword` ise tek seferlik yönetici şifremizi okumamızı sağlamakta.
Aşağıdaki görsellerdeki adımları izleyerek kurulumu ve ajan kurulumunu gerçekleştirebilirsiniz. Fakat herşeydene önce `SSH` servisinin çalışıp çalışmadığını kontrol edin.
`SSH` servisini çalışma durumunu kontrol etmek için;
```bash
sudo systemctl status ssh
```
`SSH` servisini çalıştırmak için;
```bash
sudo systemctl start ssh
```
`SSH` servisini başlangıçta otomatik başlamasını sağlamak için;
```bash
sudo sytemctl enable --now ssh
```

#### Jenkins Ajan Kurulumu

<img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*-v_EEHzFTlJeyLeCUQeiXg.png"></img>

<img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*8aov0-hixvK1aSnFePKHvA.png"></img>

<img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*ZqUR56PwBn1pCzHn__PVEw.png"></img>


Yukarıdaki görselde ajanımızın ismini `docker-agent` olarak belirliyoruz, ilerleyen süreçte bu değer sistemimizin tutarlılığı için önemli.

Oluşturacağımız `agent` için isim koyduktan sonra `Label` bölümünü `agent` için koyduğunuz isimle aynı yapıp `Launch Method` seçeneğini `Launch agents via SSH' seçeneğini seçip ana makinemizin IP adresi ile ana makinemizde oluşturduğumuz jenkins kullanıcının kullanıcı adı ve şifresini `Credidentals` seçeneğinin altında bulunan Add butonuna tıkladıktan sonra girip `Host Verification Strategy` seçeneğini `Non Verifying Verification Strategy` olarak seçiyoruz.

<img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*YIHNtxd7wvXmKU39rF8SWA.png"></img>

<img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*PTPN8amklp6gufRDvST7sQ.png"></img>

Geri kalan seçenekleri ellemeden `Save` butonuna tıklayıp `agent` işlemini tamamlıyoruz.

Jenkins için ajanımız hazır.

#### Jenkins Pipeline (CI/CD Hattı) Hazırlama

Jenkins ana sayfasına gidip `New Item` butonuna tıklıyoruz. Karşımıza çıkan sayfada projemiz için oluşturmak istediğiniz `Pipeline` ismini ve proje türünü Pipeline olarak seçip devam ediyoruz.

<img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*XvLU09gyRlizzMYL1LQF9w.png"></img>

Pipeline konfigürasyon sayfasında ilk başta Build Triggers başlığının altındaki seçenekleri ellememenizi tavsiye ediyorum fakat ardından Jenkins kullanma amacınız olacak bu seçeneklere değineceğiz.

Pipeline başlığının altında bulunan `Definition` seçeneğini örnek projemizde `Pipeline Script From SCM` olarak seçeceğiz fakat siz kendi projenizde `Pipeline Script` olarak seçerek devam edebilirsiniz, tek farklı scripti `Github` Projesinden çekmiyor oluşunuz olacak. `SCM` seçeneğini `Git` olarak seçtikten sonra `Github Repo URL`’nizi gerekli yere girip, eğer Private Repo ise Github giriş bilgilerinizi de ekledikten sonra, `branch` ismini de değiştirmeniz gerekiyorsa düzenledikten sonra `Save` butonuna basıp devam edebilirsiniz.
Bu repositorynin içerisinde bulunan `Dockerfile`, `Jenkinsfile`, `docker-compose.yml` dosyalarından faydalanarak bir test projesi ayağa kaldırabilirsiniz.

#### Dockerfile'ı İnceleyelim

```Dockerfile
FROM python

RUN apt-get update -y;apt-get upgrade -y

RUN mkdir -p /var/www/html

WORKDIR /var/www/html

COPY . . 

EXPOSE 80

CMD ["python3","myscript.py","-p","80"]
```
> `FROM` kullanacağımız Docker imageını belirlemekte

> `RUN` çalıştırılacak konteyner içerisinde komut çalıştırmamızı sağlamakta

> `WORKDIR` komutların çalıştırılacağı dosya dizinini belirlemekte, shell içerisinde `cd` komutuyla eşdeğer görebilirisiniz.

> `COPY` belirlenen dizindeki dosyaları konteynerın belirlenen dizinine kopyalamakta, burada mevcut dizindeki dosyaları `WORKDIR` ile belirlenen konteyner dizinine kopyalamaktayız.

> `EXPOSE` belirlenen portu dışarıdan erişilebilir yapmakta

> `CMD` konteyner başlatıldığında çalıştırılacak ilk komutu belirlemekte.

#### docker-compose.yml Dosyasını İnceleyelim

```YAML
services:
  www:
    build: .
    ports:
      - "80:80"
    networks:
      - devops
networks:
  devops:
    driver: bridge
```

> `services` çalıştırılacak konteynerlerin belirleneceği başlık

> `networks` oluşturulacak Docker ağlarının tanımlanacağı başlık

>  `www` web sunucumuzun ismi ve konteyner için başlık

> `build` Dockerfile'ı bulacağı dizini belirtlir

> `ports` port yönlendirmelerinin tanımlandığı başlıktır

> `networks` konteynerin dahil olacağı docker ağlarının belirlendiği başlıktır

Docker compose ile çalıştıracağımız konteyneri Docker CLI ile çalıştırmak isteseydik komtuk aşağıdaki gibi olacaktı;
```bash
docker run -p 80:80 --network=devops --name=jenkins-test-www <docker image ismi>
```
Docker compose bizim için otomatik olarak hem `Build` hem `Run` işlevini yerine getirmekte.

#### Jenkinsfile'ı İnceleyelim
Başlamadan önce dikkat! repository içerisindeki Jenkinsfile içerisinde düzenlemeler yapmalısınız, yorum olarka işaretleniş satırları düzenlemelisin!
```groovy
pipeline {
  agent {
    label "docker-agent"
  }
  stages {
    stage('Stop and Remove Existing Containers') {
      steps{
        sh 'docker compose down'
      }
    }
    stage ('Run Docker Compose') {
      steps{
        sh 'docker compose up -d --build'
      }
    }
  }
}
```

> `pipeline` bir pipeline'ın olduğunu belirler

> `agent` kullanılacak ajanın özelliklerinin tanımlandığı bölümdür, bizim ajanımızın ismi ve `label` değeri `docker-agent` olduğu için `label 'docker-agent'` tanımlamasıyla hangi ajanı kullanmak istediğimizi belirtiyoruz.

> 'stages' pipeline adımlarının tanımlandığı bölümdür

> `stage` ve `steps` pipele adımının ismini ve o adımda nelerin gerçekleştirileceğini belirlendiği bölümlerdir

Bizim pipeline hattımızda öncelikle eğer varsa Docker Compose ile çalıştırılmış konteyner(ler)ı durdurmak ardından `-d` flagi ile `deamon` veya `deattached` modda `--build` flagi ile de eğer yapabiliyorsa imagei build etmesini sağlayarak konteyner(ler)i çalıştırmakta

Bütün adımlar başarılı bir şekilde gerçekleştiğinde `Build Now` butonuna bastığınız zaman Jenkins'i çalıştırdığınız makinenin `80` portundan websitesine erişebilirsiniz, Pipeline'ı SCM'e bağlayarak her `commit` yapıldığında veya belirli zaman aralıklarıyla yapılacak kontroller sonucu Pipeline tetiklenecek ve web sunucumuzun içeriği değişecek.

## Pipeline'a Güvenlik Entegrasyonu
### [Trufflehog](https://github.com/trufflesecurity/trufflehog)
```groovy
stage('Trufflehog') {
      steps {
        echo "Scanning..."
        sh "docker run --rm -v $PWD:/pwd trufflesecurity/trufflehog:latest github --json --repo ${GIT_URL}"
      }
    }
```
Pipeline içerisinde örnek bir Trufflehog kullanımı yukarıdaki gibidir. Trufflehog'u pipeline içerisinde kullanabilmek için makinede tercihen Docker aracılığıyla yüklenmiş Trufflehog olmalı. Bunun için;
```bash
docker pull trufflesecurity/trufflehog:latest
```

> `--rm` işlem bittikten sonra imagei siler ve sistemde depolama sorunlarının önüne geçer

> `-v` konteyner içerisindeki dosya içeriğine belirlenen dosya dizinine bağlar, bizim örneğimizde bu `$PWD` değişkeniyle mevcut çalışma dizinini belirtmekte.

> `--json` Trufflehog'a özel olan bir parametre ve çıktıyı `JSON` formatında almamızı sağlar

> `--repo` Trufflehog'a özel bir parametredir ve belirtilen Git Repositorysini taramasını sağlar, bizim örneğimizde `$GIT_URL` değişkeni Jenkins tarafından sağlanarak Pipeline oluştururken belirtilen Git URL'sini referans etmektedir.

Trufflehog bizim için `Credidental Hygen` konseptini sağlamaktadir. API anahtarı, JWT Token, kullanıcı adı ve şifresi gibi bilgileri tarayarak olası bilgi güvenliği sorunlarının önüne geçmektedir.
### [Trivy](https://aquasecurity.github.io/trivy/v0.53/docs/)
Trivy bizim için Trufflehog ile aynı işlemleri gerçekleştirmekle beraber Build edilen Docker imagelerini de tarayarak konteyner güvenliği kapsamında da çalışmaktadır. İlk örnekte repository scan, ikinci örnekte ise Docker Image Scan işlemlerini gerçekleştirmektedir.
Trivy sisteminize yüklemek için talimatları [resmi kaynaktan](https://aquasecurity.github.io/trivy/v0.18.3/installation/) inceleyebilirsiniz.
```groovy
stage('Trivy Repo Scan'){
      steps{
        echo "Scanning..."
        sh "trivy repository --branch ${BRANCH} ${GIT_URL}"
      }
    }
```

> `trivy repository` veya `trivy repo` repository taraması yapacağımızı belirlemekte

> `--branch` belirli bir branchi taramamızı sağlar


```groovy
stage('Trivy Docker Image Scan'){
      steps{
        echo "Trviy Docker Image Scan" 
        sh "trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}"
      }
    }
```

> `trivy image` image taraması yapacağımızı belirtir

> `--severity` belirli riskteki güvenli sorunlarını göstermesini belirtir

### Snyk



### [OWASP ZAP](https://www.zaproxy.org/docs/docker/about/)
OWASP ZAP uygulamasının docker ile çalıştırılabilir bir versiyonudur, çalışır durumdaki web uygulmasını taramamızı sağlar. Diğer uygulamalarda statik analiz yaparken ZAP dinamik analiz yapmakta.

```groovy
stage('Zaproxy Baseline Scan') {
      steps {
        echo "Initializing baseling scan..."
        sh "docker run -v ${PWD}:/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t ${HOST} -g gen.conf -r testreport.html"
        echo "Baseling scan completed succesfully"
      }
```

> `-t` TARGET değerini tanımlamakta

> `-g` config dosyasını tanımlar

> `-r` Test edilen uygulamanın `HTML` formatında rapor çıktısını verir.

Daha detaylı bilgilendirme için [ZAP Docker](https://www.zaproxy.org/docs/docker/about/).

