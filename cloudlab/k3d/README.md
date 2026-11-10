# Kubernetes on your laptop: k3d

k3d runs k3s (a small Kubernetes) inside Docker Desktop. One command makes a cluster named `fspy` with one node and a local image registry named `fspy-registry`. A load balancer sends port 8080 to the ingress.

Run every command in Git Bash, with Docker Desktop running. The cluster needs about 1 GB of memory: first stop the cloud lab with `docker compose --profile "*" down` in `~/fspy-v3-kit/cloudlab`.

## 1. Install k3d, kubectl and Helm on Windows

```bash
winget install -e --id k3d.k3d --version 5.9.0
winget install -e --id Kubernetes.kubectl --version 1.35.4
winget install -e --id Helm.Helm --version 4.3.1
```

Close VS Code and open it again, so Git Bash finds the new commands. Then check:

```bash
k3d version
kubectl version --client
helm version
```

`k3d version` shows `v5.9.0` and `k3s version v1.35.5-k3s1 (default)`, and `kubectl version --client` shows `v1.35.4`. The versions are pinned so kubectl and the cluster stay within one minor version of each other, which kubectl needs. `helm version` shows `v4.3.1`; the course's Helm commands work the same in Helm 3 and Helm 4.

### Which kubectl runs?

Docker Desktop also installs a `kubectl`, and Git Bash finds Docker Desktop's copy first. See every copy, in the order Git Bash searches them:

```bash
which -a kubectl
```

If `kubectl version --client` shows a version older than 1.34, use the winget copy. Take the folder of the line that contains `WinGet`, for example `/c/Users/asha/AppData/Local/Microsoft/WinGet/Links`, and put it first in your PATH:

```bash
echo 'export PATH="/c/Users/asha/AppData/Local/Microsoft/WinGet/Links:$PATH"' >> ~/.bashrc
source ~/.bashrc
kubectl version --client
```

Use your own folder in place of the example.

## 2. Create the cluster

```bash
k3d cluster create fspy --api-port 127.0.0.1:6550 --port "8080:80@loadbalancer" --registry-create fspy-registry
```

| Part | What it does |
|---|---|
| `fspy` | the cluster's name; kubectl's context becomes `k3d-fspy` |
| `--port "8080:80@loadbalancer"` | sends http://localhost:8080 to port 80 of the load balancer, where Traefik (the ingress controller in k3s) listens |
| `--registry-create fspy-registry` | starts a local image registry container named `fspy-registry` |

It takes 1 to 2 minutes the first time, while Docker downloads the images. Then check:

```bash
kubectl get nodes
```

You see one node, `k3d-fspy-server-0`, with STATUS `Ready`.

If `kubectl` instead fails with `host.docker.internal` and a timeout, repair the address once. See "kubectl cannot connect" under Troubleshooting.

## 3. Check metrics-server

k3s installs metrics-server, which `kubectl top` and the autoscaler use.

```bash
kubectl -n kube-system rollout status deployment/metrics-server
kubectl top nodes
```

If `kubectl top` says `metrics not available yet`, wait one minute and try again.

## 4. A first app through the ingress on port 8080

```bash
kubectl create deployment hello --image=nginx:1.30.6-alpine --replicas=2
kubectl expose deployment hello --port=80
kubectl create ingress hello --rule="/*=hello:80"
kubectl rollout status deployment/hello
curl -s http://localhost:8080/ | grep title
```

The last command prints `<title>Welcome to nginx!</title>`. Remove the app when you are done:

```bash
kubectl delete ingress,service,deployment hello
```

## 5. Get your own images into the cluster

The cluster cannot see the images on your laptop. Use one of these two ways.

### Way A: `k3d image import` (used in P12)

```bash
docker build -t hello:0.1.0 .
k3d image import hello:0.1.0 -c fspy
```

In your YAML, write `image: hello:0.1.0`.

- Import again after every rebuild.
- Never use the tag `latest` for an imported image. With `latest`, Kubernetes tries to download the image from Docker Hub and fails.
- Import only images you built. The cluster downloads Docker Hub images (such as `nginx` or `mongo`) by itself.

### Way B: the registry

The registry listens on a random port of your laptop. Find it, then tag and push:

```bash
REGISTRY_PORT=$(docker port fspy-registry 5000 | head -1 | cut -d: -f2)
docker tag hello:0.1.0 localhost:$REGISTRY_PORT/hello:0.1.0
docker push localhost:$REGISTRY_PORT/hello:0.1.0
```

Inside the cluster, the same image is `fspy-registry:5000/hello:0.1.0`. Write that in your YAML.

## 6. Helm charts

Helm installs ready-made applications (charts) from chart repositories. In 2026, the Grafana chart moved to the `grafana-community` repository:

```bash
helm repo add grafana-community https://grafana-community.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm search repo grafana-community/grafana
```

P12 shows which charts to install and with which settings.

## 7. Stop, start and delete

Stop the cluster at night, and start it again the next morning. Its volumes survive.

```bash
k3d cluster stop fspy
k3d cluster start fspy
```

Delete it when the project is over:

```bash
k3d cluster delete fspy
```

Deleting also removes the `fspy-registry` container and every image in it.

## Git Bash and paths inside pods

Git Bash changes an argument that starts with `/` into a Windows path. Put `MSYS_NO_PATHCONV=1` in front of a `kubectl` command that names a path inside a container:

```bash
MSYS_NO_PATHCONV=1 kubectl exec deploy/hello -- cat /etc/nginx/nginx.conf
```

Never `export` the variable for the whole terminal.

## Troubleshooting

- **kubectl cannot connect**: the error names `host.docker.internal` and says `timeout` or `connectex`. Docker Desktop wrote that name into the Windows hosts file with the address your laptop had then. After a Wi-Fi change, that address is wrong. Point kubectl at `127.0.0.1` instead, then check again:

  ```bash
  sed -i 's/host.docker.internal/127.0.0.1/' ~/.kube/config
  kubectl get nodes
  ```

  The repair survives `k3d cluster stop` and `start`. Do it again after `k3d cluster create`.
- **`port is already allocated`** for 8080: another stack uses the port, often Shortly from P7. Run `docker compose down` in that project's folder, then `k3d cluster delete fspy` and create the cluster again.
- **`ErrImagePull` or `ImagePullBackOff` for your own image**: the tag in the YAML differs from the imported tag, or the import failed. `k3d image import` can print `Successfully imported` even when it failed. Check the node with `docker exec k3d-fspy-server-0 crictl images | grep hello`. If the image is missing, build it with a new tag (for example `0.1.1`), import that, and use it in the YAML.
- **`metrics not available yet`**: metrics-server needs one minute after the cluster starts.
- **The laptop is slow**: run `kubectl top nodes`. Stop the cloud lab and other containers in `docker ps` that are not part of `k3d-fspy`.
