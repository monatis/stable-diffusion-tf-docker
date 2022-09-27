## stable-diffusion-tf-docker
Stable Diffusion in Docker with a simple web API and GPU support

## What is this?
[Stable Diffusion](https://github.com/CompVis/stable-diffusion) is a latent text-to-image diffusion model, made possible thanks to a collaboration with Stability AI and Runway.
It features state-of-the-art text-to-image synthesis capabilities with relatively small memory requirements (10 GB).
Divam Gupta [ported it to TensorFlow / Keras](https://github.com/divamgupta/stable-diffusion-tensorflow) from original weights.
I packed it in a Docker image with a simple web API and GPU support.

## How does it work?
This repo is intended to work on a GPU from [TensorDock Marketplace](https://marketplace.tensordock.com/).,
It should work on other machines with little-to-no change needed,
but it is a direct outcome of my experiments with recently-launched TensorDock Marketplace.
It is currently in Public Alpha, but I already like their innovative idea to democratize access to high-performance computing.
Launched in addition to their [affordable Core Cloud GPU service](https://www.tensordock.com/),
the Marketplace edition serves as a marketplace that brings clients and GPU providers together.
Hosts, i.e., those who have spare GPUs, can rent them to clients including independent researchers, startups, hobbiests, tinkerers etc.
with insanely cheap prices.
[Acording to TensorDock](https://www.tensordock.com/host),
this also lets hosts earn 2x-to-3x mining profits.
And, for a better purpose than mining meaningless cryptos.

Servers are customizable for required RAM, vCPU and disc allocated, and boot times are too short around ~45 seconds.
You may choose to start with a minimal Ubuntu image with NVIDIA drivers and Docker already installed,
or you can jump into experiments with fully-fledged images with NVIDIA drivers, Conda, TensorFlow, PyTorch and Jupyter configured.

## Ok, show me how to run
Don't let the number of steps scare you --it's only a detailed step-by-step walkthrough of the whole process from registering to making requests.
It should take no longer than ~10 minutes.

1. [Registre](https://marketplace.tensordock.com/register) and sign in to TensorDock Marketplace.
2. [Go to the order page](https://marketplace.tensordock.com/order_list), and choose a physical machine that offers a GPU with at least 10 GB of memory. I'd suggest one that offers RTX 3090.
3. This will open up a model that lets you configure your server. My suggestestions are as follows:
    - Select amount of each GPU model: 1 x GeForce RTX 3090 24 GB
    - Select amount of RAM (GB): 16
    - Select number of vCPUs: 2
    - Check checkboxes for up to 15 port forwardings. You will be able to access to your server through these ports.
    - Under "Customize your installation", select "Ubuntu 20.04 LTS".
4. Choose a password for your server, and give it a name, e.g., "stable-diffusion-api"
5. Hit "Deploy Server" and voila! Your server will be ready in seconds.
6. When you see the success page, click "Next" to see the details.
7. Find IPv4 address of your server. This may be an real IP or a subdomain like `mass-a.tensordockmarketplace.com`.
8. Find the external port mapped to internal port 22. You will use this one to SSH into your server. It might be something like 20029, for example.
9. Connect to your server using these cridentials, e.g.:
    - `ssh -p 20029 user@mass-a@tensordockmarketplace.com`


Docker is already configured for GPU access, but we need to configure Docker networking to make external requests.

10. Clone this repository and cd into it:
    - `git clone https://github.com/monatis/stable-diffusion-tf-docker.git && cd stable-diffusion-tf-docker`
11. Copy `daemon.json` over the existing `/etc/docker/daemon.json` and restart the service. Don't worry --this only adds a setting for the MTU value.
    - `sudo cp ./daemon.json /etc/docker/daemon.json`
    - `sudo systemctl restart docker.service`
12. Set an environment variable for the public port that you want to use, run Docker Compose. Our `docker-compose.yml` file will pick it up from environment variables, and it should be one of the port forwardings you configured, e.g., 20020.
    - `export PUBLIC_PORT=20020`
    - `docker compose up -d`
13. Once it's up and running, go to `http://mass-a.tensordockmarketplace.com:20020/docs` for the Swagger UI provided by FastAPI.
14. Use the `POST /generate` endpoint to generate images with Stable Diffusion. It will respond with a download ID.
15. Hit the `GET /download/<download_id>` endpoint to download your image.